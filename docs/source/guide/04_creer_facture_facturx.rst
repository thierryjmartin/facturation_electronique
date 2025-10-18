.. _guide_creer_facture_facturx:

Créer une facture Factur-X
===========================

Factur-X est une norme franco-allemande de facture électronique qui consiste en un fichier PDF/A-3 contenant un fichier XML structuré. Cette section décrit comment générer une telle facture.




1. Construire l'objet FactureFacturX
------------------------------------

Cet objet contient toutes les données nécessaires à la fois pour le fichier XML et pour l'envoi ultérieur à Chorus Pro.

.. testsetup::

    from facture_electronique.models import AdresseElectronique, SchemeID

.. testcode::

    facturx_invoice = FactureFacturX(
        mode_depot=ModeDepot("DEPOT_PDF_API"),
        numero_facture="20240000000000000110",
        date_facture="2024-10-18",
        date_echeance_paiement="2024-11-18",
        destinataire=Destinataire(
            nom="Acheteur Principal SA",
            adresse_electronique=AdresseElectronique(identifiant="404833048"),  # SIREN 9 chiffres
            adresse_postale=AdressePostale(
                ligne_un="123 Rue de l'Exemple",
                code_postal="75001",
                nom_ville="Paris",
                pays_code_iso="FR",
            ),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=12345,
            nom="Fournisseur & Co.",
            adresse_electronique=AdresseElectronique(identifiant="802369878"),  # SIREN 9 chiffres
            numero_tva_intra="FR86802369878",  # N° TVA correspondant au SIREN
            iban="FR7630006000011234567890189",  # IBAN ajouté pour la conformité
            adresse_postale=AdressePostale(
                ligne_un="456 Avenue du Test",
                code_postal="69002",
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
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1000.00"),
            montant_tva=Decimal("200.00"),
            montant_ttc_total=Decimal("1200.00"),
            montant_a_payer=Decimal("1200.00"),
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                denomination="Prestation de service",
                quantite=Decimal("1"),
                unite="pce",
                montant_unitaire_ht=Decimal("1000.00"),
                taux_tva_manuel=Decimal("20"),
                categorie_tva=CategorieTVA.STANDARD,
            ),
        ],
        lignes_de_tva=[
            LigneDeTVA(
                taux_manuel=Decimal("20"),
                montant_base_ht=Decimal("1000.00"),
                montant_tva=Decimal("200.00"),
                categorie=CategorieTVA.STANDARD,
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

    chemin_pdf_source = get_absolute_path("../facture_electronique/exemples/dummy.pdf")
    chemin_cle_signature = get_absolute_path("../facture_electronique/exemples/key.key")
    chemin_cert_signature = get_absolute_path("../facture_electronique/exemples/cert.cert")

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
