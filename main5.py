#ici je recupère à partir de tous les liens des recettes les ingrédients et instructions
import requests
from bs4 import BeautifulSoup
import time
import json

# URL de la page d'accueil des catégories
url = "https://www.recettesafricaine.com/category/les-recettes-africaines/"

# faire une requête pour récupérer le contenu de la page
response = requests.get(url)

# vérifier que la requête a réussi
if response.status_code == 200:
    # parser le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # trouver le sous-menu contenant les catégories
    sous_menu = soup.find('ul', class_='sub-menu')
    categories = sous_menu.find_all('a', itemprop="url")

    toutes_les_recettes = []

    # parcourir chaque catégorie
    for categorie in categories:
        titre_categorie = categorie.find('span', itemprop="name").get_text().strip()
        lien_categorie = categorie['href']

        #print(f"Catégorie : {titre_categorie}")
        #print(f"Lien de la catégorie : {lien_categorie}\n")

        # pagination dans la catégorie car je me suis rendue compte que pour une catégorie on retrouve les reecettes sur plusieurs pages
        max_pages = 10

        for page in range(1, max_pages + 1):
            # construire l'URL de la page actuelle car a la fin de chaque url on a le numéro de la page pour chaque page
            if page == 1:
                url_categorie_page = lien_categorie  # c'est l'URL de la première page directement
            else:
                url_categorie_page = f"{lien_categorie}/page/{page}"  # ajouter la pagination avec /page/{page} pour url des pages suivantes

            # faire une requête pour accéder à la page de la catégorie
            response_categorie = requests.get(url_categorie_page)

            # vérifier que la requête a réussi
            if response_categorie.status_code != 200:
                #print(f"Erreur : Impossible d'accéder à la page {page} de la catégorie '{titre_categorie}'.")
                break

            # parser le contenu HTML de la page de la catégorie
            soup_categorie = BeautifulSoup(response_categorie.text, 'html.parser')

            # trouve les blocs de recettes
            recette_elements = soup_categorie.find_all('h1', class_='entry-title')

            for element in recette_elements:
                # j'extrais le titre et le lien de chaque recette
                titre_recette = element.find('a', class_='entry-title-link').get_text().strip()
                lien_recette = element.find('a', class_='entry-title-link')['href']

                # accéder à la page de chaque recette pour extraire les détails
                response_recette = requests.get(lien_recette)
                soup_recette = BeautifulSoup(response_recette.text, 'html.parser')

                # j'extrais les ingrédients et instructions
                entry_content = soup_recette.find('div', class_='entry-content')
                ingredients = []
                instructions = []
                is_ingredient_section = False
                is_instruction_section = False

                # parcourir tous les paragraphes
                for p in entry_content.find_all('p'):
                    text = p.get_text().strip()

                    # Vérifier si le texte correspond à "Ingrédients" ou "Ingredients"
                    if "Ingrédients" in text or "Ingredients" in text or "Ingrédient" in text or "Ingredient" in text:
                        is_ingredient_section = True
                        is_instruction_section = False
                        continue

                    # Vérifier si le texte correspond à "Direction" pour les instructions
                    elif "Direction" in text or "Instructions"in text:
                        is_ingredient_section = False
                        is_instruction_section = True
                        continue

                    # Ajouter les ingrédients et instructions en fonction de la section
                    if is_ingredient_section:
                        ingredients.append(text)
                    elif is_instruction_section:
                        instructions.append(text)

                # Joindre les ingrédients et instructions en une seule chaîne avec des sauts de ligne
                ingredients_text = "\n".join(ingredients)
                instructions_text = "\n".join(instructions)

                # ajouter les informations de la recette à la liste
                toutes_les_recettes.append({
                    'categorie': titre_categorie,
                    'titre': titre_recette,
                    'lien': lien_recette,
                    'ingredients': ingredients_text,
                    'instructions': instructions_text
                })

                # pause pour éviter de surcharger le serveur
                time.sleep(1)

    # affiche les recettes collectées avec les ingrédients et instructions
    print("Toutes les recettes collectées :\n")
    for recette in toutes_les_recettes:
        print(f"Catégorie : {recette['categorie']}")
        print(f"Titre : {recette['titre']}")
        print(f"Lien : {recette['lien']}")
        print(f"Ingrédients : {recette['ingredients']}")
        print(f"Instructions : {recette['instructions']}\n")
    print(f"Nombre total de recettes collectées : {len(toutes_les_recettes)}")

else:
    print(f"Erreur : Impossible d'accéder à la page d'accueil. Status code {response.status_code}")

# je sauvegarde les recettes dans un fichier JSON car c'est plus flexible surtout qu'il s'agit des données plus complexes
with open("recettes.json", mode="w", encoding="utf-8") as file:
    json.dump(toutes_les_recettes, file, ensure_ascii=False, indent=4)

print("Les recettes ont été sauvegardées dans le fichier 'recettes.json'.")

#je conclus que je n'arrive pas avoir tous les ingrédients et les instructions car le site ne respecte pas la structure initiale du code html
#y'a des infos qui sont dans la balise p et d'autre la balise u et autres
