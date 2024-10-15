from django.db import models
from authentification.models import Utilisateur
from django.contrib.auth.models import User

class Norme(models.Model):
    id_norme = models.CharField(max_length=50, unique=True, default="default_id")
    libelle = models.CharField(max_length=128)

    class Meta:
        unique_together = ('id_norme', 'libelle')
        db_table = 'normes'  # Nom de la table dans la base de données
        verbose_name = 'Norme'
        verbose_name_plural = 'Normes'

    def __str__(self):
        return f"{self.id_norme} - {self.libelle}"


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True, related_name='uploaded_files')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    norme = models.CharField(max_length=255, default="internationale")
    results = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'uploaded_files'
        verbose_name = 'Fichier Uploadé'
        verbose_name_plural = 'Fichiers Uploadés'

    def __str__(self):
        return f"File: {self.file.name} uploaded at {self.uploaded_at}"


class Parametre(models.Model):
    libelle = models.CharField(max_length=255)
    sup = models.BooleanField(default=False)

    class Meta:
        db_table = 'parametres'
        verbose_name = 'Paramètre'
        verbose_name_plural = 'Paramètres'

    def __str__(self):
        seuil = "Supérieur" if self.sup else "Inférieur"
        return f"{self.libelle} - Seuil: {seuil}"


class NormeParametres(models.Model):
    norme = models.ForeignKey(Norme, on_delete=models.RESTRICT, null=True, blank=True, related_name='norme_parametres')
    parametre = models.ForeignKey(Parametre, on_delete=models.RESTRICT, null=True, blank=True, related_name='norme_parametres')
    valeurs_indicatrices = models.FloatField()

    class Meta:
        db_table = 'norme_parametres'
        verbose_name = 'Norme Paramètre'
        verbose_name_plural = 'Normes Paramètres'

    def __str__(self):
        return f"Norme: {self.norme} - Paramètre: {self.parametre} - Valeur: {self.valeurs_indicatrices}"


class Resultats(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True, related_name='resultats')
    resultat = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resultats'
        verbose_name = 'Résultat'
        verbose_name_plural = 'Résultats'

    def __str__(self):
        return f"Résultat de {self.utilisateur.nom} - {self.resultat}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        
    def __str__(self):
        return self.user.username