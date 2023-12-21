from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AdditionalInform(User):
    department = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    

class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')