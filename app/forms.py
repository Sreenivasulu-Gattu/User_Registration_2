from app.models import *
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {'password':forms.PasswordInput(attrs={'placeholder':'password under privilages','data-toggle':'password'})}
        help_texts = {'username':' '}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','profile_pic']
