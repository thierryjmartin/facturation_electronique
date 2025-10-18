from __future__ import annotations
import typing
import re
import copy
from datetime import datetime
from decimal import Decimal
from enum import Enum
from types import ModuleType
from typing import Union
from importlib import resources

from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from saxonche import PySaxonProcessor

from ..generated.factur_x_1_07_03 import (
    factur_x_minimum,
    factur_x_basic,
    factur_x_en16931,
    factur_x_extended,
)
from ..exceptions import InvalidDataFacturxError, XSLTValidationError

if typing.TYPE_CHECKING:
    from ..models import FactureFacturX, LigneDePoste, LigneDeTVA


# --- Étape 1 : La nouvelle Enum centralise TOUTE la configuration ---
class ProfilFacturX(Enum):
    """
    Enumération des profils Factur-X supportés, centralisant leur configuration.
    """

    MINIMUM = (
        "factur-x-minimum",
        "urn:factur-x.eu:1p0:minimum",
        factur_x_minimum,
        "facture_electronique.xsd.facturx-minimum._XSLT_MINIMUM",
        "FACTUR-X_MINIMUM.xslt",
    )
    BASIC = (
        "factur-x-basic",
        "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic",
        factur_x_basic,
        "facture_electronique.xsd.facturx-basic._XSLT_BASIC",
        "FACTUR-X_BASIC.xslt",
    )
    EN16931 = (
        "factur-x-en16931",
        "urn:cen.eu:en16931:2017",
        factur_x_en16931,
        "facture_electronique.xsd.facturx-EN16931._XSLT_EN16931",
        "FACTUR-X_EN16931.xslt",
    )
    EXTENDED = (
        "factur-x-extended",
        "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended",
        factur_x_extended,
        "facture_electronique.xsd.facturx-extended._XSLT_EXTENDED",
        "FACTUR-X_EXTENDED.xslt",
    )

    def __init__(self, id_str, urn, module, chemin_ressource_xslt, nom_fichier_xslt):
        self.id_str = id_str
        self.urn = urn
        self.module = module
        self.chemin_ressource_xslt = chemin_ressource_xslt
        self.nom_fichier_xslt = nom_fichier_xslt


# --- Nouvelle classe interne pour orchestrer la génération XML ---
class _GenerateurXML:
    """Génère un objet XML Factur-X à partir d'un objet de données FactureFacturX."""

    def __init__(self, facture: FactureFacturX):
        self.facture = facture

    def generer_objet_xml(self, profil: ProfilFacturX):
        """Orchestre la génération de l'objet XML."""
        _valider_pre_generation(self.facture, profil)

        if profil == ProfilFacturX.MINIMUM:
            return _gen_facturx_minimum(self.facture)
        else:
            return _gen_facturx_profil_complexe(self.facture, profil)


# --- Fonctions de bas niveau (votre logique existante, maintenant privée) ---


def _float_vers_decimal_facturx(value: Union[float, Decimal]) -> Decimal:
    """Convertit un float ou un Decimal en Decimal avec 2 décimales pour factur-x."""
    return Decimal("%.2f" % value)


def _parse_date_chorus_vers_facturx(date_str: str) -> str:
    """Convertit une date au format YYYY-MM-DD vers le format YYYYMMDD."""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")


def _get_facturx_type_code(facture: FactureFacturX) -> str:
    """Détermine le code de type de document Factur-X (380 pour facture, 381 pour avoir)."""
    return facture.get_facturx_type_code()


def _get_facturx_mode_paiement_code(facture: FactureFacturX) -> str:
    """Traduit le mode de paiement en code Factur-X standard."""
    return facture.get_facturx_mode_paiement_code()


def _get_facturx_quantity_units(unite: str) -> str:
    """Traduit une unité de quantité en code UN/ECE standard pour Factur-X."""
    equiv = {"lot": "C62", "Kg": "KGM", "L": "LTR", "m": "MTR", "m3": "MTQ", "t": "TNE"}
    return equiv.get(unite, "C62")


