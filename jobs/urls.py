from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateView.as_view(), name='job-list-create'),
    path('my-jobs/', views.UserJobsView.as_view(), name='user-jobs'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
]