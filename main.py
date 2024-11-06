import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL de base pour accéder aux recettes
base_url = "https://www.recettesafricaine.com/category/les-recettes-africaines/page/{}/"
recettes = []
max_recettes = 100  # Nombre de recettes souhaité
page = 1  # Commencer par la première page

while len(recettes) < max_recettes:
    # Requête sur la page de recettes
    url = base_url.format(page)
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code != 200:
        print(f"Erreur lors de l'accès à la page {page}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver les blocs de recettes
    recette_elements = soup.find_all('article')  # Modifier si le sélecteur est différent

    for element in recette_elements:
        if len(recettes) >= max_recettes:
            break

        # Extraire le titre de la recette
        titre = element.find('h2').get_text().strip()

        # Extraire le lien de la recette
        lien = element.find('a')['href']

        # Requête sur la page de la recette pour extraire les détails
        recette_page = requests.get(lien)
        recette_soup = BeautifulSoup(recette_page.text, 'html.parser')

        # Extraire les ingrédients et instructions (à adapter selon le site)
        ingredients = recette_soup.find('div', class_='ingredients').get_text(strip=True) if recette_soup.find('div',
                                                                                                               class_='ingredients') else "N/A"
        instructions = recette_soup.find('div', class_='instructions').get_text(strip=True) if recette_soup.find('div',
                                                                                                                 class_='instructions') else "N/A"

        # Ajouter les informations de la recette dans la liste
        recettes.append({
            'titre': titre,
            'lien': lien,
            'ingredients': ingredients,
            'instructions': instructions
        })

    # Passer à la page suivante et attendre un moment pour ne pas surcharger le site
    page += 1
    time.sleep(1)  # Attente de 1 seconde entre les requêtes

# Sauvegarder les recettes dans un fichier CSV
df = pd.DataFrame(recettes)
df.to_csv('recettes_africaines.csv', index=False)
print("Scraping terminé et données sauvegardées dans 'recettes_africaines.csv'")
