from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Activity, Review, Reservation
from .serializers import ActivitySerializer, ReviewSerializer, RegisterSerializer, LoginSerializer, \
    ReservationSerializer
from django.shortcuts import render
from .models import Activity, TimeSlot
from datetime import datetime, time, timedelta
from django.utils import timezone


def generate_slots_for_week():
    activities = Activity.objects.all()
    today = timezone.now().date()

    for i in range(7):
        target_date = today + timedelta(days=i)

        for activity in activities:
            # Одредуваме капацитет во зависност од типот на активноста
            default_capacity = 1 if activity.activity_type == "sports_hall" else 10

            for hour in range(10, 22):
                start_dt = timezone.make_aware(
                    datetime.combine(target_date, time(hour, 0))
                )
                end_dt = timezone.make_aware(
                    datetime.combine(target_date, time(hour + 1, 0))
                )

                # get_or_create сега ќе го користи динамичкиот капацитет ако креира нов слот
                TimeSlot.objects.get_or_create(
                    activity=activity,
                    start_time=start_dt,
                    end_time=end_dt,
                    defaults={"capacity": default_capacity},
                )
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data


        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email
        })


class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        if not TimeSlot.objects.filter(start_time__date=today).exists():
            generate_slots_for_week()

        return super().get(request, *args, **kwargs)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReservationView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    @api_view(['DELETE'])
    def cancel_reservation(request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.delete()
            return Response({"message": "Reservation cancelled successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        timeslot_id = self.request.data.get("timeslot")

        with transaction.atomic():
            try:
                # Ја заклучуваме редицата за TimeSlot
                slot = TimeSlot.objects.select_for_update().get(id=timeslot_id)
            except TimeSlot.DoesNotExist:
                raise ValidationError({"error": "Избраниот термин не постои."})

            # Проверка дали веќе е полн
            if slot.is_full:
                raise ValidationError({"error": "Овој термин е веќе исполнет!"})

            # Се зачувува резервацијата
            serializer.save(user=self.request.user)

            # ПОПРАВЕНО: Бидејќи во модел немаш дефинирано related_name, се користи reservation_set
            current_count = slot.reservation_set.count()

            # Ако се исполни капацитетот, се означува како полн
            if current_count >= slot.capacity:
                slot.is_full = True
                slot.save()

