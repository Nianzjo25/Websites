from django.db import models

class Utilisateur(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    mot_de_passe = models.CharField(max_length=128)  # Haché

    class Meta:
        db_table = 'utilisateurs'  # Nom de la table dans la base de données
        verbose_name = 'Utilisateur'  # Nom singulier pour l'admin
        verbose_name_plural = 'Utilisateurs'  # Nom pluriel pour l'admin

    def __str__(self):
        return self.nom


