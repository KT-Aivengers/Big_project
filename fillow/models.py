from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class AdditionalInform(User):
    department = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    
class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')
    
class Email(models.Model):
    email_file_name = models.CharField(max_length=100)
    email_subject = models.CharField(max_length=100)
    email_date = models.CharField(max_length=100)
    email_from = models.CharField(max_length=1000)
    email_to = models.CharField(max_length=1000)
    email_cc = models.CharField(max_length=1000)
    email_text_content = models.CharField(max_length=10000)
    
class Qna(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="qna")
    question = models.CharField(max_length=300, blank=True)
    # image = models.ImageField(blank=True, upload_to='fillow')
    answer = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10, blank=True)
    edit_date = models.DateField()