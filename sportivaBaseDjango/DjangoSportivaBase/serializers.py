from rest_framework import serializers
from .models import Activity, TimeSlot, Review


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    slots = TimeSlotSerializer(many=True, read_only=True)  # Гледање на термини во самата активност

    class Meta:
        model = Activity
        fields = ['id', 'name', 'activity_type', 'location', 'description', 'image', 'slots']