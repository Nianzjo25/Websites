# Website

## Récupération du projet

Pour récupérer le projet, ouvrez un terminal sur votre ordinateur et tapez la commande suivante :

```bash
git clone https://github.com/Nianzjo25/Website.git
```

## Installation et configuration

Après avoir cloné le projet, exécutez les commandes suivantes :

1. **Accéder au répertoire du projet :**

   ```bash
   cd Website/src
   ```

2. **Créer un environnement virtuel :**

   - Si vous utilisez l'environnement Python standard :

     ```bash
     python -m venv env
     env/Scripts/activate  # Pour Windows
     # source env/bin/activate  # Pour macOS/Linux
     ```

   - Si vous utilisez Anaconda :

     ```bash
     conda create --name env
     conda activate env
     ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   pip install mysqlclient
   ```

## Configuration de la base de données

Ouvrez le fichier `settings.py` et configurez la base de données selon le système que vous utilisez :

### Pour SQLite :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```

### Pour PostgreSQL :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nom_de_la_base',
        'USER': 'utilisateur',
        'PASSWORD': 'mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Pour MySQL :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nom_de_la_base',
        'USER': 'ton_utilisateur',
        'PASSWORD': 'ton_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## Migrer la base de données

Exécutez les commandes suivantes pour appliquer les migrations :

```bash
python manage.py makemigrations
python manage.py migrate
```

## Lancer le serveur

Enfin, lancez le serveur de développement :

```bash
python manage.py runserver
```

