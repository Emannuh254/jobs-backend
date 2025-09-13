from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer, JobCreateSerializer

class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobSerializer
    
    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        if self.request.user != self.get_object().posted_by and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to edit this job.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user != instance.posted_by and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to delete this job.")
        instance.delete()

class UserJobsView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)