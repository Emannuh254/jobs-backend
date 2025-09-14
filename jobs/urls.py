# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobList.as_view(), name='job-list'),
    path('<int:pk>/', views.JobDetail.as_view(), name='job-detail'),
    path('create/', views.JobCreate.as_view(), name='job-create'),
    # Add more job-related URLs as needed
]