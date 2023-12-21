from django import forms
from .models import User, Document, Email

class LoginForm(forms.Form):
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
    

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_id', 'user_pw', 'user_email', 'user_dep', 'user_phone']
        widgets = {
            'user_name': forms.TextInput(
                attrs={
                    "class":'form-control'
                }
            ),
            'user_id': forms.TextInput(
                attrs={
                    "class":'form-control'
                }
            ),
            'user_pw': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'user_email': forms.EmailInput(
                attrs={
                    "class":'form-control'
                }
            ),
            'user_dep': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'user_phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('uploaded_file',)
        
class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['email_file_name','email_subject','email_date','email_from','email_to','email_cc','email_text_content']