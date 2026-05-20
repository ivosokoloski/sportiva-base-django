from rest_framework import generics
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
            for hour in range(10, 22):
                start_dt = timezone.make_aware(datetime.combine(target_date, time(hour, 0)))
                end_dt = timezone.make_aware(datetime.combine(target_date, time(hour + 1, 0)))

                # get_or_create за да не прави дупликати ако веќе постојат
                TimeSlot.objects.get_or_create(
                    activity=activity,
                    start_time=start_dt,
                    end_time=end_dt,
                    defaults={'capacity': 10}
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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



