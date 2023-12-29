from django.contrib.auth.forms import UsernameField
from django import forms
from .models import Document, Email, AdditionalInform, Qna, EmailCompose, EmailComposeTpl
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

class AdditionalInformForm(forms.ModelForm):
    department = forms.CharField(label = "부서", widget=forms.TextInput(attrs={"class":"form-control"}))
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
        model = AdditionalInform
        fields = ['department', 'phone']

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
    username = forms.CharField(label = "아이디", widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(
        label=("비밀번호"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}),
    )
    password2 = forms.CharField(
        label=("비밀번호 확인"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}),
        strip=False,
    )
    email = forms.EmailField(label = "이메일", widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label = "이름", widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label = "성", widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["username", "last_name", "first_name", "password1", "password2", "email"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['uploaded_file',]
        
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email_file_name','email_subject','email_date','email_from','email_to','email_cc','email_text_content']
        
        
class QnaForm(forms.ModelForm):
    class Meta:
        model = Qna
        fields = ['title', 'question']

class EmailComposeForm(forms.ModelForm):
    class Meta:
        model = EmailCompose
        fields = ['email_to','email_cc','email_subject','email_file','email_text_content']
        widgets = {
            'email_to': forms.TextInput(attrs={'class': 'form-control bg-transparent', 'placeholder': ''}),
            'email_cc': forms.TextInput(attrs={'class': 'form-control bg-transparent', 'placeholder': ''}),
            'email_subject': forms.TextInput(attrs={'class': 'form-control bg-transparent', 'placeholder': ''}),
            'email_file': forms.FileInput(attrs={'class': 'form-control', 'id': 'formFileMultiple', 'multiple': True}),
            'email_text_content': forms.Textarea(attrs={'class': 'form-control bg-transparent', 'rows': 15, 'placeholder': '내용을 입력하세요'}),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['email_cc'].required = False  
            self.fields['email_file'].required = False  
    
class EmailComposeTplForm(forms.ModelForm):
    class Meta:
        model = EmailComposeTpl
        fields = ['texts']
        widgets = {
            'texts': forms.Textarea(attrs={'placeholder': ''}),
        }
    

class QnaSearchForm(forms.Form):
    STATUS_CHOICES = [
        (0, '---'),
        (1, '답변 대기중'),
        (2, '답변 완료'),
    ]  
    title = forms.CharField(label = "제목",
                            widget=forms.TextInput(
                                attrs={
                                    "class":"form-control mb-xl-0 mb-3",
                                    "id":"exampleFormControlInput1",
                                    "placeholder":"제목",
                                    }
                                ),
                            required=False,
                            )
    status = forms.CharField(label = "상태",
                             widget=forms.Select(
                                 attrs={
                                     "class": "form-control default-select h-auto wide",
                                     "aria-label": "Default select example"
                                 },
                                 choices=STATUS_CHOICES,
                             ),
                            )
