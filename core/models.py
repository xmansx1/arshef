# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'مدير'),
        ('employee', 'موظف'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
from django.db import models
from django.conf import settings


class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20)
    job_title = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)

    # ✅ الحقل الذي يرفع الصورة ويحفظها داخل media/profiles/
    personal_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Attachment(models.Model):
    profile = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='attachments')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.profile.user.username}"

 
