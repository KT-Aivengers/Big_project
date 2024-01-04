from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

class AdditionalInform(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=10)
    phone = models.CharField(max_length=16, 
        validators=[
            RegexValidator(
                regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                message="010-****-****의 형태로 입력해주세요."
            ),
        ],)
    introduce = models.CharField(max_length=500)
    image = models.ImageField(upload_to="profile/")
    USERNAME_FIELD = 'email'
    company = models.CharField(max_length=10)
class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')
    
class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    # tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='emails', null=True)
    email_file_name = models.CharField(max_length=100)
    email_subject = models.CharField(max_length=100)
    email_from = models.CharField(max_length=1000)
    email_to = models.CharField(max_length=1000)
    email_cc = models.CharField(max_length=1000, null=True)
    email_file = models.FileField(upload_to='uploads/', null=True)
    email_text_content = models.CharField(max_length=10000)
    email_date = models.DateTimeField()
    category = models.CharField(max_length=100)
    from_company = models.CharField(max_length=100)
    from_dept = models.CharField(max_length=100)
    from_name = models.CharField(max_length=100)
    reply_req_yn = models.BooleanField(default=False)
    reply_start_date = models.CharField(max_length=100)
    reply_end_date = models.CharField(max_length=100)
    company_yn = models.BooleanField(default=False)
    department_yn = models.BooleanField(default=False)
    reply_yn = models.BooleanField(default=False)
    reply_date = models.CharField(max_length=100, null=True)
    meeting_date = models.TextField(null=True)
    read = models.BooleanField(default=False)
    trash = models.BooleanField(default=False) 
    sent = models.BooleanField(default = False)
    
class Qna(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="qna")
    question = models.CharField(max_length=300, blank=True)
    # image = models.ImageField(blank=True, upload_to='fillow')
    answer = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=50, blank=True)
    edit_date = models.DateField()

class EmailCompose(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_compose')
    email_to = models.CharField(max_length=1000)
    email_cc = models.CharField(max_length=1000, blank=True)
    email_subject = models.CharField(max_length=100)
    email_file = models.FileField(upload_to='documents/compose/', blank=True)
    email_text_content = models.CharField(max_length=1000)    

class EmailComposeTpl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tpl')
    texts = models.CharField(max_length=1000, blank=True)
