.. _guide_creer_facture_api:

Créer une facture en mode API
=============================

Le mode `SAISIE_API` permet de soumettre une facture en fournissant toutes les données directement via l'API, sans attacher de fichier PDF. C'est le mode le plus direct pour une intégration complète.




1. Construire l'objet Facture
------------------------------

La première étape est de construire un objet `FactureChorus` qui représente la facture avec toutes ses informations : destinataire, fournisseur, lignes de facture, montants, etc.

.. testcode::

    # L'identifiant technique du fournisseur sur Chorus Pro.
    # Voir le guide "Interagir avec l'API Chorus Pro" pour savoir comment le récupérer.
    identifiant_fournisseur_chorus = 12345

    facture_api = FactureChorus(
        mode_depot=ModeDepot.SAISIE_API,
        id_utilisateur_courant=0, # L'ID de l'utilisateur qui effectue l'action
        destinataire=Destinataire(
            code_destinataire="99986401570264", # SIRET du client
        ),
        fournisseur=Fournisseur(
            id_fournisseur=identifiant_fournisseur_chorus,
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
                denomination="D1",
                quantite=Decimal("10"),
                unite="lot",
                montant_unitaire_ht=Decimal("50.00"),
                taux_tva_manuel=Decimal("20"),
            ),
            LigneDePoste(
                numero=2,
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

    assert facture_api.montant_total.montant_ttc_total == Decimal("1041.07")
    assert len(facture_api.lignes_de_poste) == 2

    # On génère le dictionnaire attendu par l'API Chorus Pro
    payload = facture_api.to_api_payload()

    if False:
        # Envoi de la facture à Chorus Pro
        c = ChorusProAPI(sandbox=True)
        reponse_envoi = c.envoyer_facture(payload)
        # En cas de succès, la réponse contient l'identifiant de la facture sur Chorus
        # id_facture_cpp = reponse_envoi['identifiantFactureCPP']

    assert payload["fournisseur"]["idFournisseur"] == identifiant_fournisseur_chorus
