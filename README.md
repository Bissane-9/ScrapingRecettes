# ScrapingRecettes
  Ce projet est un script de scraping conçu pour extraire des recettes africaines à partir du site Recettes Africaines. Le script récupère des informations telles que le titre de la recette, la catégorie, les ingrédients, et les instructions, et les sauvegarde dans un fichier JSON.

# Fonctionnalités
  -Extraction des catégories de recettes
  -Navigation dans les pages de chaque catégorie
  -Extraction des détails des recettes : titre, lien, ingrédients, instructions
  -Sauvegarde des données dans un fichier structuré JSON

# Prérequis
  Avant de commencer, assurez-vous d'avoir installé les éléments suivants :
  -Python 3.x
  -Les bibliothèques Python suivantes (que vous pouvez installer avec pip) :
    requests : pour faire des requêtes HTTP et récupérer le contenu des pages web
    BeautifulSoup4 : pour parser et extraire les informations du contenu HTML

# Installation
  Clonez ce dépôt sur votre machine locale puis accédez au répertoire du projet.

# Utilisation
  Exécutez le script pour commencer à scraper les recettes
Le script est configuré pour sauvegarder les données récupérées dans un fichier JSON.

# Structure des données extraites
  Les données extraites par le script comprennent les informations suivantes pour chaque recette :

  Catégorie : La catégorie de la recette (ex. "Beignets Africains").
  Titre : Le titre de la recette (ex. "Beignets de farine").
  Lien : Le lien URL de la recette.
  Ingrédients : La liste des ingrédients nécessaires pour la recette.
  Instructions : Les étapes à suivre pour préparer la recette.

# Exemple de sortie en format JSON
  [
  {
          "categorie": "Beignets Africains",
          "titre": "Recette de beignets de farine",
          "lien": "https://www.recettesafricaine.com/recette-de-beignets-de-farine.html",
          "ingredients": "250g de farine\n100 à 120 g de sucre\n10 g de levure boulangère\n200 à 250 ml d’eau tiède\nUne pincée de sel\nDe l’arôme au choix (vanille ou autres)\nHuile pour la friture",
          "instructions": "Mélanger ensemble la farine, le sucre, la pincée de sel et l’extrait de vanille, puis ajouter la levure et bien mélanger le tout ensemble.\nAjouter l’eau et bien battre la pâte avec un fouet ou des mains propres.\nPuis couvrir avec un torchon (ou couvercle) et laisser reposer pendant 45-60 min.\nLorsque la pâte double de volume, faire chauffer l’huile à température moyenne et former vos boules de pâte à l’aide d’une cuillère ou vos mains puis faire frire.\nRetirer et servir lorsque vos beignets sont bien dorés.\nServir et bonne dégustation !!!"
      }
      ]

# Notes importantes
  Ce script de scraping respecte les termes d'utilisation du site source. Assurez-vous de ne pas surcharger le serveur en ajoutant des pauses (comme time.sleep(1)) entre les requêtes.
Le scraping de données peut être soumis aux droits d'auteur et aux conditions d'utilisation du site web source. Utilisez ce script à des fins personnelles ou éducatives, et assurez-vous de respecter les droits d'auteur.
