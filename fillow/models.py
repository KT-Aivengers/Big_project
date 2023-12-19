from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20)
    user_pw = models.CharField(max_length=30)
    user_dep = models.CharField(max_length=10)
    user_email = models.EmailField()
    
    def __str__(self):
        return self.user_id