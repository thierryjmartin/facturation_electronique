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


## Utilisation

Voici un exemple rapide pour interagir avec l'API Chorus Pro et créer une facture au format Factur-X.

> Pour un exemple complet, consultez le fichier `facture_electronique/exemples/exemple_decoupe.py`.

```python
from decimal import Decimal

# --- Imports mis à jour ---
# On importe les modèles, l'API Chorus, et les utilitaires de bas niveau si besoin.
from facture_electronique.api.chorus_pro import ChorusProAPI
from facture_electronique.utils.files import get_absolute_path
from facture_electronique.models import (
	FactureFacturX,
	FactureChorus,
	ModeDepot,
	Destinataire,
	Fournisseur,
	CodeCadreFacturation,
	References,
	TypeFacture,
	CadreDeFacturation,
	TypeTVA,
	ModePaiement,
	LigneDePoste,
	LigneDeTVA,
	MontantTotal,
	CategorieTVA,
	AdressePostale,
	PieceJointePrincipale,  # Ajout pour la partie Chorus
)
# Le seul import nécessaire pour la génération Factur-X !
from facture_electronique.utils.facturx import ProfilFacturX

# 1. Utiliser l'API Chorus Pro

# a. Instancier le client API (lit la configuration depuis l'environnement)
# from facture_electronique.api.chorus_pro import ChorusProAPI
# from dotenv import load_dotenv
#
# # Charger les variables du fichier .env
# load_dotenv()
#
# client_chorus = ChorusProAPI(sandbox=True)

# b. Créer l'objet facture pour l'API
exemple_facture_mode_api = FactureChorus(
		mode_depot=ModeDepot("SAISIE_API"),
		id_utilisateur_courant=0,
		destinataire=Destinataire(code_destinataire="99986401570264", code_service_executant=""),
		fournisseur=Fournisseur(id_fournisseur=12345),
		cadre_de_facturation=CadreDeFacturation(code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR),
		references=References(devise_facture="EUR", type_facture=TypeFacture("FACTURE"),
						  type_tva=TypeTVA("TVA_SUR_DEBIT"), numero_marche="VABFM001",
						  mode_paiement=ModePaiement("ESPECE")),
		lignes_de_poste=[LigneDePoste(numero=1, reference="R1", denomination="D1", quantite=Decimal("10"), unite="lot",
								  montant_unitaire_ht=Decimal("50.00"), montant_remise_ht=Decimal("0"), taux_tva="",
								  taux_tva_manuel=Decimal("20")),
						 LigneDePoste(numero=2, reference="R2", denomination="D2", quantite=Decimal("12"), unite="Kg",
								  montant_unitaire_ht=Decimal("36.00"), montant_remise_ht=Decimal("0"), taux_tva="",
								  taux_tva_manuel=Decimal("2.1")),
						 LigneDePoste(numero=3, reference="R3", denomination="D3", quantite=Decimal("16"), unite="lot",
								  montant_unitaire_ht=Decimal("24.00"), montant_remise_ht=Decimal("0"), taux_tva="",
								  taux_tva_manuel=Decimal("5")),
						 LigneDePoste(numero=4, reference="XX", denomination="XX", quantite=Decimal("1"), unite="lot",
								  montant_unitaire_ht=Decimal("10.00"), montant_remise_ht=Decimal("0"), taux_tva="",
								  taux_tva_manuel=Decimal("20"))],
		lignes_de_tva=[LigneDeTVA(taux_manuel=Decimal("20"), taux=None, montant_base_ht=Decimal("510.00"),
								  montant_tva=Decimal("102.00")),
					   LigneDeTVA(taux_manuel=Decimal("2.1"), taux=None, montant_base_ht=Decimal("432.00"),
								  montant_tva=Decimal("9.072")),
					   LigneDeTVA(taux_manuel=Decimal("5"), taux=None, montant_base_ht=Decimal("384.00"),
								  montant_tva=Decimal("19.20"))],
		montant_total=MontantTotal(montant_ht_total=Decimal("1326.00"), montant_tva=Decimal("130.272"),
								   montant_ttc_total=Decimal("1406.272"), montant_remise_globale_ttc=Decimal("50.00"),
								   motif_remise_globale_ttc="Geste commercial", montant_a_payer=Decimal("1400.00")),
		commentaire="Création_VABF_SoumettreFacture",
	)

# c. Envoyer la facture via l'API
# payload = exemple_facture_mode_api.to_api_payload()
# client_chorus.envoyer_facture(payload)


# 2. Créer une facture pour générer un fichier Factur-X (API Fluide)

```python
# --- 2. Préparation des données de facture ---
# Les données de cet exemple sont corrigées pour être mathématiquement cohérentes.
exemple_facture_mode_pdf = FactureFacturX(
    mode_depot=ModeDepot("DEPOT_PDF_API"),
    numero_facture="20240000000000000110",
    date_facture="2024-10-18",
    date_echeance_paiement="2024-11-18",
    id_utilisateur_courant=0,
    destinataire=Destinataire(nom="acheteur 99986401570264", code_destinataire="99986401570264",
                              adresse_postale=AdressePostale(code_postal="122345",
                                                             ligne_un="adresse du destinataire", nom_ville="PARIS",
                                                             pays_code_iso="FR"), code_service_executant=""),
    fournisseur=Fournisseur(id_fournisseur=12345, nom="Fournisseur 26073617692140", siret="26073617692140",
                            numero_tva_intra="FR61529571234", iban="FR7630006000011234567890189",
                            adresse_postale=AdressePostale(code_postal="122345", ligne_un="2 rue de l andouillette",
                                                           nom_ville="PARIS", pays_code_iso="FR")),
    cadre_de_facturation=CadreDeFacturation(code_cadre_facturation=CodeCadreFacturation("A1_FACTURE_FOURNISSEUR")),
    references=References(devise_facture="EUR", type_facture=TypeFacture("FACTURE"),
                          type_tva=TypeTVA("TVA_SUR_DEBIT"), numero_marche="VABFM001", numero_bon_commande="coucou",
                          mode_paiement=ModePaiement("ESPECE")),

    # Les lignes de poste sont la source de vérité
    lignes_de_poste=[
        LigneDePoste(numero=1, reference="R1", denomination="D1", quantite=Decimal("10"), unite="lot",
                     montant_unitaire_ht=Decimal("50.00"), montant_remise_ht=Decimal("5"),
                     taux_tva_manuel=Decimal("20"), categorie_tva=CategorieTVA("S"),
                     raison_reduction="parce que je suis sympa"),
        LigneDePoste(numero=2, reference="R2", denomination="D2", quantite=Decimal("12"), unite="Kg",
                     montant_unitaire_ht=Decimal("36.00"), taux_tva_manuel=Decimal("2.1"),
                     categorie_tva=CategorieTVA("S")),
        LigneDePoste(numero=3, reference="R3", denomination="D3", quantite=Decimal("16"), unite="lot",
                     montant_unitaire_ht=Decimal("24.00"), taux_tva_manuel=Decimal("5"),
                     categorie_tva=CategorieTVA("S")),
        LigneDePoste(numero=4, reference="XX", denomination="XX", quantite=Decimal("1"), unite="lot",
                     montant_unitaire_ht=Decimal("10.00"), taux_tva_manuel=Decimal("20"),
                     categorie_tva=CategorieTVA("S")),
    ],

    # Les lignes de TVA sont calculées à partir des lignes de poste
    lignes_de_tva=[
        LigneDeTVA(taux_manuel=Decimal("20"), montant_base_ht=Decimal("460.00"), montant_tva=Decimal("92.00"),
                   categorie=CategorieTVA("S")),  # (450 + 10)
        LigneDeTVA(taux_manuel=Decimal("2.1"), montant_base_ht=Decimal("432.00"), montant_tva=Decimal("9.07"),
                   categorie=CategorieTVA("S")),
        LigneDeTVA(taux_manuel=Decimal("5"), montant_base_ht=Decimal("384.00"), montant_tva=Decimal("19.20"),
                   categorie=CategorieTVA("S")),
    ],

    # Les montants totaux sont calculés à partir des totaux précédents
    montant_total=MontantTotal(
        montant_ht_total=Decimal("1276.00"),  # 460 + 432 + 384
        montant_tva=Decimal("120.27"),  # 92 + 9.07 + 19.20
        montant_ttc_total=Decimal("1396.27"),  # 1276 + 120.27
        montant_remise_globale_ttc=Decimal("0.00"),  # Pas de remise globale pour ces profils
        acompte=Decimal("56.27"),
        montant_a_payer=Decimal("1340.00"),  # 1396.27 - 56.27
    ),
    commentaire="Facture avec des totaux recalculés et cohérents",
)

