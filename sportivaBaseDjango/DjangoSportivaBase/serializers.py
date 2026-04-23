from rest_framework import serializers
from django.db.models import Avg
from .models import Activity, TimeSlot, Review, GalleryImage


# Прво дефинирај го ReviewSerializer за да можеш да го користиш во views
class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(
        source='user.username')  # Го додаваме ова за да го видиш името на тој што оставил коментар

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
    # Овие линии овозможуваат React да ги види сите слики и термини во еден JSON објект
    gallery = GalleryImageSerializer(many=True, read_only=True)
    slots = TimeSlotSerializer(many=True, read_only=True)

    # Ако сакаш и рецензиите да се гледаат во деталите на активноста:
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