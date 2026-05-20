from django.urls import path
from .views import *

urlpatterns = [

    path('activities/', ActivityList.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityDetail.as_view(), name='activity-detail'),


    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('review/', ReviewView.as_view(), name='add-review'),
    path('reservations/', ReservationList.as_view(), name='reservation-list'),
    path('reservation/', ReservationView.as_view(), name='add-reservation'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('users/', UserList.as_view(), name='users'),

]