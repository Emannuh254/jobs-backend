# jobs/views.py
from django.views import View
from django.http import JsonResponse
from .models import Job

class JobList(View):
    def get(self, request):
        jobs = list(Job.objects.values())  # get all jobs as dicts
        return JsonResponse(jobs, safe=False)
