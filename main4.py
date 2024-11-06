#ici je recupère à partir de toutes les catégories les recettes de  chaque catégorie et j'ai aussi le nombre total de recettes
import requests
from bs4 import BeautifulSoup
import time

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

                # ajouter la recette à la liste
                toutes_les_recettes.append({
                    'categorie': titre_categorie,
                    'titre': titre_recette,
                    'lien': lien_recette
                })

            # pause pour éviter de surcharger le serveur
            time.sleep(1)

    # affiche les recettes collectées
    print("Toutes les recettes collectées :\n")
    for recette in toutes_les_recettes:
        print(f"Catégorie : {recette['categorie']}")
        print(f"Titre : {recette['titre']}")
        print(f"Lien : {recette['lien']}\n")
    print(f"Nombre total de recettes collectées : {len(toutes_les_recettes)}")
else:
    print(f"Erreur : Impossible d'accéder à la page d'accueil. Status code {response.status_code}")
