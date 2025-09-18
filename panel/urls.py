from django.urls import path
from . import views

urlpatterns = [
    path('api/jobs/', views.get_jobs, name='get_jobs'),
    path('api/jobs/post/', views.post_job, name='post_job'),
    path('api/jobs/search/', views.search_jobs, name='search_jobs'),
]