from rest_framework import generics
from .models import Activity, Review  # Провери дали е вака
from .serializers import ActivitySerializer, ReviewSerializer # Додај го ReviewSerializer ако го имаш


class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ActivitySerializer