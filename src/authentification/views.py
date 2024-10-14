from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Utilisateur
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur avec le formulaire Django
            user = form.save()
            
            # Enregistrer également dans le modèle Utilisateur
            Utilisateur.objects.create(
                nom=user.username,
                email=user.email,
                mot_de_passe=user.password
            )

            # Connecter l'utilisateur après l'inscription
            login(request, user)
            return redirect('index')  # Redirige vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()

    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        mot_de_passe = request.POST['password']  # Correspond à 'password' dans le formulaire
        user = authenticate(request, username=username, password=mot_de_passe)  # Corrige la clé
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')
