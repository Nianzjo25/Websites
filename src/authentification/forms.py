from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        help_text="Une adresse e-mail valide est requise.",
        widget=forms.EmailInput(attrs={'placeholder': 'Entrez votre adresse e-mail'})
    )

    password1 = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe', 'autocomplete': 'new-password'}),
        help_text="Le mot de passe doit contenir au moins 8 caractères."
    )

    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez votre mot de passe', 'autocomplete': 'new-password'}),
        strip=False,
        help_text="Veuillez entrer le même mot de passe pour confirmation."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Entrez votre nom d\'utilisateur'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise ValidationError("Le nom d'utilisateur ne peut pas contenir le symbole '@'.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un compte avec cette adresse e-mail existe déjà.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        return cleaned_data
