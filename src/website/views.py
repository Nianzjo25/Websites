from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import pandas as pd
from .models import Norme, UploadedFile, NormeParametres, Parametre, Utilisateur, Profile
from .calculs import calcul_formule_f1, calcul_formule_f2, calcul_formule_f3
from django.db import IntegrityError
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.views.generic import TemplateView
import numpy as np
 

def test(request):
    return render(request, 'template.html')


def acceuil(request):
    return render(request, 'acceuil.html')


def index(request):
    return render(request, 'index.html')

@login_required
def users(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_image = profile.profile_image.url if hasattr(user, 'profile') and profile.profile_image else 'profile_images/images.jpg'
    
    context = {
        'user': user,
        'profile_image': profile_image
    }
    return render(request, 'user_profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)  # Use get() instead of filter()

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')

        if 'profile_image' in request.FILES:  # Check if a file is uploaded
            profile.profile_image = request.FILES['profile_image']

        user.save()  # Save the updated user information
        profile.save()  # Save the updated profile
        return redirect('user_profile')  # Redirect to the profile page after saving

    return render(request, 'edit_profile.html', {'user': user, 'profile': profile})


@login_required
def historique(request):
    # Fetch all uploaded files for the current user
    uploaded_files = UploadedFile.objects.filter(user=request.user).order_by('-uploaded_at')
    print(uploaded_files)
    # Prepare the context with detailed information for each file
    context = {
        'uploaded_files': []
    }

    for file in uploaded_files:
        file_info = {
            'filename': file.file.name,
            'uploaded_at': file.uploaded_at,
            'norme': file.norme,
            'results': file.results,
            'parameters': []
        }

        # Fetch the norme object
        try:
            norme = Norme.objects.get(id_norme=file.norme)
            # Fetch all parameters for this norme
            norme_params = NormeParametres.objects.filter(norme=norme)
            
            for param in norme_params:
                parameter_info = {
                    'name': param.parametre.libelle,
                    'indicative_value': param.valeurs_indicatrices,
                    'calculated_value': file.results.get(param.parametre.libelle, 'N/A')
                }
                file_info['parameters'].append(parameter_info)
        except Norme.DoesNotExist:
            # Handle the case where the norme doesn't exist
            file_info['parameters'] = []

        context['uploaded_files'].append(file_info)

    return render(request, 'historique.html', context)

def apropos(request):
    return render(request, 'apropos.html')

def details_ipo(request):
    return render(request, 'details_ipo.html')

def details_iqe(request):
    return render(request, 'details_iqe.html')

def details_iqa(request):
    return render(request, 'details_iqa.html')


def test(request):
    return render(request, 'template.html')


@login_required  # Assure que l'utilisateur est connecté avant d'accéder à cette vue
def tableau_de_bord(request):
    # Accéder au nom de l'utilisateur connecté
    user_name = request.user.first_name or request.user.username
    return render(request, 'tableau_de_bord.html', {'user_name': user_name})


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='post')
class FileUploadView(TemplateView):
    template_name = 'calcul.html'

    def post(self, request, *args, **kwargs):
        TAILLE_MAX_FILE = 2 * 1024 * 1024  # 2 Mo

        try:
            if 'file' not in request.FILES:
                return JsonResponse({'error': 'Aucun fichier téléchargé'}, status=400)

            uploaded_file = request.FILES['file']

            if uploaded_file.size > TAILLE_MAX_FILE:
                return JsonResponse({'error': 'Le fichier dépasse la taille maximale autorisée de 2 Mo.'}, status=400)

            df = self.lire_fichier(uploaded_file)
            
            print("Données du fichier :")
            print(df.head())  # Vérifiez le contenu du DataFrame
            
            norme_type = request.POST.get('norme')
            if norme_type not in ['européenne', 'américaine', 'internationale']:
                return JsonResponse({'error': 'Norme invalide'}, status=400)

            norme = Norme.objects.get(id_norme=norme_type)

            # Calculer les indices de qualité
            form_f1 = calcul_formule_f1(df)
            form_f2, numerateur, denominateur = calcul_formule_f2(df)
            form_f3 = calcul_formule_f3(df)

            print("Calculs :")
            print("F1:", form_f1)
            print("F2:", form_f2, "Numerateur:", numerateur, "Dénominateur:", denominateur)
            print("F3:", form_f3)
            
            # Calculer l'indice de qualité
            indice_qualite = 100 - np.sqrt(pow(form_f1, 2) + pow(form_f2, 2) + pow(form_f3, 2)) / 1.732

            # Interpréter l'indice de qualité
            interpretation = self.interpreter_indice_qualite(indice_qualite)

            results = {
                'F1': round(form_f1, 2),
                'F2': round(form_f2, 2),
                'F3': round(form_f3, 2),
                'IQE': round(indice_qualite, 2),
            }

            uploaded_instance = UploadedFile.objects.create(
                user=request.user,
                file=uploaded_file,
                norme=norme_type,
                results=results
            )

            return JsonResponse({
                'results': results,
                'interpretation': interpretation
            })
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
        
    def lire_fichier(self, uploaded_file):
        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Read the file based on its type
        if file_extension == 'csv':
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='latin-1')
            except pd.errors.EmptyDataError:
                raise ValueError('Le fichier CSV est vide ou mal formaté.')

        elif file_extension in ['xls', 'xlsx']:
            try:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            except ImportError:
                raise ValueError('Veuillez installer openpyxl pour traiter les fichiers Excel.')

        elif file_extension == 'json':
            try:
                df = pd.read_json(uploaded_file)
            except ValueError:
                raise ValueError('Le fichier JSON est mal formaté.')

        else:
            raise ValueError('Format de fichier non pris en charge.')

        # Récupérer les paramètres de la base de données pour la norme
        norme_type = self.request.POST.get('norme')
        norme = Norme.objects.get(id_norme=norme_type)
        norme_parametres = NormeParametres.objects.filter(norme=norme)

        # Définir les types attendus pour chaque paramètre
        types_attendus = {
            'TDs': int, 'NO2-': float, 'NO3': int, 'NH4+': int, 'DBO5': int,
            'pH': float, 'DO': int, 'PO4-': float, 'PT': float, 'SO4': int,
            'NTK': int, 'Hg': int, 'Pb': int, 'Cd': int, 'As': int,
            'Cu': int, 'Mn': float, 'Fe': int, 'Zn': int, 'E.coli': int,
            'Enterocoque': int, 'Aldicarbe': int, 'Simazine': int, 'Désisopropylatratzine': int
        }

        # Récupérer les en-têtes du fichier
        headers = df.columns.tolist()
        print(headers)

        # Créer un dictionnaire des valeurs indicatrices avec les types corrects
        valeurs_normes = {}
        for parametre in norme_parametres:
            libelle = parametre.parametre.libelle
            valeur = parametre.valeurs_indicatrices
            if libelle in headers:  # Check if the parameter name is in the headers
                if libelle in types_attendus:
                    valeurs_normes[libelle] = types_attendus[libelle](float(valeur))
                else:
                    valeurs_normes[libelle] = float(valeur)

        # Corriger le nom 'Enterocoque' si nécessaire
        if 'Enterocoque' in valeurs_normes and 'Enterucoque' not in valeurs_normes:
            valeurs_normes['Enterucoque'] = valeurs_normes.pop('Enterocoque')

        # Convertir le dictionnaire en DataFrame et concaténer
        dernier_df = pd.DataFrame([valeurs_normes])
        df = pd.concat([df, dernier_df], ignore_index=True)

        print(df.tail(5))

        return df
            
    def interpreter_indice_qualite(self, indice_qualite):
     if indice_qualite >= 95:
        return ("Excellente : L'eau est très propre et convient à toutes les utilisations, "
                "y compris la consommation humaine, la baignade et l'irrigation.")
     elif indice_qualite >= 80:
        return ("Bonne : La qualité de l'eau est adéquate pour la plupart des usages, "
                "bien qu'elle puisse nécessiter un léger traitement pour la consommation.")
     elif indice_qualite >= 65:
        return ("Moyenne : La qualité de l'eau est acceptable, mais il est conseillé "
                "de la traiter avant de l'utiliser pour boire ou pour des activités sensibles.")
     elif indice_qualite >= 45:
        return ("Médiocre : La qualité de l'eau est marginale, ce qui signifie qu'elle peut "
                "présenter des risques pour la santé et devrait être utilisée avec précaution.")
     else:
        return ("Mauvais : L'eau est fortement polluée et n'est pas sûre pour la consommation, "
                "la baignade ou d'autres usages. Des mesures de traitement sont nécessaires.")
        
    # def comparer_et_calculer(self, df, norme):
    #     resultats = {}
    #     norme_parametres = NormeParametres.objects.filter(norme=norme)

    #     # Créer un dictionnaire des valeurs indicatrices pour un accès rapide
    #     valeurs_normes = {param.parametre.libelle: param.valeurs_indicatrices for param in norme_parametres}

    #     for _, row in df.iterrows():
    #         for parametre, valeur in row.items():
    #             # Vérifiez si le paramètre existe dans les normes
    #             if parametre in valeurs_normes:
    #                 valeur_norme = valeurs_normes[parametre]
                    
    #                 # Gérer les valeurs négatives
    #                 if valeur < 0:
    #                     resultats[parametre] = {
    #                         'valeur': valeur,
    #                         'norme': valeur_norme,
    #                         'resultat': 'Valeur non valide (négatif)'
    #                     }
    #                     continue
                    
    #                 # Effectuer les calculs selon les conditions
    #                 if valeur > valeur_norme:
    #                     resultat = calcul_formule_f1(valeur, valeur_norme)
    #                 elif valeur == valeur_norme:
    #                     resultat = calcul_formule_f2(valeur, valeur_norme)
    #                 else:
    #                     resultat = calcul_formule_f3(valeur, valeur_norme)
                    
    #                 resultats[parametre] = {
    #                     'valeur': valeur,
    #                     'norme': valeur_norme,
    #                     'resultat': resultat
    #                 }
    #             else:
    #                 resultats[parametre] = {
    #                     'valeur': valeur,
    #                     'norme': None,
    #                     'resultat': 'Paramètre non trouvé'
    #                 }
        
    #     return resultats

    # def calculer_indice_qualite(self, resultats):
    #     f1 = sum(r['resultat'] for r in resultats.values() if isinstance(r['resultat'], (int, float)) and r['valeur'] > r['norme'])
    #     f2 = sum(r['resultat'] for r in resultats.values() if isinstance(r['resultat'], (int, float)) and r['valeur'] == r['norme'])
    #     f3 = sum(r['resultat'] for r in resultats.values() if isinstance(r['resultat'], (int, float)) and r['valeur'] < r['norme'])
        
    #     return 100 - np.sqrt(pow(f1, 2) + pow(f2, 2) + pow(f3, 2)) / 1.732
