from django.db.models import Avg
from rest_framework import serializers
from .models import Activity, TimeSlot, Review, GalleryImage


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption']


class ActivitySerializer(serializers.ModelSerializer):
    # 'gallery' е името што го ставивме во related_name во моделот
    gallery = GalleryImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'name', 'activity_type', 'location','google_maps_address', 'description', 'image', 'gallery', 'slots','average_rating', 'reviews_count']

    def get_average_rating(self, obj):
            # Ги зема сите поврзани рецензии и пресметува просек на полето 'rating'
            average = obj.reviews.aggregate(Avg('rating'))['rating__avg']
            return round(average, 1) if average else 0

    def get_reviews_count(self, obj):
            return obj.reviews.count()