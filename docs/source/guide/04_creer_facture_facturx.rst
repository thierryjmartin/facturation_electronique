.. _guide_creer_facture_facturx:

Créer une facture Factur-X
===========================

Factur-X est une norme franco-allemande de facture électronique qui consiste en un fichier PDF/A-3 contenant un fichier XML structuré. Cette section décrit comment générer une telle facture.




1. Construire l'objet FactureFacturX
------------------------------------

Cet objet contient toutes les données nécessaires à la fois pour le fichier XML et pour l'envoi ultérieur à Chorus Pro.

.. testcode::

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
            id_fournisseur=12345,
            siret="26073617692140",
            numero_tva_intra="FR61529571234",
            nom="Mon Entreprise SAS",
			iban="FR7630006000011234567890189",
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

    assert facturx_invoice.numero_facture == "FX-2024-001"


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

    # On choisit ici le profil EN16931, le plus complet
    xml_content = gen_xml_depuis_facture(facturx_invoice.to_facturx_en16931())
    
    # La validation lève une exception en cas de non-conformité
    try:
        valider_xml_xldt(xml_content, FACTURX_EN16931)
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


Le fichier `facture_en16931.pdf` est maintenant une facture Factur-X valide, prête à être envoyée.
