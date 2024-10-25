# Facturation Electronique SDK

## Description
`Facturation Electronique` est une bibliothèque Python qui simplifie l'interaction avec les principales API de facturation électronique en France, notamment **Chorus Pro**, et d'autres partenaires privés. Elle supporte également le format **Factur-X** pour la création et l'envoi de factures électroniques.

Le concept repose sur l'instanciation d’une classe **Facture** (actuellement largement inspirée de l’API Chorus Pro), qui fournit ensuite les outils nécessaires pour interagir avec diverses API publiques, principalement Chorus Pro, ainsi qu’avec des plateformes de dématérialisation partenaires telles que Qonto, Sage, et Pennylane. La vérification de cohérence et de logique des factures s'appuie sur le format Factur-X, pris en charge par Chorus Pro, et particulièrement adapté pour les contrôles de cohérence avancés.

## Fonctionnalités
- **Chorus Pro** : Ce module permet la création, l'envoi et le suivi des factures destinées aux entités publiques. Il intègre également des fonctionnalités de recherche d’entités via le SIRET, permettant par exemple de retrouver l’identifiant Chorus Pro d’une entité.
- **Factur-X** : Ce module prend en charge la génération de factures au format PDF/Factur-X, en particulier les profils minimum et basic. Il valide le fichier factur-x.xml en conformité avec les schémas XSD via le module facturx. De plus, il offre la possibilité d'une validation plus poussée du fichier XML en appliquant les règles avancées définies dans les fichiers XSLT, ce que le module facturx ne propose pas nativement, via la fonction valider_xml_xslt.

## Installation

1. Clonez ce dépôt ou téléchargez-le :

   ```bash
   git clone https://github.com/thierryjmartin/facturation_electronique.git
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

## Contribution
Si vous souhaitez contribuer à ce projet, veuillez suivre les étapes suivantes :

    Clonez le dépôt.
    Créez une branche pour votre fonctionnalité : git checkout -b nouvelle-fonctionnalité.
    Faites vos modifications et testez-les.
    Soumettez une merge request.

## Licence
Ce projet est sous licence MIT.

## Auteur
Developpé par Thierry Martin