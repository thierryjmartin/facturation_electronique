from decimal import Decimal
from facture_electronique.api.chorus_pro import ChorusProAPI
from facture_electronique.models import (
    FactureChorus,
    FactureFacturX,
    ModeDepot,
    Destinataire,
    Fournisseur,
    CadreDeFacturation,
    CodeCadreFacturation,
    References,
    TypeFacture,
    TypeTVA,
    ModePaiement,
    LigneDePoste,
    LigneDeTVA,
    MontantTotal,
    AdressePostale,
    CategorieTVA,
    AdresseElectronique,  # Ajout
    SchemeID,  # Ajout
)
from facture_electronique.utils.files import get_absolute_path
from dotenv import load_dotenv

# --- MISE À JOUR DES IMPORTS ---
# On n'importe plus les anciennes fonctions procédurales, mais la nouvelle Enum `ProfilFacturX`.
from facture_electronique.utils.facturx import ProfilFacturX

if __name__ == "__main__":
    load_dotenv()
    # --- Initialisation de l'API (inchangé) ---
    c = ChorusProAPI()
    fournisseur_siret = "26073617692140"
    destinataire_siret = "99986401570264"
    identifiant_cpro = 12345  # ID CPro du fournisseur

    # --- 1. Exemple de facture pour l'API Chorus Pro (Mode SAISIE_API) - (Mise à jour) ---
    chorus_invoice = FactureChorus(
        mode_depot=ModeDepot.SAISIE_API,
        numero_facture="API-2025-003",
        date_echeance_paiement="2025-12-01",
        id_utilisateur_courant=0,
        destinataire=Destinataire(
            adresse_electronique=AdresseElectronique(
                identifiant=destinataire_siret, scheme_id=SchemeID.FR_SIREN
            ),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=identifiant_cpro,
            adresse_electronique=AdresseElectronique(
                identifiant=fournisseur_siret, scheme_id=SchemeID.FR_SIREN
            ),
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR,
        ),
        references=References(
            devise_facture="EUR",
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            numero_marche="VABFM001",
            mode_paiement=ModePaiement.ESPECE,
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                reference="R1",
                denomination="D1",
                quantite=Decimal("10"),
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                taux_tva_manuel=Decimal("20"),
            ),
            LigneDePoste(
                numero=2,
                reference="R2",
                denomination="D2",
                quantite=Decimal("12"),
                unite="Kg",
                montant_unitaire_ht=Decimal("36.00"),
                taux_tva_manuel=Decimal("2.1"),
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("500.00"),
                montant_tva=Decimal("100.00"),
                taux_manuel=Decimal("20"),
            ),
            LigneDeTVA(
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.07"),
                taux_manuel=Decimal("2.1"),
            ),
        ],
        montant_total=MontantTotal(
            montant_ht_total=Decimal("932.00"),
            montant_tva=Decimal("109.07"),
            montant_ttc_total=Decimal("1041.07"),
            montant_a_payer=Decimal("1041.07"),
        ),
        commentaire="Facture envoyée via SAISIE_API",
    )

    # payload = chorus_invoice.to_api_payload()
    # print(payload)
    # c.envoyer_facture(payload)

    # --- 2. Exemple de facture pour Factur-X (et envoi via DEPOT_PDF_API) - (Mise à jour) ---
    facturx_invoice = FactureFacturX(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FX-2024-001",
        date_facture="2024-01-01",
        date_echeance_paiement="2024-11-18",
        destinataire=Destinataire(
            adresse_electronique=AdresseElectronique(
                identifiant=destinataire_siret, scheme_id=SchemeID.FR_SIREN
            ),
            nom="Client Principal SA",
            adresse_postale=AdressePostale(
                ligne_un="123 Rue du Test",
                code_postal="75001",
                nom_ville="Paris",
                pays_code_iso="FR",
            ),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=identifiant_cpro,
            adresse_electronique=AdresseElectronique(
                identifiant=fournisseur_siret, scheme_id=SchemeID.FR_SIREN
            ),
            numero_tva_intra="FR61529571234",
            nom="Mon Entreprise SAS",
            iban="FR7630006000011234567890189",
            adresse_postale=AdressePostale(
                ligne_un="456 Avenue du Code",
                code_postal="69001",
                nom_ville="Lyon",
                pays_code_iso="FR",
            ),
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
            numero_bon_commande="BC-456",
            devise_facture="EUR",
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                denomination="Prestation de conseil",
                quantite=Decimal("10"),
                unite="heure",
                montant_unitaire_ht=Decimal("100.00"),
                categorie_tva=CategorieTVA.STANDARD,
                taux_tva_manuel=Decimal("20"),
            )
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("1000.00"),
                montant_tva=Decimal("200.00"),
                categorie=CategorieTVA.STANDARD,
                taux_manuel=Decimal("20"),
            )
        ],
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1000.00"),
            montant_tva=Decimal("200.00"),
            montant_ttc_total=Decimal("1200.00"),
            montant_a_payer=Decimal("1200.00"),
        ),
    )

    # --- Génération du PDF/A et du fichier Factur-X ---
    pdf_original = get_absolute_path("facture_electronique/exemples/dummy.pdf")
    facturx_output = get_absolute_path("facture_electronique/exemples/facture_en16931.pdf")

    # --- MISE À JOUR : Remplacement du bloc de génération procédural ---
    # L'ancien bloc de 4 étapes manuelles est remplacé par un seul appel fluide.
    # L'API s'occupe de la validation, de la conversion PDF/A et de l'intégration du XML.

    print(f"Génération de la facture Factur-X (profil EN16931) vers '{facturx_output}'...")
    try:
        with facturx_invoice.generer_facturx(profil=ProfilFacturX.EN16931) as constructeur:
            resultat = (
                constructeur.valider_conformite()
                .integrer_dans_pdfa(pdf_original)
                .enregistrer_sous(facturx_output)
            )
        print(f"Facture Factur-X générée avec succès : {resultat['chemin_fichier']}")
    except Exception as e:
        print(f"ERREUR lors de la génération Factur-X : {e}")

    # --- 3. Envoi de la facture Factur-X à Chorus Pro (Mode DEPOT_PDF_API) ---
    # Cette logique reste valide. Elle utilise le fichier généré à l'étape précédente.

    # Il faudrait ici transformer la FactureFacturX en FactureChorus pour l'envoi.
    # Cela peut se faire avec un constructeur ou une méthode de conversion.
    chorus_pdf_invoice = FactureChorus(
        **facturx_invoice.model_dump(),
    )

# # Logique d'envoi (décommenter pour utiliser)
# from facture_electronique.utils.files import file_to_base64, guess_mime_type, get_file_extension
#
# # On utilise le chemin du fichier qui vient d'être généré
# chemin_facture_a_envoyer = facturx_output
#
# reponse_fichier = c.ajouter_fichier_dans_systeme(
# 	file_to_base64(chemin_facture_a_envoyer),
# 	"facture.pdf",
# 	guess_mime_type(chemin_facture_a_envoyer),
# 	get_file_extension(chemin_facture_a_envoyer),
# )
#
# pj_id = reponse_fichier["pieceJointeId"]
#
# chorus_pdf_invoice.pieces_jointes_principales = [PieceJointePrincipale(designation="Facture principale", id=pj_id)]
#
# payload = chorus_pdf_invoice.to_api_payload()
# print(payload)
# c.envoyer_facture(payload)
