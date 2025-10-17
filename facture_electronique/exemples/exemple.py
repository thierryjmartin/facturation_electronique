from dotenv import load_dotenv
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
    AdressePostale,  # Ajout pour la partie Chorus
)

# Le seul import nécessaire pour la génération Factur-X !
from facture_electronique.utils.facturx import ProfilFacturX

load_dotenv()

if __name__ == "__main__":
    c = ChorusProAPI(sandbox=True)

    # --- 1. Cinématique Chorus Pro (conservée à l'identique) ---
    """
	 A titre d'exemple, voici une cinématique nominale pour avoir des informations sur une structure et ses services:

			  1- Faire appel à l'API "RechercherStructure" afin de retrouver des structures avec quelques informations en sortie notamment "idStructureCPP

			  2- Faire appel à l'API "ConsulterStructure" avec en entrée l'idStructureCPP pour avoir les paramètres obligatoires de la structure (numéro d'engagement et/ou code service)

			  3- Faire appel à l'API "rechercherServicesStructure" avec "idStructure" en entrée de la requête afin de visualiser les services actifs de la structure renseignée

			  4- Faire appel à l'API consulterServiceStructure avec idService en entrée de la requête afin de consulter les paramètres obligatoires du service.
	"""
    payload = {
        "parametres": {
            "nbResultatsParPage": 10,
            "pageResultatDemandee": 1,
            "triColonne": "IdentifiantStructure",
            "triSens": "Descendant",
        },
        "restreindreStructuresPrivees": False,
        "structure": {
            "identifiantStructure": "26073617692140",
            "typeIdentifiantStructure": "SIRET",
        },
    }
    # recherche_structure = c.rechercher_structure(payload)
    # identifiant_cpro = 0
    # if recherche_structure["parametresRetour"]["total"] == 1:
    # identifiant_cpro = recherche_structure["listeStructures"][0]["idStructureCPP"]
    # print(identifiant_cpro)
    # identifiant_cpro = 12345
    # identifiant_cpro = c.obtenir_identifiant_cpro_depuis_siret("26073617692140")
    # c.consulter_structure(26300989)
    # c.rechercher_services_structure(26300989)
    # service = c.consulter_service_structure(id_structure=26311042, id_service=10657669)
    # print(service)

    # --- 2. Préparation des données de facture (conservée à l'identique) ---
    exemple_facture_mode_api = FactureChorus(
        mode_depot=ModeDepot("SAISIE_API"),
        id_utilisateur_courant=0,
        destinataire=Destinataire(
            code_destinataire="99986401570264", code_service_executant=""
        ),
        fournisseur=Fournisseur(id_fournisseur=12345),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            devise_facture="EUR",
            type_facture=TypeFacture("FACTURE"),
            type_tva=TypeTVA("TVA_SUR_DEBIT"),
            numero_marche="VABFM001",
            mode_paiement=ModePaiement("ESPECE"),
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                reference="R1",
                denomination="D1",
                quantite=Decimal("10"),
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=Decimal("20"),
            ),
            LigneDePoste(
                numero=2,
                reference="R2",
                denomination="D2",
                quantite=Decimal("12"),
                unite="Kg",
                montant_unitaire_ht=Decimal("36.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=Decimal("2.1"),
            ),
            LigneDePoste(
                numero=3,
                reference="R3",
                denomination="D3",
                quantite=Decimal("16"),
                unite="lot",
                montant_unitaire_ht=Decimal("24.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=Decimal("5"),
            ),
            LigneDePoste(
                numero=4,
                reference="XX",
                denomination="XX",
                quantite=Decimal("1"),
                unite="lot",
                montant_unitaire_ht=Decimal("10.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=Decimal("20"),
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                taux_manuel=Decimal("20"),
                taux=None,
                montant_base_ht=Decimal("510.00"),
                montant_tva=Decimal("102.00"),
            ),
            LigneDeTVA(
                taux_manuel=Decimal("2.1"),
                taux=None,
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.072"),
            ),
            LigneDeTVA(
                taux_manuel=Decimal("5"),
                taux=None,
                montant_base_ht=Decimal("384.00"),
                montant_tva=Decimal("19.20"),
            ),
        ],
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1326.00"),
            montant_tva=Decimal("130.272"),
            montant_ttc_total=Decimal("1406.272"),
            montant_remise_globale_ttc=Decimal("50.00"),
            motif_remise_globale_ttc="Geste commercial",
            montant_a_payer=Decimal("1400.00"),
        ),
        commentaire="Création_VABF_SoumettreFacture",
    )

    payload = {
        "numeroFactureSaisi": "FACT-2025-001",  # AJOUT OBLIGATOIRE
        # "dateFacture": "2025-10-17T00:00:00",  # FORMAT DATE-TIME
        "modeDepot": "SAISIE_API",
        "destinataire": {
            "codeDestinataire": "99986401570264",
            "codeServiceExecutant": "",  # À REMPLIR
        },
        "fournisseur": {
            "idFournisseur": 26073617692140,
            "idServiceFournisseur": 10652252,  # AJOUT OBLIGATOIRE
            # "codeCoordonneesBancairesFournisseur": 123,  # Si nécessaire
        },
        "cadreDeFacturation": {"codeCadreFacturation": "A1_FACTURE_FOURNISSEUR"},
        "references": {
            "deviseFacture": "EUR",
            "modePaiement": "ESPECE",
            "typeFacture": "FACTURE",
            "typeTva": "TVA_SUR_DEBIT",
            "numeroMarche": "VABFM001",
        },
        "commentaire": "Création_VABF_SoumettreFacture",
        "idUtilisateurCourant": 0,  # ID UTILISATEUR RÉEL
        "lignePoste": [
            {
                "lignePosteNumero": 1,
                "lignePosteReference": "R1",
                "lignePosteDenomination": "D1",
                "lignePosteQuantite": 10.0,  # FLOAT
                "lignePosteUnite": "lot",
                "lignePosteMontantUnitaireHT": 50.00,  # FLOAT
                "lignePosteMontantRemiseHT": 0.00,  # FLOAT
                "lignePosteTauxTva": "TVA2",
                "lignePosteTauxTvaManuel": 20.0,  # FLOAT
            },
            # ... autres lignes
        ],
        "ligneTva": [
            {
                "ligneTvaMontantBaseHtParTaux": 510.00,  # FLOAT
                "ligneTvaMontantTvaParTaux": 102.00,  # FLOAT
                "ligneTvaTaux": "TVA2",
                "ligneTvaTauxManuel": 20.0,  # FLOAT
            },
            # ... autres lignes
        ],
        "montantTotal": {
            "montantHtTotal": 1326.00,  # FLOAT
            "montantTVA": 130.27,  # FLOAT (notez 'montantTVA' pas 'montantTva')
            "montantTtcTotal": 1456.27,  # FLOAT
            "montantAPayer": 1406.27,  # FLOAT
            "montantRemiseGlobaleTTC": 50.00,  # FLOAT
            "motifRemiseGlobaleTTC": "Geste commercial",
        },
    }
    # print(exemple_facture_mode_api.to_api_payload())
    # c.envoyer_facture(exemple_facture_mode_api.to_api_payload())
    print(payload)
    res = c.envoyer_facture(payload)
    print(res)

    exemple_facture_mode_pdf = FactureFacturX(
        mode_depot=ModeDepot("DEPOT_PDF_API"),
        numero_facture="20240000000000000110",
        date_facture="2024-10-18",
        date_echeance_paiement="2024-11-18",
        id_utilisateur_courant=0,
        destinataire=Destinataire(
            nom="acheteur 99986401570264",
            code_destinataire="99986401570264",
            adresse_postale=AdressePostale(
                code_postal="122345",
                ligne_un="adresse du destinataire",
                nom_ville="PARIS",
                pays_code_iso="FR",
            ),
            code_service_executant="",
        ),
        fournisseur=Fournisseur(
            id_fournisseur=12345,
            nom="Fournisseur 26073617692140",
            siret="26073617692140",
            numero_tva_intra="FR61529571234",
            iban="FR7630006000011234567890189",
            adresse_postale=AdressePostale(
                code_postal="122345",
                ligne_un="2 rue de l andouillette",
                nom_ville="PARIS",
                pays_code_iso="FR",
            ),
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation("A1_FACTURE_FOURNISSEUR")
        ),
        references=References(
            devise_facture="EUR",
            type_facture=TypeFacture("FACTURE"),
            type_tva=TypeTVA("TVA_SUR_DEBIT"),
            numero_marche="VABFM001",
            numero_bon_commande="coucou",
            mode_paiement=ModePaiement("ESPECE"),
        ),
        # Les lignes de poste sont la source de vérité
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                reference="R1",
                denomination="D1",
                quantite=Decimal("10"),
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                montant_remise_ht=Decimal("5"),
                taux_tva_manuel=Decimal("20"),
                categorie_tva=CategorieTVA("S"),
                raison_reduction="parce que je suis sympa",
            ),
            LigneDePoste(
                numero=2,
                reference="R2",
                denomination="D2",
                quantite=Decimal("12"),
                unite="Kg",
                montant_unitaire_ht=Decimal("36.00"),
                taux_tva_manuel=Decimal("2.1"),
                categorie_tva=CategorieTVA("S"),
            ),
            LigneDePoste(
                numero=3,
                reference="R3",
                denomination="D3",
                quantite=Decimal("16"),
                unite="lot",
                montant_unitaire_ht=Decimal("24.00"),
                taux_tva_manuel=Decimal("5"),
                categorie_tva=CategorieTVA("S"),
            ),
            LigneDePoste(
                numero=4,
                reference="XX",
                denomination="XX",
                quantite=Decimal("1"),
                unite="lot",
                montant_unitaire_ht=Decimal("10.00"),
                taux_tva_manuel=Decimal("20"),
                categorie_tva=CategorieTVA("S"),
            ),
        ],
        # Les lignes de TVA sont calculées à partir des lignes de poste
        lignes_de_tva=[
            LigneDeTVA(
                taux_manuel=Decimal("20"),
                montant_base_ht=Decimal("460.00"),
                montant_tva=Decimal("92.00"),
                categorie=CategorieTVA("S"),
            ),  # (450 + 10)
            LigneDeTVA(
                taux_manuel=Decimal("2.1"),
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.07"),
                categorie=CategorieTVA("S"),
            ),
            LigneDeTVA(
                taux_manuel=Decimal("5"),
                montant_base_ht=Decimal("384.00"),
                montant_tva=Decimal("19.20"),
                categorie=CategorieTVA("S"),
            ),
        ],
        # Les montants totaux sont calculés à partir des totaux précédents
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1276.00"),  # 460 + 432 + 384
            montant_tva=Decimal("120.27"),  # 92 + 9.07 + 19.20
            montant_ttc_total=Decimal("1396.27"),  # 1276 + 120.27
            montant_remise_globale_ttc=Decimal(
                "0.00"
            ),  # Pas de remise globale pour ces profils
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
            with exemple_facture_mode_pdf.generer_facturx(
                profil=profil
            ) as constructeur:
                resultat = (
                    constructeur.valider_conformite()
                    .integrer_dans_pdfa(chemin_pdf_source)
                    .enregistrer_sous(nom_fichier)
                )
            chemins_factures_generees[profil] = resultat["chemin_fichier"]
            print(
                f"  -> Succès ! Fichier '{resultat['chemin_fichier']}' créé et validé."
            )
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

            print(
                f"  -> La logique de signature serait exécutée ici pour générer '{chemin_facture_signee}'."
            )
        else:
            print(
                "  -> AVERTISSEMENT : Le fichier EN16931 n'a pas été généré, impossible de le signer."
            )

    except FileNotFoundError:
        # La nouvelle API de signature lèverait une FileNotFoundError
        print(
            "  -> AVERTISSEMENT : Fichiers de clé/certificat non trouvés. La signature est ignorée."
        )
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
