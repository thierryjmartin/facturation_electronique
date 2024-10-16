# Facturation Electronique SDK

## Description
`Facturation Electronique SDK` est une bibliothèque Python qui simplifie l'interaction avec les principales API de facturation électronique en France, notamment **Chorus Pro**, et d'autres partenaires privés. Elle supporte également le format **Factur-X** pour la création et l'envoi de factures électroniques.

Ce SDK est conçu pour être extensible et compatible avec les différentes plateformes de facturation électronique en France, facilitant l'envoi et la gestion des factures en toute conformité avec les réglementations.

## Fonctionnalités
- **Chorus Pro** : Création, envoi et suivi des factures à destination des entités publiques.
- **Factur-X** : Génération de factures au format PDF/Factur-X.

## Installation

1. Clonez ce dépôt ou téléchargez-le :

   ```bash
   git clone https://gitlab.com/cleverip/fr-efact-python-sdk.git
    ```
   
2. Installez les dépendances à l'aide du fichier requirements.txt :
   ```bash
   pip install -r requirements.txt
    ```
## Configuration

Vous devez fournir vos clés API et les URL des différentes plateformes dans un fichier de configuration ou via des variables d'environnement.

Exemple d'un fichier config.py :
   ```python
from .template_config import *


# Configuration API Chorus Pro
CHORUS_PRO_BASE_URL = 'https://chorus-pro.gouv.fr/api'
CHORUS_PRO_API_KEY = 'votre-api-key-chorus-pro'

# Configuration API DPGF
DPGF_BASE_URL = 'https://dpgf-partenaire.fr/api'
DPGF_API_KEY = 'votre-api-key-dpgf'

# Autres configurations...
   ```

## Utilisation

Voir le script api/chorus_pro.py

## Gestion des erreurs
La bibliothèque lève des exceptions personnalisées pour la gestion des erreurs spécifiques aux interactions avec les API de facturation. Voici un exemple :
```python
from facture_electronique.exceptions import FacturationAPIError

try:
	reponse = chorus_pro.envoyer_facture(facture)
except FacturationAPIError as e:
	print(f"Erreur lors de l'envoi de la facture: {e}")
   ```

## Contribution
Si vous souhaitez contribuer à ce projet, veuillez suivre les étapes suivantes :

    Clonez le dépôt.
    Créez une branche pour votre fonctionnalité : git checkout -b nouvelle-fonctionnalité.
    Faites vos modifications et testez-les.
    Soumettez une pull request.

## Licence
Ce projet est sous licence MIT.

## Auteur
Developpé par Thierry Martin