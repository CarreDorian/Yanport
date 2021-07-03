# import the pandas lybrary for BDD, nunpy to get nan (empty element)

import pandas as pd
from copy import copy
from numpy import nan

to_drop = ['ID', 'URL', 'CRAWL_SOURCE', 'IMAGES', 'MARKETING_TYPE', 'PRICE', 'PRICE_M2', 'PRICE_EVENTS', 'RENTAL_EXPENSES', 'RENTAL_EXPENSES_INCLUDED', 'DEPOSIT', 'FEES', 'FEES_INCLUDED', 'EXCLUSIVE_MANDATE', 'DEALER_NAME', 'DEALER_TYPE', 'AGENCIES_UNWANTED', 'EXCLUSIVE_MANDATE', 'PUBLICATION_END_DATE', 'PUBLICATION_START_DATE', 'LAST_CRAWL_DATE', 'LAST_PRICE_DECREASE_DATE']

# function reseaching oversproperty whith the same carractèristics (like the number of room) to see who's the same one. The changing characteristics (like the seller) define in the varriable "to_drop" are excluded from the comparing.
def find_same_property(dataset, to_start = 1, to_drop = []):
    
    # we're taking the data to compare.
    element = dataset.loc[dataset.index == to_start-1]
    element = element.drop(to_drop, axis=1)

    # we're comparing the data.
    for i in element.columns:
        dataset = dataset.loc[dataset[i] == element[i].values[0]]
        if len(dataset) < 2:
            break

    return dataset

try:
    # we take the database, to insert a 0 in the empty element. Thanks to that, we can compare the empty element.
    BDD = pd.read_csv(f"https://docs.google.com/spreadsheets/d/1XUjqeXVgjZJ8jVNAn9MeIb9zHLhVj4mwRs-hk1P050o/export?format=csv")
    BDD = BDD.fillna(0)
    
    i = 0
    
    # we are researching the same emement. If they are more of one, we concatanate them in the first one.
    while i < len(BDD)-1:
        
        element = find_same_property(BDD [i:], i+1, to_drop)
        if len(element) > 1:
            
            # we reset the index to be shure that they are no missing index. We conserve the original index
            element.reset_index(inplace=True)
            index = []
            for x in element['index']:
                index.append(x)
            element = element.drop('index', axis=1)
            
            # On condence the same property in one.
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
                        
            # we delate the useless information.
            for drop in index[1:]:
                BDD = BDD.drop(drop)
            BDD.reset_index(inplace=True, drop=True)
        # next test.
        i += 1
    
    # we reverse fillna and we save de data.
    BDD = BDD.replace(0, nan)
    try:
        BDD.to_excel('Dataset - Ads - Biens Regroupés - Levallois-Perret - 2019-08.xlsx', index=False)
        print('Donnes telecharges dans un fichier nomme : "Dataset - Ads - Biens Regroupés - Levallois-Perret - 2019-08.xlsx"')
    except:
        print("Erreur de telechargement")
except:
    print("La connextion a la database a echoue")

    
    
# Mission accomplished  

# This is my areas for improvement :

# let the choice of the document name to the user, and ask him a validation before erase a document ;
# make the link containe in the functional clickable list ;
# optimisation (7,40s pour ce programme) ;
# memory optimisation ;
# creation of a dedicated cli ;
# conservation of more data ;
# creation of an interface who're gonna showing the property and he's sellers, with possibility of acces to the sellers's internet page by the link.
