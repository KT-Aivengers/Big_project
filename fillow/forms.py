from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id', 'user_pw', 'user_email', 'user_dep']