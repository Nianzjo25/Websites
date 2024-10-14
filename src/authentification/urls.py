from django.urls import path
from . import views as view

urlpatterns = [
    path('', view.inscription, name='inscription'),
    path('connexion', view.connexion, name='connexion'),
    path('deconnexion', view.deconnexion, name='deconnexion'),
]