def _gen_applicable_header_trade_agreement(facturx_module, facture: FactureFacturX):
    """Génère la section `ApplicableHeaderTradeAgreement` du XML Factur-X."""
    return facturx_module.HeaderTradeAgreementType(
        buyer_reference=facturx_module.TextType(value=facture.destinataire.code_service_executant),
        seller_trade_party=facturx_module.TradePartyType(
            name=facturx_module.TextType(value=facture.fournisseur.nom),
            specified_legal_organization=facturx_module.LegalOrganizationType(
                id=facturx_module.Idtype(
                    scheme_id=facture.fournisseur.adresse_electronique.scheme_id,
                    value=facture.fournisseur.adresse_electronique.identifiant,
                )
            ),
            postal_trade_address=facturx_module.TradeAddressType(
                country_id=facturx_module.CountryIdtype(
                    value=facture.fournisseur.adresse_postale.pays_code_iso
                )
            ),
            specified_tax_registration=[
                facturx_module.TaxRegistrationType(
                    id=facturx_module.Idtype(
                        scheme_id="VA", value=facture.fournisseur.numero_tva_intra
                    )
                )
            ],
        ),
        buyer_trade_party=facturx_module.TradePartyType(
            name=facturx_module.TextType(value=facture.destinataire.nom),
            specified_legal_organization=facturx_module.LegalOrganizationType(
                id=facturx_module.Idtype(
                    scheme_id=facture.destinataire.adresse_electronique.scheme_id,
                    value=facture.destinataire.adresse_electronique.identifiant,
                )
            ),
            postal_trade_address=facturx_module.TradeAddressType(
                country_id=facturx_module.CountryIdtype(
                    value=facture.destinataire.adresse_postale.pays_code_iso
                )
            ),
        ),
        buyer_order_referenced_document=facturx_module.ReferencedDocumentType(
            issuer_assigned_id=facturx_module.Idtype(value=facture.references.numero_bon_commande)
        ),
    )


def _gen_facturx_minimum(facture: FactureFacturX):
    """Génère un objet XML Factur-X conforme au profil MINIMUM."""
    module = ProfilFacturX.MINIMUM.module
    exchanged_document_context = module.ExchangedDocumentContextType(
        guideline_specified_document_context_parameter=module.DocumentContextParameterType(
            id=module.Idtype(value=ProfilFacturX.MINIMUM.urn)
        )
    )
    exchanged_document = module.ExchangedDocumentType(
        id=module.Idtype(value=facture.numero_facture),
        type_code=module.DocumentCodeType(value=_get_facturx_type_code(facture)),
        issue_date_time=module.DateTimeType(
            date_time_string=module.DateTimeType.DateTimeString(
                value=_parse_date_chorus_vers_facturx(facture.date_facture),
                format="102",
            )
        ),
    )
    supply_chain_trade_transaction = module.SupplyChainTradeTransactionType(
        applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(module, facture),
        applicable_header_trade_delivery=module.HeaderTradeDeliveryType(),
        applicable_header_trade_settlement=module.HeaderTradeSettlementType(
            invoice_currency_code=module.CurrencyCodeType(value=facture.references.devise_facture),
            specified_trade_settlement_header_monetary_summation=module.TradeSettlementHeaderMonetarySummationType(
                tax_basis_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_ht_total)
                ),
                tax_total_amount=[
                    module.AmountType(
                        value=_float_vers_decimal_facturx(facture.montant_total.montant_tva),
                        currency_id=facture.references.devise_facture,
                    )
                ],
                grand_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_ttc_total)
                ),
                due_payable_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_a_payer)
                ),
            ),
        ),
    )
    return module.CrossIndustryInvoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )


