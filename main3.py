#ici je recupère à partir de la premiere catégorie beignets africains les recettes de  cette catégories
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
    premiere_categorie = sous_menu.find('a', itemprop="url")
    # et là je ressors le lien et le titre de la première catégorie ("Beignets Africains") dans le sous-menu
    titre_categorie = premiere_categorie.find('span', itemprop="name").get_text().strip()
    lien_categorie = premiere_categorie['href']

    print(f"Catégorie : {titre_categorie}")
    print(f"Lien de la catégorie de départ : {lien_categorie}\n")

    # pagination dans la catégorie car je me suis rendue compte que pour une catégorie on retrouve les reecettes sur plusieurs pages
    max_pages = 10  # limite pour éviter de boucler indéfiniment
    recettes = []

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
            print(f"Erreur : Impossible d'accéder à la page {page} de la catégorie.")
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
            recettes.append({
                'categorie': titre_categorie,
                'titre': titre_recette,
                'lien': lien_recette
            })

        # affiche les recettes collectées
        print(f"Recettes de la page {page} de la catégorie '{titre_categorie}':")
        for recette in recettes:
            print(f"Catégorie : {recette['categorie']}")
            print(f"Titre : {recette['titre']}")
            print(f"Lien : {recette['lien']}\n")

        # pause pour éviter de surcharger le serveur
        time.sleep(1)

else:
    print(f"Erreur : Impossible d'accéder à la page d'accueil. Status code {response.status_code}")
