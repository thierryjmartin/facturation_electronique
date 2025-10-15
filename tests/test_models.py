from decimal import Decimal
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
)


def test_creation_facture_chorus_simple():
    """Teste la création d'une instance simple de FactureChorus et sa sérialisation."""
    facture = FactureChorus(
        mode_depot=ModeDepot.SAISIE_API,
        destinataire=Destinataire(code_destinataire="123456789"),
        fournisseur=Fournisseur(id_fournisseur=9876),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("100.0"),
            montant_tva=Decimal("20.0"),
            montant_ttc_total=Decimal("120.0"),
            montant_a_payer=Decimal("120.0"),
        ),
        lignes_de_poste=[
            LigneDePoste(
                numero=1,
                denomination="Test",
                quantite=1,
                unite="pce",
                montant_unitaire_ht=Decimal("100.0"),
            )
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("100.0"),
                montant_tva=Decimal("20.0"),
                taux_manuel=20.0,
            )
        ],
    )
    assert facture.mode_depot == ModeDepot.SAISIE_API
    assert facture.destinataire.code_destinataire == "123456789"


def test_facture_chorus_to_api_payload():
    """Teste la méthode to_api_payload pour la conversion en camelCase."""
    facture = FactureChorus(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture_saisi="FAC-2024-01",
        destinataire=Destinataire(
            code_destinataire="123456789", code_service_executant="RH"
        ),
        fournisseur=Fournisseur(id_fournisseur=9876),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("100.0"),
            montant_tva=Decimal("20.0"),
            montant_ttc_total=Decimal("120.0"),
            montant_a_payer=Decimal("120.0"),
        ),
    )
    payload = facture.to_api_payload()

    assert "modeDepot" in payload
    assert payload["modeDepot"] == "DEPOT_PDF_API"
    assert "numeroFactureSaisi" in payload
    assert "destinataire" in payload
    assert payload["destinataire"]["codeDestinataire"] == "123456789"
    assert payload["destinataire"]["codeServiceExecutant"] == "RH"
    assert "fournisseur" in payload
    assert payload["fournisseur"]["idFournisseur"] == 9876
    # Vérifie qu'un champ non défini n'est pas dans le payload
    assert "commentaire" not in payload


def test_creation_facture_facturx():
    """Teste la création d'une instance de FactureFacturX avec les champs requis."""
    facture = FactureFacturX(
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
            nom="Mon Entreprise SAS",
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
            montant_ht_total=Decimal("1000.0"),
            montant_tva=Decimal("200.0"),
            montant_ttc_total=Decimal("1200.0"),
            montant_a_payer=Decimal("1200.0"),
        ),
    )
    assert facture.numero_facture == "FX-2024-001"
    assert facture.destinataire.nom == "Client Principal SA"
    assert facture.references.devise_facture == "EUR"  # Vérifie la valeur par défaut


def test_conversion_facturx_to_chorus():
    """Teste la conversion d'un modèle FacturFacturX vers FactureChorus."""
    facturx_invoice = FactureFacturX(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FX-2024-001",
        date_facture="2024-10-18",
        date_echeance_paiement="2024-11-18",  # Ce champ ne doit pas être transféré
        destinataire=Destinataire(code_destinataire="123"),
        fournisseur=Fournisseur(id_fournisseur=456),
        cadre_de_facturation=CadreDeFacturation(
            code_cadre_facturation=CodeCadreFacturation.A1_FACTURE_FOURNISSEUR
        ),
        references=References(
            type_facture=TypeFacture.FACTURE,
            type_tva=TypeTVA.SUR_DEBIT,
            mode_paiement=ModePaiement.VIREMENT,
        ),
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1"),
            montant_tva=Decimal("1"),
            montant_ttc_total=Decimal("1"),
            montant_a_payer=Decimal("1"),
        ),
    )

    chorus_invoice = FactureChorus(
        **facturx_invoice.model_dump(
            exclude={"numero_facture", "date_echeance_paiement"}
        ),
        numero_facture_saisi=facturx_invoice.numero_facture,
    )

    assert chorus_invoice.numero_facture_saisi == "FX-2024-001"
    assert chorus_invoice.date_facture == "2024-10-18"
    assert chorus_invoice.destinataire.code_destinataire == "123"
    assert not hasattr(chorus_invoice, "date_echeance_paiement")
