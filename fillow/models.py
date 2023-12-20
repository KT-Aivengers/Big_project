from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class User(models.Model):
    user_name = models.CharField("이름", max_length=10)
    user_phone = models.CharField(
        "전화번호 (010-****-**** 의 형태로 입력해주세요.)",
        max_length=16,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                message="010-****-****의 형태로 입력해주세요."
            ),
        ],
    )
    user_id = models.CharField("아이디", max_length=20)
    user_pw = models.CharField("비밀번호", max_length=30)
    user_dep = models.CharField("부서", max_length=10)
    user_email = models.EmailField("이메일")
    
    def __str__(self):
        return self.user_id
<<<<<<< Updated upstream

class Document(models.Model):
    uploaded_file = models.FileField(upload_to='documents/')
=======
    
from allauth.socialaccount.forms import SignupForm, DisconnectForm
class MyCustomSocialSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

class MyCustomSocialDisconnectForm(DisconnectForm):

    def save(self):

        # Add your own processing here if you do need access to the
        # socialaccount being deleted.

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomSocialDisconnectForm, self).save()

        # Add your own processing here if you don't need access to the
        # socialaccount being deleted.
>>>>>>> Stashed changes
