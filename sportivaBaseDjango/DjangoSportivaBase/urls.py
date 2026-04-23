from django.urls import path
from .views import ActivityList, ActivityDetail  # Додај го и ActivityDetail овде

urlpatterns = [
    path('activities/', ActivityList.as_view(), name='activity-list'),


    path('activities/<int:pk>/', ActivityDetail.as_view(), name='activity-detail'),
]