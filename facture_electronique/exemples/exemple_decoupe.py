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
)
from facture_electronique.utils.files import get_absolute_path
from facture_electronique.utils.pdfs import convert_to_pdfa
from facture_electronique.utils.facturx import (
    gen_xml_depuis_facture,
    valider_xml_xldt,
    FACTURX_EN16931,
)
import facturx

if __name__ == "__main__":
    # --- Initialisation de l'API ---
    c = ChorusProAPI()
    # identifiant_cpro = c.obtenir_identifiant_cpro_depuis_siret("26073617692140") or 12345
    identifiant_cpro = 12345

    # --- 1. Exemple de facture pour l'API Chorus Pro (Mode SAISIE_API) ---

    chorus_invoice = FactureChorus(
        mode_depot=ModeDepot.SAISIE_API,
        id_utilisateur_courant=0,
        destinataire=Destinataire(
            code_destinataire="99986401570264",
        ),
        fournisseur=Fournisseur(
            id_fournisseur=identifiant_cpro,
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
                quantite=10,
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                taux_tva_manuel=20,
            ),
            LigneDePoste(
                numero=2,
                reference="R2",
                denomination="D2",
                quantite=12,
                unite="Kg",
                montant_unitaire_ht=Decimal("36.00"),
                taux_tva_manuel=2.1,
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("500.00"),
                montant_tva=Decimal("100.00"),
                taux_manuel=20,
            ),
            LigneDeTVA(
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.07"),
                taux_manuel=2.1,
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

    # --- 2. Exemple de facture pour Factur-X (et envoi via DEPOT_PDF_API) ---

    facturx_invoice = FactureFacturX(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FX-2024-001",
        date_facture="2024-10-18",
        date_echeance_paiement="2024-11-18",
        destinataire=Destinataire(
            code_destinataire="99986401570264",
            nom="Client Principal SA",
            adresse_postale=AdressePostale(
                ligne_un="123 Rue du Test", code_postal="75001", nom_ville="Paris"
            ),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=identifiant_cpro,
            siret="26073617692140",
            numero_tva_intra="FR61529571234",
            nom="Mon Entreprise SAS",
            adresse_postale=AdressePostale(
                ligne_un="456 Avenue du Code", code_postal="69001", nom_ville="Lyon"
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
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                denomination="Prestation de conseil",
                quantite=10,
                unite="heure",
                montant_unitaire_ht=Decimal("100.00"),
                categorie_tva=CategorieTVA.STANDARD,
                taux_tva_manuel=20,
            )
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("1000.00"),
                montant_tva=Decimal("200.00"),
                categorie=CategorieTVA.STANDARD,
                taux_manuel=20,
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
    pdfa_output = get_absolute_path("facture_electronique/exemples/dummy.pdfa.pdf")
    facturx_output = get_absolute_path(
        "facture_electronique/exemples/facture_en16931.pdf"
    )

    # 1. Convertir le PDF en PDF/A-3
    convert_to_pdfa(pdf_original, pdfa_output)

    # 2. Générer le XML Factur-X
    xml_content = gen_xml_depuis_facture(facturx_invoice.to_facturx_en16931())
    valider_xml_xldt(xml_content, FACTURX_EN16931)

    # 3. Intégrer le XML dans le PDF/A pour créer la facture Factur-X
    facturx.generate_from_file(
        pdfa_output,
        xml_content,
        output_pdf_file=facturx_output,
        flavor="factur-x",
        level="en16931",
        check_xsd=True,
    )

    print(f"Facture Factur-X générée : {facturx_output}")

    # --- 3. Envoi de la facture Factur-X à Chorus Pro (Mode DEPOT_PDF_API) ---

    # Il faudrait ici transformer la FactureFacturX en FactureChorus pour l'envoi.
    # Cela peut se faire avec un constructeur ou une méthode de conversion.
    chorus_pdf_invoice = FactureChorus(
        **facturx_invoice.model_dump(
            exclude={"numero_facture", "date_echeance_paiement"}
        ),
        numero_facture_saisi=facturx_invoice.numero_facture,
    )
    # # Logique d'envoi (décommenter pour utiliser)
    # reponse_fichier = c.ajouter_fichier_dans_systeme(
    # 	file_to_base64(facturx_output),
    # 	"facture.pdf",
    # 	guess_mime_type(facturx_output),
    # 	get_file_extension(facturx_output),
    # )
    #
    # pj_id = reponse_fichier["pieceJointeId"]
    #
    # chorus_pdf_invoice.pieces_jointes_principales = [PieceJointePrincipale(designation="Facture principale", id=pj_id)]
    #
    # payload = chorus_pdf_invoice.to_api_payload()
    # print(payload)
    # c.envoyer_facture(payload)
