from django import forms
from .models import User, Document

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