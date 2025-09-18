from django.db import models
from django.conf import settings  # ✅ use this, not direct User import

class Job(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=JOB_TYPES)
    salary = models.CharField(max_length=100)
    tags = models.CharField(max_length=200, help_text="Comma separated tags")
    description = models.TextField()
    requirements = models.TextField()
    application_link = models.URLField()
    posted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