def _ligne_poste_facturx(ligne: LigneDePoste, facture: FactureFacturX, module: ModuleType):
    """Génère une ligne de facture (`SupplyChainTradeLineItem`)."""
    date_debut_retenue = ligne.date_debut_periode or facture.date_facture
    date_fin_retenue = ligne.date_fin_periode or ligne.date_debut_periode or facture.date_facture

    trade_allowance_charge = None
    trade_allowance_charge_trade_agreement = None
    if ligne.montant_remise_ht:
        trade_allowance_charge = module.TradeAllowanceChargeType(
            charge_indicator=module.IndicatorType(indicator=False),
            actual_amount=module.AmountType(
                value=_float_vers_decimal_facturx(
                    ligne.montant_remise_ht * Decimal(str(ligne.quantite))
                )
            ),
        )

        trade_allowance_charge_trade_agreement = copy.deepcopy(trade_allowance_charge)
        trade_allowance_charge_trade_agreement.actual_amount.value = _float_vers_decimal_facturx(
            ligne.montant_remise_ht
        )

        if ligne.code_raison_reduction:
            trade_allowance_charge.reason_code = module.AllowanceChargeReasonCodeType(
                value=ligne.code_raison_reduction
            )
        if ligne.raison_reduction:
            trade_allowance_charge.reason = module.TextType(value=ligne.raison_reduction)

    ligne_unit_code = _get_facturx_quantity_units(ligne.unite)

    return module.SupplyChainTradeLineItemType(
        associated_document_line_document=module.DocumentLineDocumentType(
            line_id=module.Idtype(value=str(ligne.numero))
        ),
        specified_trade_product=module.TradeProductType(
            name=module.TextType(value=(ligne.reference or "") + " " + ligne.denomination)
        ),
        specified_line_trade_agreement=module.LineTradeAgreementType(
            gross_price_product_trade_price=module.TradePriceType(
                charge_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(ligne.montant_unitaire_ht)
                ),
                basis_quantity=module.QuantityType(
                    value=_float_vers_decimal_facturx(
                        Decimal(1.0)
                    ),  # La base de prix est toujours pour une unité
                    unit_code=ligne_unit_code,
                ),
                applied_trade_allowance_charge=trade_allowance_charge_trade_agreement
                if trade_allowance_charge_trade_agreement
                else None,
            ),
            net_price_product_trade_price=module.TradePriceType(
                charge_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(
                        ligne.montant_unitaire_ht - (ligne.montant_remise_ht or 0)
                    )
                ),
            ),
        ),
        specified_line_trade_delivery=module.LineTradeDeliveryType(
            billed_quantity=module.QuantityType(
                value=_float_vers_decimal_facturx(ligne.quantite),
                unit_code=ligne_unit_code,
            )
        ),
        specified_line_trade_settlement=module.LineTradeSettlementType(
            applicable_trade_tax=module.TradeTaxType(
                type_code=module.TaxTypeCodeType(value="VAT"),
                category_code=module.TaxCategoryCodeType(value=ligne.categorie_tva),
                rate_applicable_percent=module.PercentType(
                    value=_float_vers_decimal_facturx(ligne.taux_tva_manuel)
                ),
            ),
            billing_specified_period=module.SpecifiedPeriodType(
                start_date_time=module.DateTimeType(
                    date_time_string=module.DateTimeType.DateTimeString(
                        value=_parse_date_chorus_vers_facturx(date_debut_retenue),
                        format="102",
                    )
                ),
                end_date_time=module.DateTimeType(
                    date_time_string=module.DateTimeType.DateTimeString(
                        value=_parse_date_chorus_vers_facturx(date_fin_retenue),
                        format="102",
                    )
                ),
            ),
            specified_trade_allowance_charge=[
                trade_allowance_charge,
            ]
            if trade_allowance_charge
            else None,
            specified_trade_settlement_line_monetary_summation=module.TradeSettlementLineMonetarySummationType(
                line_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(
                        (ligne.montant_unitaire_ht - (ligne.montant_remise_ht or 0))
                        * Decimal(str(ligne.quantite))
                    )
                ),
            ),
        ),
    )


