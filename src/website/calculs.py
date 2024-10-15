import pandas as pd
import numpy as np

try:
    import sys
except:
    print("This implementation requires the sys module.")
    exit(0)

#######################################################
# Fonction de progression (Voir fichier JAUGE.PY)
def update_progress(progress): 
    barLength = 10
    status = ""
    if isinstance(progress, int): 
        progress = float(progress) 
    if not isinstance(progress, float): 
        progress = 0 
        status = "error: progress var must be float\r\n" 
    if progress < 0: 
        progress = 0 
        status = "Halt...\r\n" 
    if progress >= 1: 
        progress = 1 
        status = "Done...\r\n" 
    block = int(round(barLength * progress)) 
    text = "\rPercent: [{0}] {1}% {2}".format("#" * block + "-" * (barLength - block), round(progress * 100, 3), status) 
    sys.stdout.write(text) 
    sys.stdout.flush()

##########################################################
def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return -1  # ou une autre valeur par défaut appropriée

def calcul_formule_f1(R1):
    form_f1 = 0
    nbre_var_depass_va_aut = 0
    nbre_var_tot = 0
    nbre_de_ligne = len(R1)
    
    for j in range(len(R1.columns)):
        nbre_var_tot += 1
        for i in range(len(R1) - 1):
            val = convert_to_float(R1.iloc[i, j])
            norm = convert_to_float(R1.iloc[nbre_de_ligne - 1, j])
            if val > -1 and norm != -1:
                if R1.columns[j] in ["DO", "pH"]:
                    if val < norm:
                        nbre_var_depass_va_aut += 1
                        break
                else:
                    if val > norm:
                        nbre_var_depass_va_aut += 1
                        break
    
    form_f1 = (nbre_var_depass_va_aut / nbre_var_tot) * 100
    return form_f1

def calcul_formule_f2(R1):
    form_f2 = 0
    nbre_var_depass_va_aut = 0
    nbre_var_tot = 0
    nbre_de_ligne = len(R1)
    
    for j in range(len(R1.columns)):
        for i in range(len(R1) - 1):
            val = convert_to_float(R1.iloc[i, j])
            norm = convert_to_float(R1.iloc[nbre_de_ligne - 1, j])
            if val > -1 and norm != -1:
                nbre_var_tot += 1
                if R1.columns[j] in ["DO", "pH"]:
                    if val < norm:
                        nbre_var_depass_va_aut += 1
                else:
                    if val > norm:
                        nbre_var_depass_va_aut += 1
                            
    form_f2 = (nbre_var_depass_va_aut / nbre_var_tot) * 100
    numerateur = nbre_var_depass_va_aut
    denominateur = nbre_var_tot
    return form_f2, numerateur, denominateur

def calcul_formule_f3(R1):
    form_f3 = 0
    nse = 0
    nbre_var_depass_va_aut = 0
    nbre_var_tot = 0
    nbre_de_ligne = len(R1)

    for j in range(len(R1.columns)):
        for i in range(len(R1) - 1):
            val = convert_to_float(R1.iloc[i, j])
            norm = convert_to_float(R1.iloc[nbre_de_ligne - 1, j])
            if val > -1 and norm != -1:
                nbre_var_tot += 1
                if R1.columns[j] in ["DO", "pH"]:
                    if val < norm:
                        nbre_var_depass_va_aut += (norm / val - 1)
                else:
                    if val > norm:
                        nbre_var_depass_va_aut += (val / norm - 1)
    
    nse = nbre_var_depass_va_aut / nbre_var_tot
    form_f3 = nse / (nse * 0.01 + 0.01)
    return form_f3

if __name__ == "__main__":
    R1 = pd.read_excel('iqe_doc.xlsx')
    
    form_f1 = calcul_formule_f1(R1)
    form_f2, numerateur, denominateur = calcul_formule_f2(R1)
    form_f3 = calcul_formule_f3(R1)
    
    indice_qualite = 100 - np.sqrt(pow(form_f1, 2) + pow(form_f2, 2) + pow(form_f3, 2)) / 1.732
    print("F1:", form_f1)
    print("F2:", form_f2)
    print("F3:", form_f3)
    print("IQE:", indice_qualite)
    