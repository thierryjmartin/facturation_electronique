.. _guide_creer_facture_facturx:

Créer une facture Factur-X
===========================

Factur-X est une norme franco-allemande de facture électronique qui consiste en un fichier PDF/A-3 contenant un fichier XML structuré. Cette section décrit comment générer une telle facture.




1. Construire l'objet FactureFacturX
------------------------------------

Cet objet contient toutes les données nécessaires à la fois pour le fichier XML et pour l'envoi ultérieur à Chorus Pro.

.. testcode::

    facturx_invoice = FactureFacturX(
        mode_depot=ModeDepot("DEPOT_PDF_API"),
        numero_facture="20240000000000000110",
        date_facture="2024-10-18",  # seulement en depot PDF
        date_echeance_paiement="2014-12-18",
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
                quantite=Decimal("10"),
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                montant_remise_ht=Decimal("5"),
                taux_tva="",
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
                montant_remise_ht=Decimal("0"),
                taux_tva="",
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
                montant_remise_ht=Decimal("0"),
                taux_tva="",
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
                montant_remise_ht=Decimal("0"),
                taux_tva="",
                taux_tva_manuel=Decimal("20"),
                categorie_tva=CategorieTVA("S"),
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                taux_manuel=Decimal("20"),
                taux=None,
                montant_base_ht=Decimal("510.00"),
                montant_tva=Decimal("102.00"),
                categorie=CategorieTVA("S"),
            ),
            LigneDeTVA(
                taux_manuel=Decimal("2.1"),
                taux=None,
                montant_base_ht=Decimal("432.00"),
                montant_tva=Decimal("9.072"),
                categorie=CategorieTVA("S"),
            ),
            LigneDeTVA(
                taux_manuel=Decimal("5"),
                taux=None,
                montant_base_ht=Decimal("384.00"),
                montant_tva=Decimal("19.20"),
                categorie=CategorieTVA("S"),
            ),
        ],
    )
    assert facturx_invoice.numero_facture == "20240000000000000110"


2. Génération de TOUS les profils Factur-X via une boucle
----------------------------------------------------------

La nouvelle API fluide permet de générer tous les profils Factur-X de manière concise.

.. testcode::

    import os
    from facture_electronique.utils.facturx import ProfilFacturX
    from facture_electronique.utils.files import get_absolute_path
    from facture_electronique.utils.pdfs import convert_to_pdfa

    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)

    chemin_pdf_source = get_absolute_path("facture_electronique/exemples/dummy.pdf")
    chemin_cle_signature = get_absolute_path("facture_electronique/exemples/key.key")
    chemin_cert_signature = get_absolute_path("facture_electronique/exemples/cert.cert")

    chemins_factures_generees = {}
    for profil in ProfilFacturX:
        nom_fichier = os.path.join(output_dir, f"facture_generee_{profil.name.lower()}.pdf")
        try:
            with facturx_invoice.generer_facturx(profil=profil) as constructeur:
                resultat = (
                    constructeur.valider_conformite()
                    .integrer_dans_pdfa(chemin_pdf_source)
                    .enregistrer_sous(nom_fichier)
                )
            chemins_factures_generees[profil] = resultat['chemin_fichier']
        except Exception as e:
            print(f"  -> ERREUR lors de la génération du profil {profil.name}: {e}")

    assert os.path.exists(chemins_factures_generees[ProfilFacturX.EN16931])
    assert os.path.exists(chemins_factures_generees[ProfilFacturX.EXTENDED])


Le fichier `facture_generee_en16931.pdf` est maintenant une facture Factur-X valide, prête à être envoyée.
