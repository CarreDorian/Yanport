# importation de pandas pour gerer la BDD, et de sys pour pouvoir recuperer l'argument.

import pandas as pd
import sys

# fonction repondant à la problematique. Elle verifiera qu'il n'existe pas d'autres biens possedent les mêmes carracteristiques immuable (tel que le nombre de chambres...) pour reconnaître les mêmes biens. 

def find_same_property(ID_element):
    # dataset contiendra le document gsheet pour ensuite verifier que ID est contenue dedans
    
    dataset = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1XUjqeXVgjZJ8jVNAn9MeIb9zHLhVj4mwRs-hk1P050o/export?format=csv")
    
    no_ID = True
    for i in dataset['ID']:
        if i == ID_element:
            no_ID = False
        else:
            pass
    
    if no_ID:
        print("ID IMPORTER NON VALIDE")
        return 
    
    # On recupere les datas de la proprietee pour ensuite inserer un 0 dans les cases vide de la BDD que nous utiliserons
    
    cols = list(dataset.loc[dataset['ID'] == ID_element].columns.values)
    element = element[cols[3:35]].drop(columns=['DESCRIPTION', 'IMAGES'])

    for i in element:
        count = 0
        lst = []
        for j in dataset[i].isnull():
            if j:
                lst.append(0)
            else:
                lst.append(dataset[i][count])
            count+=1
        dataset[i] = lst[:]

    # On recupere les datas de la proprietee sans case vide 

    element = dataset.loc[dataset['ID'] == ID_element]
    cols = list(element.columns.values)
    element = element[cols[3:35]].drop(columns=['DESCRIPTION', 'IMAGES'])

    # On compare les valeurs de chaques colones immuable
    
    for i in element.columns:
        dataset = dataset.loc[dataset[i] == element[i].values[0]]

    # seul les ID (afin de retrouver le bien), les url (afin de retrouver le site de vente) et le nom des vendeurs seront retournes.

    cols = list(dataset.columns.values)
    dataset = dataset[[cols[0:3]]]
    return dataset



try:
    dataset = find_same_property(sys.argv[1])
    print(dataset)
except:
    print("ARGMENT OUBLIER")
    
    
# Mission accomplis 

# Cependant, mon algorithme ne prenant pas en compte l'adresse, il n'est pas totalement fiable. 
# En effet, deux biens ayant les mêmes carracteristiques seront associes.

# Voici donc mes pistes d'amelioration :

# prise en compte de l'adresse ;
# creatoin d'un cli dedie ;
# creation d'une interface presentant le bien ainsi que ces sites vendeurs, avec possibilite d'accede au lien du site revendeur en cliquant sur le fameux vendeur.