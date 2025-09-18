from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from .models import Job

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def post_job(request):
    try:
        data = json.loads(request.body)
        
        job = Job(
            title=data['title'],
            company=data['company'],
            location=data['location'],
            type=data['type'],
            salary=data['salary'],
            tags=', '.join(data['tags']),
            description=data['description'],
            requirements=data['requirements'],
            application_link=data['application_link'],
            posted_by=request.user
        )
        job.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Job posted successfully!',
            'job_id': job.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Error: {str(e)}'
        }, status=400)

@require_http_methods(["GET"])
@login_required
def search_jobs(request):
    query = request.GET.get('q', '')
    jobs = Job.objects.all()
    
    if query:
        jobs = jobs.filter(
            models.Q(title__icontains=query) |
            models.Q(company__icontains=query) |
            models.Q(location__icontains=query)
        )
    
    job_data = []
    for job in jobs:
        job_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'type': job.type,
            'salary': job.salary,
            'tags': job.get_tags_list(),
            'description': job.description,
            'requirements': job.requirements,
            'application_link': job.application_link,
            'posted_date': job.posted_date.strftime('%Y-%m-%d'),
        })
    
    return JsonResponse({'jobs': job_data})

@require_http_methods(["GET"])
@login_required
def get_jobs(request):
    jobs = Job.objects.all().order_by('-posted_date')
    
    job_data = []
    for job in jobs:
        job_data.append({
            'id': job.id,
            'title': job.title,
            'company': job.company,
            'location': job.location,
            'type': job.type,
            'salary': job.salary,
            'tags': job.get_tags_list(),
            'description': job.description,
            'requirements': job.requirements,
            'application_link': job.application_link,
            'posted_date': job.posted_date.strftime('%Y-%m-%d'),
        })
    
    return JsonResponse({'jobs': job_data})