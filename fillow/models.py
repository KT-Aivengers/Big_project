from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

class AdditionalInform(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=10)
    # 암호화된 전화번호를 저장할 내부 필드 추가
    _phone = models.CharField(max_length=255, null=True, blank=True)

    # 외부에서 접근할 phone 필드는 실제로는 암호화된 데이터를 처리합니다.
    @property
    def phone(self):
        # 복호화하여 평문 전화번호 반환
        if self._phone:  # 암호화된 데이터가 있을 경우에만 복호화 진행
            encrypted_data = self._phone.encode()
            decrypted_data = settings.FERNET_CIPHER_SUITE.decrypt(encrypted_data)
            return decrypted_data.decode()
        return None

    @phone.setter
    def phone(self, value):
        # 유효성 검사 수행
        validator = RegexValidator(
            regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
            message="010-****-****의 형태로 입력해주세요."
        )
        validator(value)

        # 전화번호 암호화하여 내부 필드에 저장
        encrypted_data = settings.FERNET_CIPHER_SUITE.encrypt(value.encode())
        self._phone = encrypted_data.decode()
    introduce = models.CharField(default='안녕하세요', max_length=500)
    image = models.ImageField(upload_to="profile/")
    USERNAME_FIELD = 'email'
    company = models.CharField(max_length=10)
    schedule = models.TextField(default='[]')
    
    
class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')
    
class Email(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    email_file_name = models.CharField(max_length=100)
    email_subject = models.CharField(max_length=100)
    email_from = models.CharField(max_length=1000)
    email_to = models.CharField(max_length=1000)
    email_cc = models.CharField(max_length=1000, null=True)
    email_file = models.FileField(upload_to='uploads/', null=True)
    email_text_content = models.CharField(max_length=10000)
    email_date = models.DateTimeField()
    category = models.CharField(max_length=100)
    from_company = models.CharField(max_length=100, null=True)
    from_dept = models.CharField(max_length=100, null=True)
    from_name = models.CharField(max_length=100, null=True)
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
    spam = models.BooleanField(default = False)
    
class Qna(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="qna")
    question = models.CharField(max_length=300, blank=True)
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
