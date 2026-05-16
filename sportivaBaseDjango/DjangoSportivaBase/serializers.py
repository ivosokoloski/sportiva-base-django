from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Activity, TimeSlot, Review, GalleryImage, Reservation, Service


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    def get_users_count(self):
        return User.objects.count()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at']


class ReservationSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Reservation
        fields = ['id', 'user_name', 'timeslot', 'reserved_at', 'status']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name','icon']


class ActivitySerializer(serializers.ModelSerializer):
    gallery = GalleryImageSerializer(many=True, read_only=True)
    slots = TimeSlotSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    reservations=ReservationSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    services = ServiceSerializer(many=True, read_only=True)



    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'activity_type', 'location',
            'google_maps_address', 'description', 'image',
            'gallery', 'slots', 'reviews','reservations', 'average_rating', 'reviews_count','services'
        ]

    def get_average_rating(self, obj):
        average = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 1) if average else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()

