from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer, ApplicationCreateSerializer
from jobs.models import Job

class ApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ApplicationCreateSerializer
        return ApplicationSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Application.objects.all()
        return Application.objects.filter(applicant=self.request.user)
    
    def perform_create(self, serializer):
        job_id = serializer.validated_data.get('job').id
        job = Job.objects.get(id=job_id)
        
        if Application.objects.filter(job=job, applicant=self.request.user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        if self.request.user.points < 5:
            raise serializers.ValidationError("You need at least 5 points to apply for this job.")
        
        self.request.user.points -= 5
        self.request.user.save()
        
        serializer.save(applicant=self.request.user)

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        if obj.applicant != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to view this application.")
        return obj
    
    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to update this application.")
        serializer.save()

class JobApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)
        
        if job.posted_by != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to view these applications.")
        
        return Application.objects.filter(job=job)