from django.urls import path
from .views import ActivityList, ActivityDetail, ReviewList, RegisterView, LoginView, UserList

urlpatterns = [

    path('activities/', ActivityList.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityDetail.as_view(), name='activity-detail'),


    path('reviews/', ReviewList.as_view(), name='review-list'),


    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    path('users/', UserList.as_view(), name='users'),

]