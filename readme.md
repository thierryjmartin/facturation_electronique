# Facturation Electronique SDK

[![CI - Tests Python](https://github.com/thierryjmartin/facturation_electronique/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/thierryjmartin/facturation_electronique/actions/workflows/ci-tests.yml)
[![codecov](https://codecov.io/github/thierryjmartin/facturation_electronique/graph/badge.svg?token=TCWSSLACFQ)](https://codecov.io/github/thierryjmartin/facturation_electronique)
[![PyPI version](https://badge.fury.io/py/facture-electronique.svg)](https://badge.fury.io/py/facture-electronique)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/facture-electronique)](https://pypi.org/project/facture-electronique/)
[![GitHub license](https://img.shields.io/github/license/thierryjmartin/facturation_electronique)](https://github.com/thierryjmartin/facturation_electronique/blob/main/LICENSE)

## Description
`Facturation Electronique` est une bibliothèque Python qui simplifie l'interaction avec les principales API de facturation électronique en France, notamment **Chorus Pro**, et d'autres partenaires privés. Elle supporte également le format **Factur-X** pour la création et l'envoi de factures électroniques.

Le concept repose sur l'instanciation de classes Pydantic dédiées (`FactureChorus` et `FactureFacturX`), qui fournissent ensuite les outils nécessaires pour interagir avec diverses API publiques (Chorus Pro) et générer des factures conformes.

## Fonctionnalités
- **Chorus Pro** : Création, envoi et suivi des factures destinées aux entités publiques.
- **Factur-X** : Génération de factures au format PDF/A-3 avec XML embarqué (profils MINIMUM, BASIC, EN16931), avec des fonctions de validation avancées (XSD et Schematron).

## Installation

```bash
git clone https://github.com/thierryjmartin/facturation_electronique.git
cd facturation_electronique
pip install -r requirements.txt
```

## Utilisation

Voici un exemple rapide pour créer une facture destinée à l'API Chorus Pro et une autre au format Factur-X.

> Pour un exemple complet, consultez le fichier `facture_electronique/exemples/exemple_decoupe.py`.

```python
from facture_electronique.models import *

# 1. Créer une facture simple pour l'API Chorus Pro
facture_chorus = FactureChorus(
    mode_depot=ModeDepot.SAISIE_API,
    destinataire=Destinataire(code_destinataire="123456789"), # SIRET du client
    fournisseur=Fournisseur(id_fournisseur=9876), # Votre ID Chorus Pro
    cadre_de_facturation=CadreDeFacturation(code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR),
    references=References(
        type_facture=TypeFacture.FACTURE,
        type_tva=TypeTVA.SUR_DEBIT,
        mode_paiement=ModePaiement.VIREMENT,
    ),
    montant_total=MontantTotal(
        montant_ht_total=100.0,
        montant_tva=20.0,
        montant_ttc_total=120.0,
        montant_a_payer=120.0,
    ),
    lignes_de_poste=[LigneDePoste(numero=1, denomination="Test", quantite=1, unite="pce", montant_unitaire_ht=100.0)]
)

# Générer le payload JSON pour l'API
# payload = facture_chorus.to_api_payload()
# api.envoyer_facture(payload)


# 2. Créer une facture pour générer un fichier Factur-X
facture_fx = FactureFacturX(
    mode_depot=ModeDepot.DEPOT_PDF_API,
    numero_facture="FX-2024-001",
    date_facture="2024-10-18",
    date_echeance_paiement="2024-11-18",
    destinataire=Destinataire(
        code_destinataire="99986401570264",
        nom="Client Principal SA",
    ),
    fournisseur=Fournisseur(
        id_fournisseur=12345,
        siret="26073617692140",
        nom="Mon Entreprise SAS",
    ),
    cadre_de_facturation=CadreDeFacturation(code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR),
    references=References(
        type_facture=TypeFacture.FACTURE,
        type_tva=TypeTVA.SUR_DEBIT,
        mode_paiement=ModePaiement.VIREMENT,
    ),
    montant_total=MontantTotal(
        montant_ht_total=1000.0,
        montant_tva=200.0,
        montant_ttc_total=1200.0,
        montant_a_payer=1200.0,
    ),
    lignes_de_poste=[LigneDePoste(numero=1, denomination="Prestation", quantite=10, unite="heure", montant_unitaire_ht=100.0)]
)

# Générer le XML Factur-X (profil EN16931)
# xml_content = facture_fx.to_facturx_en16931()
# ... puis l'intégrer à un PDF pour obtenir la facture finale.
```

## Petite note technique
Le code dans generated est généré par cette commande qui convertit les xsd Factur-X en classes python :
   ```bash
 xsdata generate xsd/facturx-minimum/Factur-X_1.07.2_MINIMUM.xsd
```

## Contribution
Les contributions sont les bienvenues ! Veuillez cloner le dépôt, créer une branche et soumettre une Pull Request.

## Licence
Ce projet est sous licence MIT.

## Auteur
Developpé par Thierry Martin

## Changelog

### 0.4.0
- Gestion des dépendances centralisée via pyproject.toml

### 0.3.0
- Utilisation du type Decimal de préférence

### 0.2.1
- **Fix** : Correction de plusieurs `TypeError` dans la logique de génération Factur-X (`utils/facturx.py`) liés à la gestion des champs optionnels (`None`).
- **Tests** : Ajout d'une suite de tests dédiée (`tests/test_facturx.py`) pour la génération des factures Factur-X.

### 0.2.0
- Refactoring majeur des modèles de données (`Facture` -> `FactureChorus` / `FactureFacturX`).
- Harmonisation des noms de champs en français.
- Ajout de tests unitaires pour les modèles.
- Mise à jour de la documentation et des exemples.

### 0.1.24
- Modernisation de la gestion des dépendances avec `pip-tools`.

### 0.1.22
- Maj validation XML via Schematron

### 0.1.19
- Ajout des XSD de factur-x au package, en particulier pour pouvoir utiliser utils.facturx.valider_xml_xldt plus facilement.

### 0.1.16
- Ajout d'exemple de code pour signer les PDFs avec PyHanko, car cela devrait être nécessaire pour faire des Factur-X (Qualified eSeal). Pour le moment la signature casse la validité PDF/A...

### 0.1.13
- Ajout de la génération de Factur-X EN16931 (en plus des profils Minimum et Basic).

### 0.1.12
- Mise à jour pour le support de Factur-X 1.0.7.2.
