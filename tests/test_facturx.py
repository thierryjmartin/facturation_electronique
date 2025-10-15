import pytest
from decimal import Decimal
from facture_electronique.models import (
    FactureFacturX,
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
    ModeDepot,
)
from facture_electronique.utils.facturx import (
    get_facturx_type_code,
    get_facturx_mode_paiement,
    _float_vers_decimal_facturx,
    _parse_date_chorus_vers_facturx,
    gen_facturx_en16931,
    gen_xml_depuis_facture,
    valider_xml_xldt,
    chemin_xldt_minimum,
    chemin_xldt_basic,
    chemin_xldt_en16931,
)
from facture_electronique.exceptions import XSLTValidationError


@pytest.fixture
def sample_facture() -> FactureFacturX:
    """Provides a sample FactureFacturX object for testing."""
    return FactureFacturX(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FA-2024-001",
        date_facture="2024-10-26",
        date_echeance_paiement="2024-11-26",
        destinataire=Destinataire(
            code_destinataire="12345678901234",
            nom="Acheteur SA",
            adresse_postale=AdressePostale(pays_code_iso="FR"),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=123,
            nom="Vendeur SAS",
            siret="11122233300011",
            numero_tva_intra="FR12111222333",
            adresse_postale=AdressePostale(pays_code_iso="FR"),
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
                denomination="Produit 1",
                quantite=10,
                unite="pce",
                montant_unitaire_ht=Decimal("100.0"),
                categorie_tva=CategorieTVA.STANDARD,
                taux_tva_manuel=20.0,
            )
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("1000.0"),
                montant_tva=Decimal("200.0"),
                categorie=CategorieTVA.STANDARD,
                taux_manuel=20.0,
            )
        ],
        montant_total=MontantTotal(
            montant_ht_total=Decimal("1000.0"),
            montant_tva=Decimal("200.0"),
            montant_ttc_total=Decimal("1200.0"),
            montant_a_payer=Decimal("1200.0"),
        ),
    )


def test_get_facturx_type_code(sample_facture):
    """Tests the invoice type code generation."""
    assert get_facturx_type_code(sample_facture) == "380"
    sample_facture.references.type_facture = TypeFacture.AVOIR
    assert get_facturx_type_code(sample_facture) == "381"


def test_get_facturx_mode_paiement(sample_facture):
    """Tests the payment mode code generation."""
    sample_facture.references.mode_paiement = ModePaiement.VIREMENT
    assert get_facturx_mode_paiement(sample_facture) == "30"
    sample_facture.references.mode_paiement = ModePaiement.CHEQUE
    assert get_facturx_mode_paiement(sample_facture) == "20"


def test_float_vers_decimal_facturx():
    """Tests the float to Decimal conversion."""
    assert _float_vers_decimal_facturx(123.456) == Decimal("123.46")
    assert _float_vers_decimal_facturx(100.0) == Decimal("100.00")
    assert _float_vers_decimal_facturx(Decimal("123.456")) == Decimal("123.46")


def test_parse_date_chorus_vers_facturx():
    """Tests the date format conversion."""
    assert _parse_date_chorus_vers_facturx("2024-10-26") == "20241026"


def test_gen_facturx_en16931_structure(sample_facture):
    """Tests the main structure of the generated EN16931 object."""
    facturx_obj = gen_facturx_en16931(sample_facture)

    # Check root element
    assert facturx_obj.exchanged_document is not None
    assert facturx_obj.supply_chain_trade_transaction is not None

    # Check document ID and date
    assert facturx_obj.exchanged_document.id.value == "FA-2024-001"
    assert (
        facturx_obj.exchanged_document.issue_date_time.date_time_string.value
        == "20241026"
    )

    # Check amounts
    summation = facturx_obj.supply_chain_trade_transaction.applicable_header_trade_settlement.specified_trade_settlement_header_monetary_summation
    assert summation.tax_basis_total_amount.value == Decimal("1000.00")
    assert summation.grand_total_amount.value == Decimal("1200.00")

    # Check line items
    lines = (
        facturx_obj.supply_chain_trade_transaction.included_supply_chain_trade_line_item
    )
    assert len(lines) == 1
    assert lines[0].associated_document_line_document.line_id.value == "1"
    # The sample line has no 'reference', so (ligne.reference or "") results in a leading space
    assert lines[0].specified_trade_product.name.value == " Produit 1"


def test_gen_xml_depuis_facture(sample_facture):
    """Tests that the XML generation produces a valid XML string."""
    facturx_obj = gen_facturx_en16931(sample_facture)
    xml_output = gen_xml_depuis_facture(facturx_obj)

    assert isinstance(xml_output, str)
    assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_output
    assert "<rsm:CrossIndustryInvoice" in xml_output
    assert "<ram:GrandTotalAmount>1200.00</ram:GrandTotalAmount>" in xml_output
    assert "</rsm:CrossIndustryInvoice>" in xml_output


def test_valider_xml_xldt(sample_facture):
    """Tests the XSLT validation for all Factur-X profiles."""
    # Test MINIMUM profile
    facturx_min_obj = sample_facture.to_facturx_minimum()
    xml_min_output = gen_xml_depuis_facture(facturx_min_obj)
    assert valider_xml_xldt(xml_min_output, chemin_xldt_minimum) is False

    # Test BASIC profile
    facturx_basic_obj = sample_facture.to_facturx_basic()
    xml_basic_output = gen_xml_depuis_facture(facturx_basic_obj)
    assert valider_xml_xldt(xml_basic_output, chemin_xldt_basic) is False

    # Test EN16931 profile
    facturx_en16931_obj = sample_facture.to_facturx_en16931()
    xml_en16931_output = gen_xml_depuis_facture(facturx_en16931_obj)
    assert valider_xml_xldt(xml_en16931_output, chemin_xldt_en16931) is False

    # Test for an invalid XML
    # Let's break the XML by removing the invoice number, which is mandatory
    invalid_facture = sample_facture.model_copy(deep=True)
    invalid_facture.numero_facture = ""
    facturx_invalid_obj = invalid_facture.to_facturx_en16931()
    xml_invalid_output = gen_xml_depuis_facture(facturx_invalid_obj)
    with pytest.raises(XSLTValidationError):
        valider_xml_xldt(xml_invalid_output, chemin_xldt_en16931)
