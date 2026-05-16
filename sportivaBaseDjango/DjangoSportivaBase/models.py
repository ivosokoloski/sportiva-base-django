from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    TYPE_CHOICES = [
        ('gym', 'Gym'),
        ('boxing', 'Boxing'),
        ('sports_hall', 'Sports Hall'),
    ]

    name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=255)
    google_maps_address = models.CharField(max_length=255,default="null")
    description = models.TextField()
    image = models.ImageField(upload_to='activities/')
    created_at = models.DateTimeField(auto_now_add=True)
    services = models.ManyToManyField('Service', blank=True, related_name='activities')

    def __str__(self):
        return self.name



class TimeSlot(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=10)  # Колку луѓе можат да резервираат во исто време
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.activity.name} ({self.start_time})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='confirmed') # confirmed, canceled

    class Meta:
        unique_together = ('user', 'timeslot') # Спречува ист корисник да резервира ист термин двапати






class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # Оценка од 1 до 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class GalleryImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='activities/gallery/')
    caption = models.CharField(max_length=100, blank=True) # Опционален опис на сликата

    def __str__(self):
        return f"Image for {self.activity.name}"





