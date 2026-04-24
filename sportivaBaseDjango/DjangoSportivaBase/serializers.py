from rest_framework import serializers
from django.db.models import Avg
from django.contrib.auth.models import User
from .models import Activity, TimeSlot, Review, GalleryImage


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


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at']

class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption']

class ActivitySerializer(serializers.ModelSerializer):
    gallery = GalleryImageSerializer(many=True, read_only=True)
    slots = TimeSlotSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'activity_type', 'location',
            'google_maps_address', 'description', 'image',
            'gallery', 'slots', 'reviews', 'average_rating', 'reviews_count'
        ]

    def get_average_rating(self, obj):
        average = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average, 1) if average else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()