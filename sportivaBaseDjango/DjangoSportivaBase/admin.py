from django.contrib import admin
from .models import Activity, TimeSlot, Reservation, Review, GalleryImage


# Ова овозможува додавање термини директно во страната на Активноста
class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1  # Колку празни полиња за термини да се појават одеднаш

# Ова овозможува преглед на рецензиите директно во Активноста
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'comment') # Рецензиите обично само ги читаме во админ


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'activity_type', 'location', 'created_at','google_maps_address')
    list_filter = ('activity_type',)
    search_fields = ('name', 'location')
    inlines = [TimeSlotInline, ReviewInline, GalleryImageInline]
@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('activity', 'start_time', 'end_time', 'capacity', 'is_full')
    list_filter = ('activity', 'start_time')
    date_hierarchy = 'start_time' # Додава лента за навигација по датуми на врвот

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'timeslot', 'reserved_at', 'status')
    list_filter = ('status', 'reserved_at')
    search_fields = ('user__username', 'timeslot__activity__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')