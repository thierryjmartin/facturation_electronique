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
    AdresseElectronique,
)
from facture_electronique.utils.facturx import (
    _get_facturx_type_code,
    _float_vers_decimal_facturx,
    _parse_date_chorus_vers_facturx,
    _GenerateurXML,  # Pour les tests de bas niveau si besoin
    gen_xml_depuis_facture,
    valider_xml_facturx_schematron,
    ProfilFacturX,
)
from facture_electronique.exceptions import XSLTValidationError


@pytest.fixture
def sample_facture() -> FactureFacturX:
    """Fournit un objet FactureFacturX standard pour les tests."""
    return FactureFacturX(
        mode_depot=ModeDepot.DEPOT_PDF_API,
        numero_facture="FA-2024-001",
        date_facture="2024-10-26",
        date_echeance_paiement="2024-11-26",
        destinataire=Destinataire(
            adresse_electronique=AdresseElectronique(identifiant="12345678901234"),
            nom="Acheteur SA",
            adresse_postale=AdressePostale(pays_code_iso="FR"),
        ),
        fournisseur=Fournisseur(
            id_fournisseur=123,
            adresse_electronique=AdresseElectronique(identifiant="11122233300011"),
            nom="Vendeur SAS",
            numero_tva_intra="FR12111222333",
            iban="FR7630006000011234567890189",
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
                reference="REF001",
                quantite=Decimal(10),
                unite="pce",
                montant_unitaire_ht=Decimal("100.0"),
                categorie_tva=CategorieTVA.STANDARD,
                taux_tva_manuel=Decimal(20.0),
            )
        ],
        lignes_de_tva=[
            LigneDeTVA(
                montant_base_ht=Decimal("1000.0"),
                montant_tva=Decimal("200.0"),
                categorie=CategorieTVA.STANDARD,
                taux_manuel=Decimal(20.0),
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
    """Teste la génération du code de type de facture."""
    assert _get_facturx_type_code(sample_facture) == "380"
    sample_facture.references.type_facture = TypeFacture.AVOIR
    assert _get_facturx_type_code(sample_facture) == "381"


def test_mode_paiement_to_facturx_code(sample_facture):
    """Teste la génération du code de mode de paiement depuis l'Enum."""
    sample_facture.references.mode_paiement = ModePaiement.VIREMENT
    assert sample_facture.get_facturx_mode_paiement_code() == "30"
    sample_facture.references.mode_paiement = ModePaiement.CHEQUE
    assert sample_facture.get_facturx_mode_paiement_code() == "20"


def test_float_vers_decimal_facturx():
    """Teste la conversion de float vers Decimal."""
    assert _float_vers_decimal_facturx(123.456) == Decimal("123.46")
    assert _float_vers_decimal_facturx(100.0) == Decimal("100.00")
    assert _float_vers_decimal_facturx(Decimal("123.456")) == Decimal("123.46")


def test_parse_date_chorus_vers_facturx():
    """Teste la conversion du format de date."""
    assert _parse_date_chorus_vers_facturx("2024-10-26") == "20241026"


def test_gen_facturx_en16931_structure(sample_facture):
    """Teste la structure principale de l'objet EN16931 généré."""
    # --- MODIFICATION 2 : Utilisation du générateur interne ---
    generateur = _GenerateurXML(sample_facture)
    facturx_obj = generateur.generer_objet_xml(ProfilFacturX.EN16931)

    # Les assertions restent les mêmes...
    assert facturx_obj.exchanged_document.id.value == "FA-2024-001"
    summation = facturx_obj.supply_chain_trade_transaction.applicable_header_trade_settlement.specified_trade_settlement_header_monetary_summation
    assert summation.grand_total_amount.value == Decimal("1200.00")
    lines = facturx_obj.supply_chain_trade_transaction.included_supply_chain_trade_line_item
    assert lines[0].specified_trade_product.name.value == "REF001 Produit 1"


def test_gen_xml_depuis_facture(sample_facture):
    """Teste que la génération XML produit une chaîne de caractères valide."""
    generateur = _GenerateurXML(sample_facture)
    facturx_obj = generateur.generer_objet_xml(ProfilFacturX.EN16931)
    xml_output = gen_xml_depuis_facture(facturx_obj)

    # Les assertions restent les mêmes...
    assert isinstance(xml_output, str)
    assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_output
    assert "<ram:GrandTotalAmount>1200.00</ram:GrandTotalAmount>" in xml_output


def test_valider_xml_facturx_schematron_tous_profils(sample_facture):
    """Teste la validation XSLT pour tous les profils Factur-X."""

    # --- MODIFICATION 3 : Utilisation de la nouvelle API fluide pour les tests ---
    # Cela rend les tests plus lisibles et alignés sur l'usage de la librairie.
    for profil in ProfilFacturX:
        with sample_facture.generer_facturx(profil=profil) as constructeur:
            xml_str = constructeur.xml_str
            # La validation se fait maintenant via la fonction qui prend l'Enum
            assert valider_xml_facturx_schematron(xml_str, profil) is True


def test_intercepter_xslt_validation_error(sample_facture):
    """
    Teste la levée correcte de XSLTValidationError pour un XML invalide.
    """
    invalid_facture = sample_facture.model_copy(deep=True)
    invalid_facture.numero_facture = ""  # Champ obligatoire manquant

    with pytest.raises(XSLTValidationError) as excinfo:
        # On utilise la nouvelle API pour générer le XML invalide
        with invalid_facture.generer_facturx(profil=ProfilFacturX.EN16931) as constructeur:
            xml_invalide = constructeur.xml_str
            valider_xml_facturx_schematron(xml_invalide, ProfilFacturX.EN16931)

    # Optionnel: vérifier que le message d'erreur contient des informations pertinentes
    assert "[BR-02]-An Invoice shall have an Invoice number (BT-1)" in str(excinfo.value)
    assert "ram:ID" in str(excinfo.value)
