from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApplicationListCreateView.as_view(), name='application-list-create'),
    path('<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('job/<int:job_id>/', views.JobApplicationsView.as_view(), name='job-applications'),
]