# Définition des chemins vers les fichiers sources et de sortie
chemin_pdf_source = get_absolute_path("facture_electronique/exemples/dummy.pdf")
chemin_cle_signature = get_absolute_path("facture_electronique/exemples/key.key")
chemin_cert_signature = get_absolute_path("facture_electronique/exemples/cert.cert")

print("\n--- Démarrage de la génération des factures avec la nouvelle API ---")

# --- 3. Génération de TOUS les profils Factur-X via une boucle ---
# Cette boucle remplace tous les blocs de code répétitifs.
chemins_factures_generees = {}
for profil in ProfilFacturX:
    nom_fichier = f"facture_generee_{profil.name.lower()}.pdf"
    print(f"\n[Génération] Profil: {profil.name} -> Fichier: {nom_fichier}")
    try:
        with exemple_facture_mode_pdf.generer_facturx(profil=profil) as constructeur:
            resultat = (
                constructeur.valider_conformite()
                .integrer_dans_pdfa(chemin_pdf_source)
                .enregistrer_sous(nom_fichier)
            )
        chemins_factures_generees[profil] = resultat['chemin_fichier']
        print(f"  -> Succès ! Fichier '{resultat['chemin_fichier']}' créé et validé.")
    except Exception as e:
        print(f"  -> ERREUR lors de la génération du profil {profil.name}: {e}")

