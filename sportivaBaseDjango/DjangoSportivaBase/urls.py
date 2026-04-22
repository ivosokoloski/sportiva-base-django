from django.urls import path
from .views import ActivityList # Сега работи со точка бидејќи се во иста папка

urlpatterns = [
    path('activities/', ActivityList.as_view(), name='activity-list'),
]