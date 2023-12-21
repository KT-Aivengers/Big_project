from django.contrib.auth.forms import UsernameField
from django import forms
from django.contrib.auth.models import User
from .models import Document
from django.core.validators import RegexValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.text import capfirst
from django.contrib.auth import authenticate, get_user_model, password_validation

UserModel = get_user_model()

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
    
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)
        
        print(self)


class UserForm(UserCreationForm):
    username = UsernameField(label = "아이디", widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class":"form-control"}),
        strip=False,
        # help_text=("Enter the same password as before, for verification."),
    )
    email = forms.EmailField(label = "이메일", widget=forms.EmailInput(attrs={"class":"form-control"}))
    department = forms.CharField(label = "부서", widget=forms.TextInput(attrs={"class":"form-control"}))
    name = forms.CharField(label = "이름", widget=forms.TextInput(attrs={"class":"form-control"}))
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
        model = User
        fields = ["username", "name", "password1", "password2", "email", "department", "phone"]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('uploaded_file',)