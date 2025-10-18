# Facturation Electronique SDK

[![CI - Tests Python](https://github.com/thierryjmartin/facturation_electronique/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/thierryjmartin/facturation_electronique/actions/workflows/ci-tests.yml)
[![codecov](https://codecov.io/github/thierryjmartin/facturation_electronique/graph/badge.svg?token=TCWSSLACFQ)](https://codecov.io/github/thierryjmartin/facturation_electronique)
[![PyPI version](https://badge.fury.io/py/facture-electronique.svg)](https://badge.fury.io/py/facture-electronique)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/facture-electronique)](https://pypi.org/project/facture-electronique/)
[![GitHub license](https://img.shields.io/github/license/thierryjmartin/facturation_electronique)](https://github.com/thierryjmartin/facturation_electronique/blob/main/LICENSE)

## Description
`Facturation Electronique` est une bibliothèque Python complète conçue pour simplifier l'interaction avec les principales API de facturation électronique en France, notamment **Chorus Pro** et d'autres Plateformes de Dématérialisation Partenaires (PDP). Elle offre une approche robuste pour la création, la validation et l'envoi de factures électroniques conformes au standard **Factur-X**.

Contrairement à la bibliothèque `factur-x` qui fournit les structures de données XML brutes, ce SDK se positionne comme une surcouche intelligente. Il vous permet de manipuler vos données de facture via des **modèles Pydantic intuitifs et validés**, puis d'orchestrer leur conversion en XML Factur-X et leur soumission aux plateformes requises.

## Fonctionnalités
- **Modélisation et Validation des Données (Pydantic)** :
  - Définissez vos factures avec des modèles Pydantic riches, typés et auto-validés.
  - Bénéficiez d'une validation automatique des types, formats et contraintes métier (ex: montants positifs) dès la saisie de vos données, bien avant la génération du XML.
- **Génération Factur-X Complète** :
  - Créez des factures au format PDF/A-3 avec XML embarqué, supportant les profils MINIMUM, BASIC, EN16931, EXTENDED.
  - **API Fluide et Simplifiée** : La génération de Factur-X est désormais orchestrée via une API fluide et intuitive, permettant de chaîner les étapes de validation, d'intégration PDF/A et d'enregistrement en un seul appel.
  - **Conformité PDF/A-3** : Le module assure la génération de documents PDF/A-3, un format d'archivage à long terme qui permet l'intégration du fichier XML Factur-X directement dans le PDF. Cette conformité est essentielle pour l'interopérabilité et la validité légale des factures électroniques.
  - **Signature Électronique** : Intégrez des signatures électroniques qualifiées (e-Seal) à vos documents PDF/A-3, garantissant l'authenticité et l'intégrité de vos factures.
  - **Validation Multi-couches** :
    - **Validation Pydantic** : Assure l'intégrité de vos données d'entrée.
    - **Validation de Règles Métier** : Des contrôles spécifiques aux profils Factur-X (ex: interdiction de remises globales TTC pour le profil BASIC) sont appliqués.
    - **Validation Schematron (`valider_xml_facturx_schematron`)** : Une validation approfondie du XML généré contre les règles métier officielles de Factur-X, utilisant XSLT et `saxonche`. Cette étape cruciale garantit la conformité de votre facture aux exigences les plus strictes, allant au-delà de la simple validation de schéma XML (XSD).
- **Intégrations API Robustes** :
  - **Chorus Pro** : Gérez le cycle de vie complet de vos factures (création, envoi, suivi de statut, ajout de pièces jointes) via un client API dédié, avec gestion de l'authentification OAuth2.
  - **Autres PDP** : Des clients API pour d'autres plateformes (ex: Pennylane, Sage) sont également inclus pour une interopérabilité étendue.

## Ressources

Pour vous aider à démarrer et à utiliser ce projet, voici les ressources essentielles :

- 📖 **Documentation Complète** : Explorez le guide complet, les tutoriels et la référence de l'API.
  - **https://thierryjmartin.github.io/facturation_electronique/**
- 📦 **Paquet PyPI** : Installez la dernière version stable directement depuis le Python Package Index.
  - **https://pypi.org/project/facture-electronique/**

## Installation

Le paquet est disponible sur PyPI :
```bash
pip install facture-electronique
```

Pour le développement, clonez le dépôt et installez les dépendances :
```bash
git clone https://github.com/thierryjmartin/facturation_electronique.git
cd facturation_electronique
pip install -r requirements-dev.txt
```

## Configuration

Les interactions avec les API (comme Chorus Pro) nécessitent des identifiants. Cette bibliothèque se configure via des **variables d'environnement**.

Pour le développement local, copiez le fichier `.env.example` en `.env` à la racine de votre projet, puis remplissez les valeurs :

```bash
cp .env.example .env
```
N'oubliez pas d'ajouter le fichier `.env` à votre `.gitignore`.

Les classes API, comme `ChorusProAPI`, liront automatiquement ces variables. Vous pouvez également les fournir explicitement lors de l'instanciation.


## Construire une Adresse Électronique (Recommandé)

La norme de facturation électronique française (AFNOR XP Z12-014) définit des formats d'adressage précis basés sur le SIREN, comme `SIREN_SIRET` ou `SIREN_SIRET_CODEROUTAGE`. Pour simplifier la création de ces identifiants et éviter les erreurs, la bibliothèque fournit un constructeur dédié : `ConstructeurAdresse`.

L'utilisation de ce "builder" est la méthode recommandée pour garantir la conformité de vos adresses.

```python
from facture_electronique.models import ConstructeurAdresse, AdresseElectronique, SchemeID

# Cas 1 : Adresse simple avec SIREN
adresse_simple = ConstructeurAdresse(siren="123456789").construire()
# -> identifiant = "123456789"

# Cas 2 : Adresse avec SIRET pour un établissement
adresse_etablissement = ConstructeurAdresse(siren="123456789").avec_siret("12345678901234").construire()
# -> identifiant = "123456789_12345678901234"

# Cas 3 : Adresse avec un code de routage pour un service public
adresse_service = (
    ConstructeurAdresse(siren="123456789")
    .avec_siret("12345678901234")
    .avec_code_routage("SERVICE01")
    .construire()
)
# -> identifiant = "123456789_12345678901234_SERVICE01"

# Il reste possible de créer une adresse manuellement (non recommandé pour les cas complexes)
adresse_manuelle = AdresseElectronique(identifiant="123456789", scheme_id=SchemeID.FR_SIREN)
```

## Utilisation

Voici des exemples simples pour les cas d'usage les plus courants. Pour des scénarios plus avancés (tous les profils Factur-X, signature, envoi de PDF...), consultez le fichier `facture_electronique/exemples/exemple_decoupe.py`.

### Exemple 1 : Générer une facture au format Factur-X

Cet exemple montre comment créer une facture simple et la sauvegarder en tant que fichier PDF contenant un XML Factur-X au profil `EN16931`.

```python
from decimal import Decimal
from facture_electronique.models import (
    FactureFacturX, ModeDepot, Destinataire, Fournisseur, CadreDeFacturation,
    CodeCadreFacturation, References, TypeFacture, TypeTVA, ModePaiement,
    LigneDePoste, LigneDeTVA, MontantTotal, AdresseElectronique, SchemeID
)
from facture_electronique.utils.facturx import ProfilFacturX
from facture_electronique.utils.files import get_absolute_path

# 1. Définir les données de la facture avec les modèles Pydantic
facture_simple = FactureFacturX(
    mode_depot=ModeDepot.DEPOT_PDF_API,
    numero_facture="F2025-001",
    date_echeance_paiement="2025-11-17",
    destinataire=Destinataire(
        adresse_electronique=AdresseElectronique(
            identifiant="12345678901234", scheme_id=SchemeID.FR_SIREN
        )
    ),
    fournisseur=Fournisseur(
        adresse_electronique=AdresseElectronique(
            identifiant="11122233300011", scheme_id=SchemeID.FR_SIREN
        ),
        id_fournisseur=12345,  # ID Chorus Pro du fournisseur (fictif ici)
        numero_tva_intra="FR12111222333",
    ),
    cadre_de_facturation=CadreDeFacturation(
        code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
    ),
    references=References(
        type_facture=TypeFacture.FACTURE,
        type_tva=TypeTVA.SUR_DEBIT,
        mode_paiement=ModePaiement.VIREMENT,
    ),
    lignes_de_poste=[
        LigneDePoste(
            numero=1,
            denomination="Prestation de conseil",
            quantite=Decimal("1"),
            unite="pce",  # pièce
            montant_unitaire_ht=Decimal("100.00"),
            taux_tva_manuel=Decimal("20.0"),
        )
    ],
    lignes_de_tva=[
        LigneDeTVA(
            montant_base_ht=Decimal("100.00"),
            montant_tva=Decimal("20.00"),
            taux_manuel=Decimal("20.0"),
        )
    ],
    montant_total=MontantTotal(
        montant_ht_total=Decimal("100.00"),
        montant_tva=Decimal("20.00"),
        montant_ttc_total=Decimal("120.00"),
        montant_a_payer=Decimal("120.00"),
    ),
)

# 2. Utiliser l'API fluide pour générer le fichier
# Un PDF source est requis pour y intégrer le XML.
chemin_pdf_source = get_absolute_path("facture_electronique/exemples/dummy.pdf")
nom_fichier_sortie = "facture_simple_en16931.pdf"

try:
    with facture_simple.generer_facturx(profil=ProfilFacturX.EN16931) as constructeur:
        resultat = (
            constructeur.valider_conformite()
            .integrer_dans_pdfa(chemin_pdf_source)
            .enregistrer_sous(nom_fichier_sortie)
        )
    print(f"Facture Factur-X générée avec succès : {resultat['chemin_fichier']}")
except Exception as e:
    print(f"Erreur lors de la génération Factur-X : {e}")
```

### Exemple 2 : Envoyer une facture à Chorus Pro (mode API)

Cet exemple montre comment envoyer les données d'une facture directement à l'API de Chorus Pro (`SAISIE_API`), sans générer de fichier PDF.

```python
from decimal import Decimal
from facture_electronique.api.chorus_pro import ChorusProAPI
from facture_electronique.models import (
    FactureChorus, ModeDepot, Destinataire, Fournisseur, CadreDeFacturation,
    CodeCadreFacturation, References, TypeFacture, TypeTVA, ModePaiement,
    LigneDePoste, LigneDeTVA, MontantTotal, AdresseElectronique, SchemeID
)

# 1. Initialiser le client API (en mode sandbox)
# Assurez-vous que vos identifiants sont dans les variables d'environnement
# (PISTE_CLIENT_ID, PISTE_CLIENT_SECRET, CHORUS_PRO_LOGIN, CHORUS_PRO_PASSWORD)
try:
    client_chorus = ChorusProAPI(sandbox=True)
except Exception as e:
    print(f"Erreur d'initialisation du client API : {e}")
    # Dans un vrai scénario, on arrêterait ici.
    # Pour l'exemple, on continue sans client fonctionnel.
    client_chorus = None

# 2. Définir les données de la facture pour le mode SAISIE_API
facture_api = FactureChorus(
    mode_depot=ModeDepot.SAISIE_API,
    numero_facture="API-2025-001",
    destinataire=Destinataire(
        adresse_electronique=AdresseElectronique(
            identifiant="12345678901234", scheme_id=SchemeID.FR_SIREN
        )
    ),  # SIRET du client public
    fournisseur=Fournisseur(
        id_fournisseur=12345,  # Votre ID technique Chorus Pro
        adresse_electronique=AdresseElectronique(
            identifiant="11122233300011", scheme_id=SchemeID.FR_SIREN
        ),
    ),
    cadre_de_facturation=CadreDeFacturation(
        code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
    ),
    references=References(
        type_facture=TypeFacture.FACTURE,
        type_tva=TypeTVA.SUR_DEBIT,
        mode_paiement=ModePaiement.VIREMENT,
    ),
    lignes_de_poste=[
        LigneDePoste(
            numero=1,
            denomination="Fournitures de bureau",
            quantite=Decimal("1"),
            unite="lot",
            montant_unitaire_ht=Decimal("75.50"),
            taux_tva_manuel=Decimal("20.0"),
        )
    ],
    lignes_de_tva=[
        LigneDeTVA(
            montant_base_ht=Decimal("75.50"),
            montant_tva=Decimal("15.10"),
            taux_manuel=Decimal("20.0"),
        )
    ],
    montant_total=MontantTotal(
        montant_ht_total=Decimal("75.50"),
        montant_tva=Decimal("15.10"),
        montant_ttc_total=Decimal("90.60"),
        montant_a_payer=Decimal("90.60"),
    ),
    commentaire="Facture simple envoyée via API"
)

# 3. Préparer et envoyer la facture
# L'envoi réel est commenté car il nécessite des identifiants valides.
if client_chorus:
    try:
        payload = facture_api.to_api_payload()
        print("Payload généré pour l'API Chorus Pro.")
        # print(payload) # Décommentez pour voir le payload

        # --- Décommentez la ligne suivante pour envoyer la facture ---
        # reponse = client_chorus.envoyer_facture(payload)
        # print(f"Facture envoyée avec succès ! ID Chorus Pro : {reponse.get('identifiantFactureCPP')}")

        print("\nL'envoi réel est commenté. Décommentez le code pour l'activer.")

    except Exception as e:
        print(f"Erreur lors de la préparation ou de l'envoi de la facture : {e}")

```

## Petite note technique
Le code dans le répertoire `generated` est généré à partir des schémas XSD officiels de Factur-X à l'aide de la commande `xsdata`:
```bash
xsdata generate xsd/facturx-minimum/Factur-X_1.07.2_MINIMUM.xsd
```

## Contribution
Les contributions sont les bienvenues ! Veuillez cloner le dépôt, créer une branche et soumettre une Pull Request.

## Licence
Ce projet est sous licence MIT.

## Auteur
Développé par Thierry Martin

## Changelog

### 0.6.0 (17 octobre 2025)
- **Nouvelle fonctionnalité** : Ajout du support pour le profil Factur-X EXTENDED.
- **Changement d'API (potentiellement non rétrocompatible)** : La fonction `valider_xml_xldt` a été renommée en `valider_xml_facturx_schematron` dans `facture_electronique/utils/facturx.py` pour une meilleure clarté et cohérence.

### 0.5.9
- Mise à jour pour le support de Factur-X 1.0.7.3.

### 0.5.8
- **Fix** : Correction d'un bug qui empêchait l'exception `XSLTValidationError` d'être interceptée (`catch`). L'exception a été refactorisée pour accepter une liste d'erreurs, la rendant robuste et testable.

### 0.5.4
- maj API et tests.

### 0.5.3
- version plus robuste de validation des XML factur-X

### 0.5.2
- mise à jour de `__init__.py` de manière à exposer l'API.

### 0.5.0
- **Changement majeur (non rétrocompatible)** : Refonte complète de la gestion de la configuration pour les clients API.
  - Suppression du système fragile basé sur l'import d'un fichier `config.py` ou `template_config.py`.
  - La configuration se fait désormais via des **variables d'environnement** (recommandé) ou en passant les identifiants directement au constructeur de la classe API.
  - Introduction d'une nouvelle exception `ErreurConfiguration` levée lorsque des identifiants requis sont manquants.
  - Ajout d'un fichier `.env.example` pour guider les utilisateurs.
- **Documentation** : Mise à jour complète du `README.md` pour refléter la nouvelle méthode d'installation et de configuration.

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
- Ajout des XSD de factur-x au package, en particulier pour pouvoir utiliser utils.facturx.valider_xml_facturx_schematron plus facilement.

### 0.1.16
- Ajout d'exemple de code pour signer les PDFs avec PyHanko, car cela devrait être nécessaire pour faire des Factur-X (Qualified eSeal). Pour le moment la signature casse la validité PDF/A...

### 0.1.13
- Ajout de la génération de Factur-X EN16931 (en plus des profils Minimum et Basic).

### 0.1.12
- Mise à jour pour le support de Factur-X 1.0.7.2.