def _ligne_tva_facturx(ligne_tva: LigneDeTVA, module: ModuleType):
    """Génère une ligne de TVA (`TradeTax`) pour le résumé de la facture."""
    return module.TradeTaxType(
        calculated_amount=module.AmountType(
            value=_float_vers_decimal_facturx(ligne_tva.montant_tva)
        ),
        type_code=module.TaxTypeCodeType(value="VAT"),
        basis_amount=module.AmountType(
            value=_float_vers_decimal_facturx(ligne_tva.montant_base_ht)
        ),
        category_code=module.TaxCategoryCodeType(value=ligne_tva.categorie),
        rate_applicable_percent=module.PercentType(
            value=_float_vers_decimal_facturx(ligne_tva.taux_manuel)
        ),
    )


def _gen_facturx_profil_complexe(facture: FactureFacturX, profil: ProfilFacturX):
    """Génère un objet XML Factur-X pour les profils BASIC, EN16931 ou EXTENDED."""
    module = profil.module
    exchanged_document_context = module.ExchangedDocumentContextType(
        guideline_specified_document_context_parameter=module.DocumentContextParameterType(
            id=module.Idtype(value=profil.urn)
        )
    )
    exchanged_document = module.ExchangedDocumentType(
        id=module.Idtype(value=facture.numero_facture),
        type_code=module.DocumentCodeType(value=_get_facturx_type_code(facture)),
        issue_date_time=module.DateTimeType(
            date_time_string=module.DateTimeType.DateTimeString(
                value=_parse_date_chorus_vers_facturx(facture.date_facture),
                format="102",
            )
        ),
    )
    supply_chain_trade_transaction = module.SupplyChainTradeTransactionType(
        included_supply_chain_trade_line_item=[
            _ligne_poste_facturx(ligne, facture, module) for ligne in facture.lignes_de_poste
        ],
        applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(module, facture),
        applicable_header_trade_delivery=module.HeaderTradeDeliveryType(),
        applicable_header_trade_settlement=module.HeaderTradeSettlementType(
            creditor_reference_id=module.Idtype(),
            payment_reference=module.TextType(),
            # tax_currency_code=factur_x_module.CurrencyCodeType(value=facture.references.devise_facture),
            # payee_trade_party=factur_x_module.TradePartyType(), utile si le bénéficiare est différent du fournisseur
            specified_trade_settlement_payment_means=[
                module.TradeSettlementPaymentMeansType(
                    type_code=module.PaymentMeansCodeType(
                        value=_get_facturx_mode_paiement_code(facture)
                    ),
                    # payer_party_debtor_financial_account=module.DebtorFinancialAccountType(ibanid=),
                    payee_party_creditor_financial_account=module.CreditorFinancialAccountType(
                        ibanid=facture.fournisseur.iban,
                        # proprietary_id=,
                    ),
                ),
            ],
            applicable_trade_tax=[
                _ligne_tva_facturx(ligne_tva, module) for ligne_tva in facture.lignes_de_tva
            ],
            # billing_specified_period=module.SpecifiedPeriodType(),
            # specified_trade_allowance_charge=[module.TradeAllowanceChargeType(
            # charge_indicator=module.IndicatorType(indicator=False),
            # actual_amount=module.AmountType(value=format_decimal % facture.montant_total.montant_remise_globale_ttc),
            # reason=module.TextType(value=facture.montant_total.motif_remise_globale_ttc),
            # category_trade_tax=module.TradeTaxType(
            # type_code=module.TaxTypeCodeType("VAT"),
            # category_code=module.TaxCategoryCodeType(value=CategorieTVA.tva_cat_S),
            # rate_applicable_percent=module.PercentType(value=format_decimal % facture.lignes_de_tva[0].taux_manuel)
            # )
            # ),],
            specified_trade_payment_terms=module.TradePaymentTermsType(
                due_date_date_time=module.DateTimeType(
                    date_time_string=module.DateTimeType.DateTimeString(
                        format="102",
                        value=_parse_date_chorus_vers_facturx(facture.date_echeance_paiement),
                    )
                ),
            ),
            invoice_currency_code=module.CurrencyCodeType(value=facture.references.devise_facture),
            # invoice_referenced_document=[factur_x_module.ReferencedDocumentType(),], # Numéro de facture antérieure ?
            # receivable_specified_trade_accounting_account=factur_x_module.TradeAccountingAccountType(),
            specified_trade_settlement_header_monetary_summation=module.TradeSettlementHeaderMonetarySummationType(
                line_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_ht_total)
                ),
                allowance_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(
                        (facture.montant_total.montant_remise_globale_ttc or 0)
                    )
                ),
                tax_basis_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_ht_total)
                ),
                tax_total_amount=[
                    module.AmountType(
                        value=_float_vers_decimal_facturx(facture.montant_total.montant_tva),
                        currency_id=facture.references.devise_facture,
                    ),
                ],
                grand_total_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_ttc_total)
                ),
                total_prepaid_amount=module.AmountType(
                    value=_float_vers_decimal_facturx((facture.montant_total.acompte or 0))
                ),
                due_payable_amount=module.AmountType(
                    value=_float_vers_decimal_facturx(facture.montant_total.montant_a_payer)
                ),
            ),
        ),
    )
    return module.CrossIndustryInvoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )


