# Generated by Django 5.1.1 on 2024-10-06 09:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('libelle', models.CharField(max_length=255)),
                ('sup', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Paramètre',
                'verbose_name_plural': 'Paramètres',
                'db_table': 'parametres',
            },
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('norme', models.CharField(default='internationale', max_length=255)),
                ('results', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Fichier Uploade',
                'verbose_name_plural': 'Fichiers Uploades',
                'db_table': 'uploaded_files',
            },
        ),
        migrations.CreateModel(
            name='Norme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_norme', models.CharField(default='default_id', max_length=50, unique=True)),
                ('libelle', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Norme',
                'verbose_name_plural': 'Normes',
                'db_table': 'normes',
                'unique_together': {('id_norme', 'libelle')},
            },
        ),
        migrations.CreateModel(
            name='NormeParametres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeurs_indicatrices', models.FloatField()),
                ('id_norme', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='website.norme')),
                ('id_parametres', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='website.parametre')),
            ],
            options={
                'verbose_name': 'Norme Paramètre',
                'verbose_name_plural': 'Normes Paramètres',
                'db_table': 'norme_parametres',
            },
        ),
        migrations.CreateModel(
            name='Resultats',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resultat', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='authentification.utilisateur')),
            ],
            options={
                'verbose_name': 'Résultat',
                'verbose_name_plural': 'Résultats',
                'db_table': 'resultats',
            },
        ),
    ]
