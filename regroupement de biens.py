# importation de pandas pour gerer la BDD, et de nan pour les valeurs absantes (nan = cases vide)

import pandas as pd
from copy import copy
from numpy import nan

to_drop = ['ID', 'URL', 'CRAWL_SOURCE', 'IMAGES', 'MARKETING_TYPE', 'PRICE', 'PRICE_M2', 'PRICE_EVENTS', 'RENTAL_EXPENSES', 'RENTAL_EXPENSES_INCLUDED', 'DEPOSIT', 'FEES', 'FEES_INCLUDED', 'EXCLUSIVE_MANDATE', 'DEALER_NAME', 'DEALER_TYPE', 'AGENCIES_UNWANTED', 'EXCLUSIVE_MANDATE', 'PUBLICATION_END_DATE', 'PUBLICATION_START_DATE', 'LAST_CRAWL_DATE', 'LAST_PRICE_DECREASE_DATE']

# fonction cherchant d'autres biens possédant les mêmes carracteristiques propre (tel que le nombre de chambres...) pour reconnaître les mêmes biens. Il sera mis de côté les carractéristiques changantes (tel que le vendeur) défini dans la varriable "to_drop".
def find_same_property(dataset, to_start = 1, to_drop = []):
    
    # On recupere les datas que nous allons comparer.
    element = dataset.loc[dataset.index == to_start-1]
    element = element.drop(to_drop, axis=1)

    # On compare ces valeurs.
    for i in element.columns:
        dataset = dataset.loc[dataset[i] == element[i].values[0]]
        if len(dataset) < 2:
            break

    return dataset

try:
    # On recupere la base de donnee, pour ensuite inserer un 0 dans les cases vide de la BDD.
    BDD = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1XUjqeXVgjZJ8jVNAn9MeIb9zHLhVj4mwRs-hk1P050o/export?format=csv")
    BDD = BDD.fillna(0)
    
    i = 0
    
    # On cherche les biens identiques.
    while i < len(BDD)-1:
        
        # Récupération des biens identiques, et si il y en as plus d'un, on les condences dans le premier bien.
        element = find_same_property(BDD [i:], i+1, to_drop)
        if len(element) > 1:
            
            # On réinicialise l'index pour ne pas avoir a chercher les biens tout en concervant leurs index d'origine.
            element.reset_index(inplace=True)
            index = []
            for x in element['index']:
                index.append(x)
            element = element.drop('index', axis=1)
            
            # On condence les informations dans un seul et même bien, si les informations sont différentes. Sinon, on ne conserve que les donnés déjà présentes.
            for multi_value in element.columns[:7]:
                BDD.at[i, multi_value] = [ copy(BDD[multi_value][index[0]]) ]
                for j in range(len(element[multi_value][:7])):
                    test = True
                    for k in range(len(BDD[multi_value][i])):
                        if BDD.at[i, multi_value] == BDD[multi_value][index[j]]:
                            test = False
                            break
                    if test:
                        BDD.at[i, multi_value].append(copy( BDD[multi_value][index[j]] ))
                        
            # On supprime les biens condencer devenu inutile. Cela évite également de les retester plus tard.
            for drop in index[1:]:
                BDD = BDD.drop(drop)
            BDD.reset_index(inplace=True, drop=True)
        # On passe au test de la donnée suivante.
        i += 1
    
    # On inverse fillna et on sauvegarde de la donnée:
    BDD = BDD.replace(0, nan)
    # Dataset\ -\ Ads\ -\ Biens\ Regroupés\ \/\ Levallois-Perret\ -\ 
    try:
        BDD.to_excel('Dataset - Ads - Biens Regroupés - Levallois-Perret -2019-08.xlsx', index=False)
        print('Donnes telecharges dans un fichier nomme : "Dataset - Ads - Biens Regroupés - Levallois-Perret -2019-08.xlsx"')
    except:
        print("Erreur de telechargement")
except:
    print("La connextion a la database a echoue")

    
    
# Mission accomplis 

# Cependant, mon algorithme ne prenant pas en compte l'adresse, il n'est pas totalement fiable. 
# En effet, les biens ayant les mêmes carracteristiques seront associes.

# Voici donc mes pistes d'amelioration :

# rendre les liens contenus dans les listes clicables fonctionnelles ;
# optimisation (7,40s pour ce programme). Une piste : remplacer les nan par 0 dans les cases que nous utilisons ;
# optimisation de la mémoire
# creatoin d'un cli dedie ;
# conservation de plus de data ;
# creation d'une interface presentant le bien ainsi que ces sites vendeurs, avec possibilite d'accede au lien du site revendeur en cliquant sur le fameux vendeur.