def _valider_pre_generation(facture: FactureFacturX, profil: ProfilFacturX):
    """Vérifie les contraintes métier avant de commencer la génération."""
    if profil in (ProfilFacturX.BASIC, ProfilFacturX.EN16931, ProfilFacturX.EXTENDED):
        if facture.montant_total.montant_remise_globale_ttc:
            raise InvalidDataFacturxError(
                "Une remise TTC globale n'est pas supportée pour ce profil."
            )


# --- Fonctions publiques de sérialisation et validation ---
def gen_xml_depuis_facture(facture_obj) -> str:
    """Sérialise un objet de facture (généré par xsdata) en une chaîne XML."""
    nsmap = {
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
        "qdt": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
        "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    }
    config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(context=XmlContext(), config=config)
    return serializer.render(facture_obj, ns_map=nsmap)


REGEX_ASSERTION_ECHOUEE_SVRL = re.compile(
    r"""
	<svrl:failed-assert          # Balise d'ouverture
	\s+
	test="([^"]+)"               # Groupe 1: Capture la valeur de l'attribut 'test'
	\s+
	id="([^"]+)"                 # Groupe 2: Capture la valeur de l'attribut 'id'
	\s+
	location="([^"]+)"           # Groupe 3: Capture la valeur de l'attribut 'location'
	>
	\s*
	<svrl:text>
	\s*
	([^<]+)                      # Groupe 4: Capture le contenu textuel de l'erreur
	\s*
	</svrl:text>                 # Balise de fermeture (sans échappement redondant)
	""",
    re.VERBOSE,
)


def valider_xml_facturx_schematron(xml_data: str, profil: ProfilFacturX) -> bool:
    """Valide un XML Factur-X en utilisant le Schematron approprié."""
    try:
        ref_xslt = resources.files(profil.chemin_ressource_xslt).joinpath(profil.nom_fichier_xslt)
    except (ModuleNotFoundError, FileNotFoundError) as e:
        raise FileNotFoundError(
            f"Ressource XSLT introuvable pour le profil '{profil.name}'. Erreur: {e}"
        )

    with resources.as_file(ref_xslt) as chemin_xslt_physique:
        with PySaxonProcessor(license=False) as proc:
            xsltproc = proc.new_xslt30_processor()
            document = proc.parse_xml(xml_text=xml_data)
            executable = xsltproc.compile_stylesheet(
                stylesheet_file=str(chemin_xslt_physique),
                base_uri=chemin_xslt_physique.parent.as_uri(),
            )
            output = executable.transform_to_string(xdm_node=document)
            matches = REGEX_ASSERTION_ECHOUEE_SVRL.findall(output)
            if matches:
                messages_erreur = [
                    f"Test: {test}\nLocation: {loc}\nMessage: {msg.strip()}"
                    for test, id_err, loc, msg in matches
                ]
                raise XSLTValidationError(messages_erreur)
    return True
