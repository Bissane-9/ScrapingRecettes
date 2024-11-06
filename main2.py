#ici je recupère juste les catégories de recettes du site
import requests
from bs4 import BeautifulSoup

# URL de la page d'accueil des catégories
url = "https://www.recettesafricaine.com/category/les-recettes-africaines/"

# faire une requête pour récupérer le contenu de la page
response = requests.get(url)

# vérifier que la requête a réussi
if response.status_code == 200:
    # parser(transformer un texte brut en une structure qu'on peut manipuler )le contenu HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # trouver le sous-menu contenant les catégories (trés important car si nous n'avons pas les bons élléments on ne va pas récuperer la bonne donnée)
    sous_menu = soup.find('ul', class_='sub-menu')

    # et là je ressors tous les liens de catégorie dans le sous-menu précédent
    categories = sous_menu.find_all('a', itemprop="url")

    # j'extrais les titres et les liens de chaque catégorie
    for category in categories:
        titre_categorie = category.find('span', itemprop="name").get_text().strip()
        lien_categorie = category['href']

        # affiche le titre et le lien des catégories
        print(f"Titre : {titre_categorie}")
        print(f"Lien : {lien_categorie}\n")
else:
    print(f"Erreur : Impossible d'accéder à la page. Status code {response.status_code}")



