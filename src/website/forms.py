from django import forms
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []