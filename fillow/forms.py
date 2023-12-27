from django.contrib.auth.forms import UsernameField
from django import forms
from .models import Document, Email, AdditionalInform, Qna, EmailComposeTpl
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model, password_validation


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="아이디",
        widget = forms.TextInput(
            attrs={
                "class": 'form-control',
                "placeholder": "아이디를 입력하세요"  
            }
        ),
    )
    password = forms.CharField(
        label="비밀번호",
        widget = forms.PasswordInput(
            attrs={
                "class": 'form-control',
                "placeholder": "비밀번호를 입력하세요",
            }
        ),
    )


class UserForm(UserCreationForm):
    username = UsernameField(label = "아이디", widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(
        label=("비밀번호"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("비밀번호 확인"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}),
        strip=False,
        # help_text=("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(label = "이메일", widget=forms.EmailInput(attrs={"class":"form-control"}))
    department = forms.CharField(label = "부서", widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label = "이름", widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label = "성", widget=forms.TextInput(attrs={"class":"form-control"}))
    
    phone = forms.CharField(
        label="전화번호",
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$',
                message="010-****-****의 형태로 입력해주세요."
            ),
        ], 
        widget=forms.TextInput(attrs={"class":"form-control"})
    )
    
    class Meta:
<<<<<<< HEAD
        model = User
        fields = ['user_id', 'user_pw', 'user_email', 'user_dep']
        # asd
=======
        model = AdditionalInform
        fields = ["username", "last_name", "first_name", "password1", "password2", "email", "department", "phone"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('uploaded_file',)
        
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email_file_name','email_subject','email_date','email_from','email_to','email_cc','email_text_content']
        
        
class QnaForm(forms.ModelForm):
    class Meta:
        model = Qna
        fields = ['title', 'question']
        
class EmailComposeTplForm(forms.ModelForm):
    class Meta:
        model = EmailComposeTpl
        fields = ['texts']
        widgets = {
            'texts': forms.Textarea(attrs={'placeholder': ''}),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(EmailComposeTplForm, self).__init__(*args, **kwargs)
    #     self.fields['texts'].required = False
        
       
>>>>>>> BE
