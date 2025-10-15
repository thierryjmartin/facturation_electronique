import facturx

from decimal import Decimal
from facture_electronique.utils.pdfs import convert_to_pdfa, sign_pdf
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
)


if __name__ == "__main__":
    c = ChorusProAPI()
    # print(c.token)

    """
	 A titre d'exemple, voici une cinématique nominale pour avoir des informations sur une structure et ses services:

              1- Faire appel à l'API "RechercherStructure" afin de retrouver des structures avec quelques informations en sortie notamment "idStructureCPP

              2- Faire appel à l'API "ConsulterStructure" avec en entrée l'idStructureCPP pour avoir les paramètres obligatoires de la structure (numéro d'engagement et/ou code service)

              3- Faire appel à l'API "rechercherServicesStructure" avec "idStructure" en entrée de la requête afin de visualiser les services actifs de la structure renseignée

              4- Faire appel à l'API consulterServiceStructure avec idService en entrée de la requête afin de consulter les paramètres obligatoires du service.
    """

    # 1 .

    payload = {
        "parametres": {
            "nbResultatsParPage": 10,
            "pageResultatDemandee": 1,
            "triColonne": "IdentifiantStructure",
            "triSens": "Descendant",
        },
        "restreindreStructuresPrivees": False,
        "structure": {
            # "adresseCodePays": "string",
            # "adresseCodePostal": "string",
            # "adresseVille": "string",
            # "estMOA": true,
            # "estMOAUniquement": true,
            "identifiantStructure": "26073617692140",
            # "libelleStructure": "string",
            # "nomStructure": "string",
            # "prenomStructure": "string",
            # "raisonSocialeStructure": "string",
            # "statutStructure": "ACTIF",
            "typeIdentifiantStructure": "SIRET",
            # "typeStructure": "PUBLIQUE"
        },
    }

    # recherche_structure = c.rechercher_structure(payload)

    # identifiant_cpro = 0
    # if recherche_structure["parametresRetour"]["total"] == 1:
    # identifiant_cpro = recherche_structure["listeStructures"][0]["idStructureCPP"]
    # print(identifiant_cpro)

    # identifiant_cpro = 12345

    # identifiant_cpro = c.obtenir_identifiant_cpro_depuis_siret("26073617692140")

    # 2 .
    # c.consulter_structure(26300989)
    # 3 .
    # c.rechercher_services_structure(26300989)

    # 4.
    # service = c.consulter_service_structure(id_structure=26311042, id_service=10657669)
    # print(service)

    exemple_facture_mode_api = FactureChorus(
        mode_depot=ModeDepot("SAISIE_API"),
        # numero_facture_saisi="20240000000000000013", # ce champ n'est pas utilié en mode_depot saisie_api
        # date_facture="2024-15-08", # seulement en depot PDF
        id_utilisateur_courant=0,
        destinataire=Destinataire(
            code_destinataire="99986401570264",
            code_service_executant="",  # est absent
        ),
        fournisseur=Fournisseur(
            id_fournisseur=12345,  # identifiant_cpro,
            # Les autres champs du fournisseur sont absents
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR,
            code_structure_valideur=None,
        ),
        references=References(
            devise_facture="EUR",
            type_facture=TypeFacture("FACTURE"),
            type_tva=TypeTVA("TVA_SUR_DEBIT"),
            motif_exoneration_tva=None,
            numero_marche="VABFM001",
            numero_bon_commande=None,
            numero_facture_origine=None,
            mode_paiement=ModePaiement("ESPECE"),
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                reference="R1",
                denomination="D1",
                quantite=10,
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=20,
            ),
            LigneDePoste(
                numero=2,
                reference="R2",
                denomination="D2",
                quantite=12,
                unite="Kg",
                montant_unitaire_ht=Decimal("36.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=2.1,
            ),
            LigneDePoste(
                numero=3,
                reference="R3",
                denomination="D3",
                quantite=16,
                unite="lot",
                montant_unitaire_ht=Decimal("24.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=5,
            ),
            LigneDePoste(
                numero=4,
                reference="XX",
                denomination="XX",
                quantite=1,
                unite="lot",
                montant_unitaire_ht=Decimal("10.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=20,
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                taux_manuel=20,
                taux=None,
                montant_base_ht=Decimal("510.00"),
                montant_tva=Decimal("102.00"),
            ),
            LigneDeTVA(
                taux_manuel=2.1,
                taux=None,
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.072"),
            ),
            LigneDeTVA(
                taux_manuel=5,
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

    # c.envoyer_facture(exemple_facture_mode_api.to_api_payload())
    # print(exemple_facture.to_facturx_basic())

    file_path = get_absolute_path("facture_electronique/exemples/dummy.pdf")

    file_path_pdfa = get_absolute_path("facture_electronique/exemples/dummy.pdfa.pdf")

    convert_to_pdfa(file_path, file_path_pdfa)

    exemple_facture_mode_pdf = FactureFacturX(
        mode_depot=ModeDepot("DEPOT_PDF_API"),
        numero_facture="20240000000000000110",
        date_facture="2024-10-18",  # seulement en depot PDF
        date_echeance_paiement="2014-12-18",
        id_utilisateur_courant=0,
        # piece_jointe_principale n'est plus dans FactureFacturX, il faut créer une FactureChorus pour l'envoi API
        # piece_jointe_principale = [PieceJointePrincipale(
        # 	designation = 'facture',
        # 	# id = pj_id
        # )],
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
            id_fournisseur=12345,  # identifiant_cpro,
            nom="Fournisseur 26073617692140",
            siret="26073617692140",
            numero_tva_intra="FR61529571234",
            adresse_postale=AdressePostale(
                code_postal="122345",
                ligne_un="2 rue de l andouillette",
                nom_ville="PARIS",
                pays_code_iso="FR",
            ),
            # Les autres champs du fournisseur sont absents
        ),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation("A1_FACTURE_FOURNISSEUR"),
            code_structure_valideur=None,
        ),
        references=References(
            devise_facture="EUR",
            type_facture=TypeFacture("FACTURE"),
            type_tva=TypeTVA("TVA_SUR_DEBIT"),
            motif_exoneration_tva=None,
            numero_marche="VABFM001",
            numero_bon_commande="coucou",
            numero_facture_origine=None,
            mode_paiement=ModePaiement("ESPECE"),
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1326.00"),
            montant_tva=Decimal("130.272"),
            montant_ttc_total=Decimal("1456.272"),
            montant_remise_globale_ttc=Decimal("0.00"),
            motif_remise_globale_ttc="",
            acompte=Decimal("56.272"),
            montant_a_payer=Decimal("1400.00"),
        ),
        commentaire="voici mon commentaire",
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                reference="R1",
                denomination="D1",
                quantite=10,
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                montant_remise_ht=Decimal("5"),
                taux_tva="",
                taux_tva_manuel=20,
                categorie_tva=CategorieTVA("S"),
                raison_reduction="parce que je suis sympa",
            ),
            LigneDePoste(
                numero=2,
                reference="R2",
                denomination="D2",
                quantite=12,
                unite="Kg",
                montant_unitaire_ht=Decimal("36.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=2.1,
                categorie_tva=CategorieTVA("S"),
            ),
            LigneDePoste(
                numero=3,
                reference="R3",
                denomination="D3",
                quantite=16,
                unite="lot",
                montant_unitaire_ht=Decimal("24.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=5,
                categorie_tva=CategorieTVA("S"),
            ),
            LigneDePoste(
                numero=4,
                reference="XX",
                denomination="XX",
                quantite=1,
                unite="lot",
                montant_unitaire_ht=Decimal("10.00"),
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=20,
                categorie_tva=CategorieTVA("S"),
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                taux_manuel=20,
                taux=None,
                montant_base_ht=Decimal("510.00"),
                montant_tva=Decimal("102.00"),
                categorie=CategorieTVA("S"),
            ),
            LigneDeTVA(
                taux_manuel=2.1,
                taux=None,
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.072"),
                categorie=CategorieTVA("S"),
            ),
            LigneDeTVA(
                taux_manuel=5,
                taux=None,
                montant_base_ht=Decimal("384.00"),
                montant_tva=Decimal("19.20"),
                categorie=CategorieTVA("S"),
            ),
        ],
    )

    from facture_electronique.utils.facturx import (
        gen_xml_depuis_facture,
        valider_xml_xldt,
        chemin_xldt_basic,
        chemin_xldt_minimum,
        chemin_xldt_en16931,
    )

    file_path_facturx_mini = file_path + ".facturx.minmum.pdf"
    file_path_facturx_basic = file_path + ".facturx.basic.pdf"
    file_path_facturx_en16931 = file_path + ".facturx.en16931.pdf"

    # test generation factur-x minimum
    xml = gen_xml_depuis_facture(exemple_facture_mode_pdf.to_facturx_minimum())
    valider_xml_xldt(xml, chemin_xldt_minimum)
    facturx.generate_from_file(
        file_path_pdfa,
        xml,
        output_pdf_file=file_path_facturx_mini,
        flavor="factur-x",
        level="minimum",
        check_xsd=False,
    )
    facturx.generate_from_file(
        file_path_pdfa,
        xml,
        output_pdf_file=file_path_facturx_mini,
        flavor="factur-x",
        level="minimum",
        check_xsd=True,
    )

    # test generation factur-x basic
    xml = gen_xml_depuis_facture(exemple_facture_mode_pdf.to_facturx_basic())
    valider_xml_xldt(xml, chemin_xldt_basic)
    facturx.generate_from_file(
        file_path_pdfa,
        xml,
        output_pdf_file=file_path_facturx_basic,
        flavor="factur-x",
        level="basic",
        check_xsd=False,
    )
    facturx.generate_from_file(
        file_path_pdfa,
        xml,
        output_pdf_file=file_path_facturx_basic,
        flavor="factur-x",
        level="basic",
        check_xsd=True,
    )

    # test generation factur-x EN16931
    xml = gen_xml_depuis_facture(exemple_facture_mode_pdf.to_facturx_en16931())
    valider_xml_xldt(xml, chemin_xldt_en16931)
    facturx.generate_from_file(
        file_path_pdfa,
        xml,
        output_pdf_file=file_path_facturx_en16931,
        flavor="factur-x",
        level="en16931",
        check_xsd=False,
    )
    facturx.generate_from_file(
        file_path_pdfa,
        xml,
        output_pdf_file=file_path_facturx_en16931,
        flavor="factur-x",
        level="en16931",
        check_xsd=True,
    )

    # besoin d'un certificat pour cela
    # https://learn.microsoft.com/en-us/azure/iot-hub/reference-x509-certificates
    # pour faire un factur-x, il faudra un eseal...
    try:
        # l'ajout de la signature fait sauter la conformité PDF/A
        file_path_pdfsigned = file_path + ".pdfsigned.pdf"
        sign_pdf(
            file_path_facturx_en16931,
            file_path_pdfsigned,
            get_absolute_path("facture_electronique/exemples/key.key"),
            get_absolute_path("facture_electronique/exemples/cert.cert"),
            tuple(),
        )
        file_path_pdfsigned_pdfa = file_path + ".pdfsigned.pdfa.pdf"
        # la conversion en PDF/A fait sauter les signatures
        convert_to_pdfa(file_path_pdfsigned, file_path_pdfsigned_pdfa)
    except AttributeError:
        # AttributeError est généré si les fichiers de clé et/ou certificat n'existent pas
        pass

    # test envoi faxctur-x basic vers chorus pro en mod pdf.
    # # Pour envoyer la facture via l'API, il faut maintenant créer une instance de FactureChorus
    # # à partir de notre FactureFacturX
    # reponse_fichier = c.ajouter_fichier_dans_systeme(
    # 	file_to_base64(file_path_facturx_basic),
    # 	"facture.pdf",
    # 	guess_mime_type(file_path),
    # 	get_file_extension(file_path),
    # )
    #
    # pj_id = reponse_fichier["pieceJointeId"]
    #
    # # On convertit le modèle FacturX en Chorus et on ajoute la pièce jointe
    # facture_chorus_pour_envoi = FactureChorus(
    # 	**exemple_facture_mode_pdf.model_dump(exclude={"numero_facture", "date_echeance_paiement"}),
    # 	numero_facture_saisi=exemple_facture_mode_pdf.numero_facture,
    # 	date_facture=exemple_facture_mode_pdf.date_facture,
    # 	pìeces_jointes_principales=[PieceJointePrincipale(designation="facture", id=pj_id)]
    # )
    #
    # reponse_envoi_facture = c.envoyer_facture(facture_chorus_pour_envoi.to_api_payload())
    #
    # id_facture_cpro = reponse_envoi_facture['identifiantFactureCPP']
    #
    # c.obtenir_statut_facture(id_facture_cpro)
