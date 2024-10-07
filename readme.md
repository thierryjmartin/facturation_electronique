# Facturation Electronique SDK

## Description
`Facturation Electronique SDK` est une bibliothèque Python qui simplifie l'interaction avec les principales API de facturation électronique en France, notamment **Chorus Pro**, **DPGF**, et d'autres partenaires privés. Elle supporte également le format **Factur-X** pour la création et l'envoi de factures électroniques, ainsi que la gestion des signatures électroniques.

Ce SDK est conçu pour être extensible et compatible avec les différentes plateformes de facturation électronique en France, facilitant l'envoi et la gestion des factures en toute conformité avec les réglementations.

## Fonctionnalités
- **Chorus Pro** : Création, envoi et suivi des factures à destination des entités publiques.
- **DPGF** : Gestion des factures électroniques entre entreprises privées.
- **JeDéclare** : Envoi de factures via EDI.
- **Factur-X** : Génération de factures au format PDF/Factur-X.
- **Signature électronique** : Gestion des signatures électroniques sur les documents (optionnel).

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
# Configuration API Chorus Pro
CHORUS_PRO_BASE_URL = 'https://chorus-pro.gouv.fr/api'
CHORUS_PRO_API_KEY = 'votre-api-key-chorus-pro'

# Configuration API DPGF
DPGF_BASE_URL = 'https://dpgf-partenaire.fr/api'
DPGF_API_KEY = 'votre-api-key-dpgf'

# Autres configurations...
   ```

## Utilisation
1. Envoi d'une facture à Chorus Pro

Voici un exemple simple pour envoyer une facture à Chorus Pro.
   ```python
from facturation_electronique.api.chorus_pro import ChorusProAPI

api_key = "votre-api-key-chorus-pro"
chorus_pro = ChorusProAPI(api_key)

facture = {
	"facture_id": "12345",
	"client": {
		"nom": "Client Externe",
		"adresse": "12 Rue Externe, 75000 Paris"
	},
	"montant_total": 1000.50,
	# autres détails...
}

# Envoi de la facture
reponse = chorus_pro.envoyer_facture(facture)
print(reponse)
   ```

2. Générer une facture au format Factur-X
   
```python
from facturation_electronique.utils.facturx import creer_facturx

facture_data = {
	"facture_id": "INV-2023-001",
	"client": {
		"nom": "Entreprise XYZ",
		"adresse": "15 Rue Principale, 75001 Paris"
	},
	"montant_total": 1500.00,
	# autres informations
}

pdf_path = "facture_base.pdf"
facturx_pdf = creer_facturx(facture_data, pdf_path)

print(f"Facture Factur-X générée: {facturx_pdf}")
   ```

3. Récupérer le statut d'une facture sur DPGF

```python
from facturation_electronique.api.dpgf import DPGFAPI

api_key = "votre-api-key-dpgf"
dpgf = DPGFAPI(api_key)

facture_id = "12345"
statut = dpgf.obtenir_statut_facture(facture_id)
print(statut)
   ```

## Gestion des erreurs
La bibliothèque lève des exceptions personnalisées pour la gestion des erreurs spécifiques aux interactions avec les API de facturation. Voici un exemple :
```python
from facturation_electronique.exceptions import FacturationAPIError

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