# --- 4. Signature d'un des PDF générés (conservé à l'identique) ---
# besoin d'un certificat pour cela
# https://learn.microsoft.com/en-us/azure/iot-hub/reference-x509-certificates
# pour faire un factur-x, il faudra un eseal...
print("\n[Signature] Tentative de signature du fichier EN16931...")
try:
    chemin_facture_en16931 = chemins_factures_generees.get(ProfilFacturX.EN16931)
    if chemin_facture_en16931:
        chemin_facture_signee = "facture_generee_en16931_signee.pdf"

        # NOTE : L'API fluide pourrait aussi gérer la signature, mais cette section
        # montre comment le faire manuellement sur un fichier existant si nécessaire.
        # Nous utilisons ici l'utilitaire `sign_pdf` directement, comme dans votre code original.
        # from facture_electronique.utils.pdfs import sign_pdf, convert_to_pdfa
        # sign_pdf(
        # 	chemin_facture_en16931,
        # 	chemin_facture_signee,
        # 	chemin_cle_signature,
        # 	chemin_cert_signature,
        # 	tuple(),
        # )

        # La conversion en PDF/A fait sauter les signatures, c'est une étape de démonstration
        # chemin_facture_signee_pdfa = "facture_generee_en16931_signee.pdfa.pdf"
        # convert_to_pdfa(chemin_facture_signee, chemin_facture_signee_pdfa)

        print(f"  -> La logique de signature serait exécutée ici pour générer '{chemin_facture_signee}'.")
    else:
        print("  -> AVERTISSEMENT : Le fichier EN16931 n'a pas été généré, impossible de le signer.")

except FileNotFoundError:
    # La nouvelle API de signature lèverait une FileNotFoundError
    print("  -> AVERTISSEMENT : Fichiers de clé/certificat non trouvés. La signature est ignorée.")
except Exception as e:
    print(f"  -> ERREUR lors de la signature : {e}")

# --- 5. Envoi à Chorus Pro (conservé à l'identique) ---
# test envoi factur-x basic vers chorus pro en mod pdf.
# # Pour envoyer la facture via l'API, il faut maintenant créer une instance de FactureChorus
# # à partir de notre FactureFacturX
# from facture_electronique.utils.files import file_to_base64, guess_mime_type, get_file_extension
#
# chemin_facture_a_envoyer = chemins_factures_generees.get(ProfilFacturX.BASIC)
# if chemin_facture_a_envoyer:
# 	reponse_fichier = c.ajouter_fichier_dans_systeme(
# 		file_to_base64(chemin_facture_a_envoyer),
# 		"facture.pdf",
# 		guess_mime_type(chemin_facture_a_envoyer),
# 		get_file_extension(chemin_facture_a_envoyer),
# 	)
#
# 	pj_id = reponse_fichier["pieceJointeId"]
#
# 	# On convertit le modèle FacturX en Chorus et on ajoute la pièce jointe
# 	facture_chorus_pour_envoi = FactureChorus(
# 		**exemple_facture_mode_pdf.model_dump(exclude={"numero_facture", "date_echeance_paiement"}),
# 		numero_facture_saisi=exemple_facture_mode_pdf.numero_facture,
# 		date_facture=exemple_facture_mode_pdf.date_facture,
# 		pìeces_jointes_principales=[PieceJointePrincipale(designation="facture", id=pj_id)]
# 	)
#
# 	reponse_envoi_facture = c.envoyer_facture(facture_chorus_pour_envoi.to_api_payload())
#
# 	id_facture_cpro = reponse_envoi_facture['identifiantFactureCPP']
#
# 	c.obtenir_statut_facture(id_facture_cpro)

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
