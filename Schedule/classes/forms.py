from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import New
from classes.models import Post
from django.contrib.auth.models import User

class HomeForm(forms.ModelForm):
    class Meta: 
        model = Post
        fields = ['class_name', 'credits']

class DeleteNewForm(forms.ModelForm):
    class Meta:
        model = New
        fields = []

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')