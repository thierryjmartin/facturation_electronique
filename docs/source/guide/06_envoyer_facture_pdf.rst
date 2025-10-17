.. _guide_envoyer_facture_pdf:

Envoyer une facture Factur-X (PDF)
====================================

Une fois votre facture Factur-X générée (et éventuellement signée), vous pouvez la soumettre à Chorus Pro en utilisant le mode `DEPOT_PDF_API`.




Le processus se déroule en trois temps : l'envoi du fichier, la création de l'objet `FactureChorus`, et l'envoi final.

1. Envoyer le fichier PDF
-------------------------

On commence par envoyer le fichier Factur-X au système de fichiers de Chorus Pro avec `ajouter_fichier_dans_systeme`. L'API nous retourne un identifiant pour cette pièce jointe.

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

    if False:
        # Conversion du fichier en base64
        contenu_base64 = file_to_base64(facturx_output)

        # Envoi du fichier
        c = ChorusProAPI(sandbox=True)
        reponse_fichier = c.ajouter_fichier_dans_systeme(
            contenu_base64,
            "facture.pdf",
            guess_mime_type(facturx_output),
            get_file_extension(facturx_output),
        )

        # On récupère l'ID de la pièce jointe
        pj_id = reponse_fichier["pieceJointeId"]
    else:
        # Pour les tests, on utilise un ID factice
        pj_id = 98765

    assert isinstance(pj_id, int)

    # On convertit le modèle FacturX en Chorus.
    # La plupart des champs peuvent être réutilisés directement.
    facture_chorus_pour_envoi = FactureChorus(
        **facturx_invoice.model_dump(),
        pieces_jointes_principales=[PieceJointePrincipale(designation="facture", id=pj_id)]
    )

    assert facture_chorus_pour_envoi.pieces_jointes_principales[0].id == pj_id
    assert facture_chorus_pour_envoi.numero_facture == "FX-2024-001"

    payload = facture_chorus_pour_envoi.to_api_payload()

    if False:
        reponse_envoi = c.envoyer_facture(payload)
        # id_facture_cpp = reponse_envoi['identifiantFactureCPP']

    assert payload["piecesJointesPrincipales"][0]["id"] == pj_id