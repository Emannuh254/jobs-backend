from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

class User(AbstractUser):
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    points = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)
    
    def generate_referral_code(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while User.objects.filter(referral_code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return code
    
    def __str__(self):
        return self.username