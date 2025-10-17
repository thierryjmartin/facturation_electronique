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


2. Convertir le PDF en PDF/A-3
--------------------------------

La norme Factur-X exige que le PDF porteur soit au format PDF/A-3. La fonction `convert_to_pdfa` utilise Ghostscript pour effectuer cette conversion.

.. testcode::

    import os
    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)

    pdf_original = "../facture_electronique/exemples/dummy.pdf"
    pdfa_output = os.path.join(output_dir, "dummy.pdfa.pdf")

    # La conversion peut prendre quelques secondes
    convert_to_pdfa(pdf_original, pdfa_output)

    assert os.path.exists(pdfa_output)

    # On choisit ici le profil EN16931 (ou EXTENDED pour plus de détails)
    xml_content = gen_xml_depuis_facture(facturx_invoice.to_facturx_en16931())
    
    # La validation lève une exception en cas de non-conformité
    try:
        valider_xml_facturx_schematron(xml_content, FACTURX_EN16931)
        validation_ok = True
    except Exception:
        validation_ok = False

    assert validation_ok is True
    assert "<rsm:ExchangedDocumentContext>" in xml_content

    facturx_output = os.path.join(output_dir, "facture_en16931.pdf")

    facturx.generate_from_file(
        pdfa_output, # Le PDF/A généré à l'étape 2
        xml_content, # Le XML généré à l'étape 3
        output_pdf_file=facturx_output,
        flavor="factur-x",
        level="en16931",
        check_xsd=True, # Active la validation XSD interne
    )

    assert os.path.exists(facturx_output)


    # On choisit ici le profil EXTENDED
    xml_content_extended = gen_xml_depuis_facture(facturx_invoice.to_facturx_extended())

    try:
        valider_xml_facturx_schematron(xml_content_extended, FACTURX_EXTENDED)
        validation_ok_extended = True
    except XSLTValidationError:
        validation_ok_extended = False

    assert validation_ok_extended is False

    assert validation_ok_extended is True
    assert "<rsm:ExchangedDocumentContext>" in xml_content_extended

    facturx_output_extended = os.path.join(output_dir, "facture_extended.pdf")

    facturx.generate_from_file(
        pdfa_output, # Le PDF/A généré à l'étape 2
        xml_content_extended, # Le XML généré
        output_pdf_file=facturx_output_extended,
        flavor="factur-x",
        level="extended",
        check_xsd=True, # Active la validation XSD interne
    )

    assert os.path.exists(facturx_output_extended)


Le fichier `facture_en16931.pdf` est maintenant une facture Factur-X valide, prête à être envoyée.
