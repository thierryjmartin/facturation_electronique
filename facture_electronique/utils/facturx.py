import re
import copy
from datetime import datetime
from decimal import Decimal
from types import ModuleType
from typing import Literal, Union, Final
from importlib import resources
from saxonche import PySaxonProcessor

from ..models import FactureFacturX, TypeFacture, LigneDePoste, LigneDeTVA
from ..generated.factur_x_1_07_03 import (
    factur_x_minimum,
    factur_x_basic,
    factur_x_en16931,
    factur_x_extended,
)
from ..exceptions import InvalidDataFacturxError, XSLTValidationError

FACTURX_MINIMUM: Final = "factur-x-minimum"
FACTURX_BASIC: Final = "factur-x-basic"
FACTURX_EN16931: Final = "factur-x-en16931"
FACTURX_EXTENDED: Final = "factur-x-extended"
ProfilFacturX = Literal[FACTURX_BASIC, FACTURX_EN16931, FACTURX_EXTENDED]


def get_factur_x_module(profil_facturx: ProfilFacturX) -> ModuleType:
    """Retourne le module Factur-X correspondant au profil demandé."""

    correspondance_modules = {
        FACTURX_BASIC: factur_x_basic,
        FACTURX_EN16931: factur_x_en16931,
        FACTURX_EXTENDED: factur_x_extended,
    }

    module_selectionne = correspondance_modules.get(profil_facturx)

    if not module_selectionne:
        # Le message d'erreur est internationalisé et formaté de manière sûre.
        message_erreur = "Profil Factur-X invalide : '{profil}'. Les profils attendus sont '{basic}', '{en16931} ou '{extended}'.".format(
            profil=profil_facturx,
            basic=FACTURX_BASIC,
            en16931=FACTURX_EN16931,
            extended=FACTURX_EXTENDED,
        )
        raise ValueError(message_erreur)

    return module_selectionne


def _float_vers_decimal_facturx(value: Union[float, Decimal]) -> Decimal:
    """convertit un float ou un Decimal en Decimal avec 2 décimales pour factur-x"""
    format_decimal = "%.2f"
    return Decimal(format_decimal % value)


def _parse_date_chorus_vers_facturx(date_str: str) -> str:
    """convertit une date au format chorus pro vers le format factur-x"""
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")


def get_facturx_type_code(facture: FactureFacturX) -> str:
    """Détermine le code de type de document Factur-X (380 pour facture, 381 for avoir)."""
    if facture.references.type_facture == TypeFacture.AVOIR:
        return "381"
    else:
        return "380"


def get_facturx_quantity_units(unite: str) -> str:
    """Traduit une unité de quantité en code UN/ECE standard pour Factur-X."""
    # Unités de mesure recommandées par la norme Factur-X
    equiv = {
        "lot": "C62",  # Unité
        "Kg": "KGM",  # Kilogramme
        "L": "LTR",  # Litre
        "m": "MTR",  # Mètre
        "m3": "MTQ",  # Mètre cube
        "t": "TNE",  # Tonne
    }
    try:
        return equiv[unite]
    except KeyError:
        return "C62"  # Retourne "Unité" par défaut si non trouvé


def _gen_applicable_header_trade_agreement(facturx, facture):
    """Génère la section `ApplicableHeaderTradeAgreement` du XML Factur-X."""
    return facturx.HeaderTradeAgreementType(
        buyer_reference=facturx.TextType(
            value=facture.destinataire.code_service_executant
        ),
        seller_trade_party=facturx.TradePartyType(
            name=facturx.TextType(value=facture.fournisseur.nom),
            specified_legal_organization=facturx.LegalOrganizationType(
                id=facturx.Idtype(scheme_id="0002", value=facture.fournisseur.siret)
            ),
            postal_trade_address=facturx.TradeAddressType(
                country_id=facturx.CountryIdtype(
                    value=facture.fournisseur.adresse_postale.pays_code_iso
                )
            ),
            specified_tax_registration=[
                facturx.TaxRegistrationType(
                    id=facturx.Idtype(
                        scheme_id="VA",
                        value=facture.fournisseur.numero_tva_intra,
                    )
                ),
            ],
        ),
        buyer_trade_party=facturx.TradePartyType(
            name=facturx.TextType(value=facture.destinataire.nom),
            specified_legal_organization=facturx.LegalOrganizationType(
                id=facturx.Idtype(
                    scheme_id="0002", value=facture.destinataire.code_destinataire
                )
            ),
            postal_trade_address=facturx.TradeAddressType(
                country_id=facturx.CountryIdtype(
                    value=facture.destinataire.adresse_postale.pays_code_iso
                )
            ),
            # specified_tax_registration=[TaxRegistrationType(), ]
        ),
        buyer_order_referenced_document=facturx.ReferencedDocumentType(
            issuer_assigned_id=facturx.Idtype(
                value=facture.references.numero_bon_commande
            )
        ),
    )


def gen_facturx_minimum(
    facture: FactureFacturX,
) -> factur_x_minimum.CrossIndustryInvoice:
    """Génère un objet XML Factur-X conforme au profil MINIMUM."""
    exchanged_document_context = factur_x_minimum.ExchangedDocumentContextType(
        guideline_specified_document_context_parameter=factur_x_minimum.DocumentContextParameterType(
            id=factur_x_minimum.Idtype(value="urn:factur-x.eu:1p0:minimum")
        )  # urn:factur-x.eu:1p0:minimum
    )
    exchanged_document = factur_x_minimum.ExchangedDocumentType(
        id=factur_x_minimum.Idtype(value=facture.numero_facture),
        type_code=factur_x_minimum.DocumentCodeType(
            value=get_facturx_type_code(facture)
        ),
        issue_date_time=factur_x_minimum.DateTimeType(
            date_time_string=factur_x_minimum.DateTimeType.DateTimeString(
                value=_parse_date_chorus_vers_facturx(facture.date_facture),
                format="102",
            )
        ),
    )
    supply_chain_trade_transaction = factur_x_minimum.SupplyChainTradeTransactionType(
        applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(
            factur_x_minimum, facture
        ),
        applicable_header_trade_delivery=factur_x_minimum.HeaderTradeDeliveryType(),
        applicable_header_trade_settlement=factur_x_minimum.HeaderTradeSettlementType(
            invoice_currency_code=factur_x_minimum.CurrencyCodeType(
                value=facture.references.devise_facture
            ),
            specified_trade_settlement_header_monetary_summation=factur_x_minimum.TradeSettlementHeaderMonetarySummationType(
                tax_basis_total_amount=factur_x_minimum.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_ht_total
                    )
                ),
                tax_total_amount=[
                    factur_x_minimum.AmountType(
                        value=_float_vers_decimal_facturx(
                            facture.montant_total.montant_tva
                        ),
                        currency_id=facture.references.devise_facture,
                    ),
                ],
                grand_total_amount=factur_x_minimum.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_ttc_total
                    )
                ),
                due_payable_amount=factur_x_minimum.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_a_payer
                    )
                ),
            ),
        ),
    )
    f = factur_x_minimum.CrossIndustryInvoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )
    return f


def _ligne_poste_facturx_basic_ou_en16931(
    ligne: LigneDePoste, facture: FactureFacturX, factur_x_module: ModuleType
) -> Union[
    factur_x_basic.SupplyChainTradeLineItemType,
    factur_x_en16931.SupplyChainTradeLineItemType,
]:
    """Génère une ligne de facture (`SupplyChainTradeLineItem`) pour les profils BASIC ou EN16931."""
    date_debut_retenue = ligne.date_debut_periode or facture.date_facture
    date_fin_retenue = (
        ligne.date_fin_periode or ligne.date_debut_periode or facture.date_facture
    )

    trade_allowance_charge = None
    trade_allowance_charge_trade_agreement = None
    if ligne.montant_remise_ht:
        trade_allowance_charge = factur_x_module.TradeAllowanceChargeType(
            charge_indicator=factur_x_module.IndicatorType(indicator=False),
            actual_amount=factur_x_module.AmountType(
                value=_float_vers_decimal_facturx(
                    ligne.montant_remise_ht * Decimal(str(ligne.quantite))
                )
            ),
        )

        rade_allowance_charge_trade_agreement = copy.deepcopy(trade_allowance_charge)
        rade_allowance_charge_trade_agreement.actual_amount.value = (
            _float_vers_decimal_facturx(ligne.montant_remise_ht)
        )

        if ligne.code_raison_reduction:
            trade_allowance_charge.reason_code = (
                factur_x_module.AllowanceChargeReasonCodeType(
                    value=ligne.code_raison_reduction
                )
            )
        if ligne.raison_reduction:
            trade_allowance_charge.reason = factur_x_module.TextType(
                value=ligne.raison_reduction
            )

    ligne_unit_code = get_facturx_quantity_units(ligne.unite)

    suply_chain_trade_line = factur_x_module.SupplyChainTradeLineItemType(
        associated_document_line_document=factur_x_module.DocumentLineDocumentType(
            line_id=factur_x_module.Idtype(value=str(ligne.numero))  # , scheme_id=),
            # included_note = factur_x_module.NoteType(content=, subject_code=),
        ),
        specified_trade_product=factur_x_module.TradeProductType(
            # global_id=factur_x_module.Idtype(value=ligne.reference, scheme_id=''),
            name=factur_x_module.TextType(
                value=(ligne.reference or "") + " " + ligne.denomination
            )
        ),
        specified_line_trade_agreement=factur_x_module.LineTradeAgreementType(
            gross_price_product_trade_price=factur_x_module.TradePriceType(
                charge_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(ligne.montant_unitaire_ht)
                ),
                basis_quantity=factur_x_module.QuantityType(
                    value=_float_vers_decimal_facturx(ligne.quantite),
                    unit_code=ligne_unit_code,
                ),
                applied_trade_allowance_charge=trade_allowance_charge_trade_agreement
                if trade_allowance_charge_trade_agreement
                else None,
            ),
            net_price_product_trade_price=factur_x_module.TradePriceType(
                charge_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        ligne.montant_unitaire_ht - (ligne.montant_remise_ht or 0)
                    )
                ),
                basis_quantity=factur_x_module.QuantityType(
                    value=_float_vers_decimal_facturx(ligne.quantite),
                    unit_code=ligne_unit_code,
                ),
                # applied_trade_allowance_charge=factur_x_module.TradeAllowanceChargeType()
            ),
        ),
        specified_line_trade_delivery=factur_x_module.LineTradeDeliveryType(
            billed_quantity=factur_x_module.QuantityType(
                value=_float_vers_decimal_facturx(ligne.quantite),
                unit_code=ligne_unit_code,
            )
        ),
        specified_line_trade_settlement=factur_x_module.LineTradeSettlementType(
            applicable_trade_tax=factur_x_module.TradeTaxType(
                # calculated_amount=factur_x_module.AmountType(),
                type_code=factur_x_module.TaxTypeCodeType(value="VAT"),
                # exemption_reason=factur_x_module.TextType(),
                # basis_amount=factur_x_module.AmountType(),
                category_code=factur_x_module.TaxCategoryCodeType(
                    value=ligne.categorie_tva
                ),
                # exemption_reason_code=factur_x_module.CodeType(),
                # due_date_type_code=factur_x_module.TimeReferenceCodeType(),
                rate_applicable_percent=factur_x_module.PercentType(
                    value=_float_vers_decimal_facturx(ligne.taux_tva_manuel)
                ),
            ),
            billing_specified_period=factur_x_module.SpecifiedPeriodType(
                start_date_time=factur_x_module.DateTimeType(
                    date_time_string=factur_x_module.DateTimeType.DateTimeString(
                        value=_parse_date_chorus_vers_facturx(date_debut_retenue),
                        format="102",
                    )
                ),
                end_date_time=factur_x_module.DateTimeType(
                    date_time_string=factur_x_module.DateTimeType.DateTimeString(
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
            specified_trade_settlement_line_monetary_summation=factur_x_module.TradeSettlementLineMonetarySummationType(
                line_total_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        ligne.montant_unitaire_ht * Decimal(str(ligne.quantite))
                    )
                ),
            ),
        ),
    )
    return suply_chain_trade_line


def _ligne_tva_facturx_basic_ou_en_16931(
    ligne_tva: LigneDeTVA, factur_x_module: ModuleType
) -> Union[factur_x_basic.TradeTaxType, factur_x_en16931.TradeTaxType]:
    """Génère une ligne de TVA (`TradeTax`) pour les profils BASIC ou EN16931."""
    return factur_x_module.TradeTaxType(
        calculated_amount=factur_x_module.AmountType(
            value=_float_vers_decimal_facturx(ligne_tva.montant_tva)
        ),
        type_code=factur_x_module.TaxTypeCodeType(value="VAT"),
        basis_amount=factur_x_module.AmountType(
            value=_float_vers_decimal_facturx(ligne_tva.montant_base_ht)
        ),
        category_code=factur_x_module.TaxCategoryCodeType(value=ligne_tva.categorie),
        rate_applicable_percent=factur_x_module.PercentType(
            value=_float_vers_decimal_facturx(ligne_tva.taux_manuel)
        ),
    )


def est_valide_pour_facturx_basic(facture: FactureFacturX) -> None:
    """Vérifie si les données de la facture sont compatibles avec le profil BASIC.

    :raises InvalidDataFacturxError: Si une remise globale TTC est présente.
    """
    if facture.montant_total.montant_remise_globale_ttc:
        raise InvalidDataFacturxError(
            "On ne peut pas mettre une remise TTC dans Facturx basic, il faut dispatch la remise sur les différentes lignes."
        )


def gen_facturx_basic_ou_en_16931(
    facture: FactureFacturX, factur_x_module_str: ProfilFacturX
) -> Union[
    factur_x_basic.CrossIndustryInvoice,
    factur_x_en16931.CrossIndustryInvoice,
    factur_x_extended.CrossIndustryInvoice,
]:
    """Génère un objet XML Factur-X pour les profils BASIC ou EN16931 ou EXTENDED."""
    factur_x_module = get_factur_x_module(factur_x_module_str)

    document_context_type_parameter = {
        FACTURX_BASIC: "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic",
        FACTURX_EN16931: "urn:cen.eu:en16931:2017",
        FACTURX_EXTENDED: "urn:cen.eu:en16931:2017#conformant#urn:factur-x.eu:1p0:extended",
    }
    exchanged_document_context = factur_x_module.ExchangedDocumentContextType(
        guideline_specified_document_context_parameter=factur_x_module.DocumentContextParameterType(
            id=factur_x_module.Idtype(
                value=document_context_type_parameter[factur_x_module_str]
            )
        )
    )
    exchanged_document = factur_x_module.ExchangedDocumentType(
        id=factur_x_module.Idtype(value=facture.numero_facture),
        type_code=factur_x_module.DocumentCodeType(
            value=get_facturx_type_code(facture)
        ),
        issue_date_time=factur_x_module.DateTimeType(
            date_time_string=factur_x_module.DateTimeType.DateTimeString(
                value=_parse_date_chorus_vers_facturx(facture.date_facture),
                format="102",
            )
        ),
    )
    supply_chain_trade_transaction = factur_x_module.SupplyChainTradeTransactionType(
        included_supply_chain_trade_line_item=[
            _ligne_poste_facturx_basic_ou_en16931(ligne, facture, factur_x_module)
            for ligne in facture.lignes_de_poste
        ],
        applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(
            factur_x_module, facture
        ),
        applicable_header_trade_delivery=factur_x_module.HeaderTradeDeliveryType(),
        applicable_header_trade_settlement=factur_x_module.HeaderTradeSettlementType(
            creditor_reference_id=factur_x_module.Idtype(),
            payment_reference=factur_x_module.TextType(),
            # tax_currency_code=factur_x_module.CurrencyCodeType(value=facture.references.devise_facture),
            # payee_trade_party=factur_x_module.TradePartyType(), utile si le bénéficiare est différent du fournisseur
            specified_trade_settlement_payment_means=[
                factur_x_module.TradeSettlementPaymentMeansType(
                    type_code=factur_x_module.PaymentMeansCodeType(
                        value=facture.references.mode_paiement.to_facturx_code()
                    ),
                    # payer_party_debtor_financial_account=factur_x_module.DebtorFinancialAccountType(ibanid=),
                    payee_party_creditor_financial_account=factur_x_module.CreditorFinancialAccountType(
                        ibanid=facture.fournisseur.iban,
                        # proprietary_id=,
                    ),
                ),
            ],
            applicable_trade_tax=[
                _ligne_tva_facturx_basic_ou_en_16931(ligne_tva, factur_x_module)
                for ligne_tva in facture.lignes_de_tva
            ],
            # billing_specified_period=factur_x_module.SpecifiedPeriodType(),
            # specified_trade_allowance_charge=[factur_x_module.TradeAllowanceChargeType(
            # charge_indicator=factur_x_module.IndicatorType(indicator=False),
            # actual_amount=factur_x_module.AmountType(value=format_decimal % facture.montant_total.montant_remise_globale_ttc),
            # reason=factur_x_module.TextType(value=facture.montant_total.motif_remise_globale_ttc),
            # category_trade_tax=factur_x_module.TradeTaxType(
            # type_code=factur_x_module.TaxTypeCodeType("VAT"),
            # category_code=factur_x_module.TaxCategoryCodeType(value=CategorieTVA.tva_cat_S),
            # rate_applicable_percent=factur_x_module.PercentType(value=format_decimal % facture.lignes_de_tva[0].taux_manuel)
            # )
            # ),],
            specified_trade_payment_terms=factur_x_module.TradePaymentTermsType(
                due_date_date_time=factur_x_module.DateTimeType(
                    date_time_string=factur_x_module.DateTimeType.DateTimeString(
                        format="102",
                        value=_parse_date_chorus_vers_facturx(
                            facture.date_echeance_paiement
                        ),
                    )
                ),
            ),
            invoice_currency_code=factur_x_module.CurrencyCodeType(
                value=facture.references.devise_facture
            ),
            # invoice_referenced_document=[factur_x_module.ReferencedDocumentType(),], # Numéro de facture antérieure ?
            # receivable_specified_trade_accounting_account=factur_x_module.TradeAccountingAccountType(),
            specified_trade_settlement_header_monetary_summation=factur_x_module.TradeSettlementHeaderMonetarySummationType(
                line_total_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_ht_total
                    )
                ),
                allowance_total_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        (facture.montant_total.montant_remise_globale_ttc or 0)
                    )
                ),
                tax_basis_total_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_ht_total
                    )
                ),
                tax_total_amount=[
                    factur_x_module.AmountType(
                        value=_float_vers_decimal_facturx(
                            facture.montant_total.montant_tva
                        ),
                        currency_id=facture.references.devise_facture,
                    ),
                ],
                grand_total_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_ttc_total
                    )
                ),
                total_prepaid_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        (facture.montant_total.acompte or 0)
                    )
                ),
                due_payable_amount=factur_x_module.AmountType(
                    value=_float_vers_decimal_facturx(
                        facture.montant_total.montant_a_payer
                    )
                ),
            ),
        ),
    )
    f = factur_x_module.CrossIndustryInvoice(
        exchanged_document_context=exchanged_document_context,
        exchanged_document=exchanged_document,
        supply_chain_trade_transaction=supply_chain_trade_transaction,
    )
    return f


def gen_facturx_basic(facture: FactureFacturX) -> factur_x_basic.CrossIndustryInvoice:
    """Génère un objet XML Factur-X conforme au profil BASIC."""
    est_valide_pour_facturx_basic(facture)
    return gen_facturx_basic_ou_en_16931(facture, factur_x_module_str=FACTURX_BASIC)


def est_valide_facturx_en16931(facture: FactureFacturX) -> None:
    """Vérifie si les données de la facture sont compatibles avec le profil EN16931."""
    return est_valide_pour_facturx_basic(facture)


def gen_facturx_en16931(
    facture: FactureFacturX,
) -> factur_x_en16931.CrossIndustryInvoice:
    """Génère un objet XML Factur-X conforme au profil EN16931."""
    est_valide_facturx_en16931(facture)
    return gen_facturx_basic_ou_en_16931(facture, factur_x_module_str=FACTURX_EN16931)


def est_valide_facturx_extended(facture: FactureFacturX) -> None:
    """Vérifie si les données de la facture sont compatibles avec le profil EXTENDED."""
    return est_valide_pour_facturx_basic(facture)


def gen_facturx_extended(
    facture: FactureFacturX,
) -> factur_x_extended.CrossIndustryInvoice:
    """Génère un objet XML Factur-X conforme au profil EN16931."""
    est_valide_facturx_extended(facture)
    return gen_facturx_basic_ou_en_16931(facture, factur_x_module_str=FACTURX_EXTENDED)


def gen_xml_depuis_facture(facture) -> str:
    """Sérialise un objet de facture (généré par xsdata) en une chaîne XML.

    :param facture: L'objet de facture à sérialiser.
    :return: Une chaîne de caractères contenant le XML formaté.
    """
    from xsdata.formats.dataclass.serializers import XmlSerializer
    from xsdata.formats.dataclass.context import XmlContext
    from xsdata.formats.dataclass.serializers.config import SerializerConfig

    nsmap = {
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
        "qdt": "urn:un:unece:uncefact:data:standard:QualifiedDataType:100",
        "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
    }

    config = SerializerConfig(indent="  ")
    serializer = XmlSerializer(context=XmlContext(), config=config)
    xml_data = serializer.render(facture, ns_map=nsmap)
    return xml_data


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


def valider_xml_facturx_schematron(xml_data: str, profil: str) -> bool:
    """
    Valide un contenu XML en utilisant le fichier XSLT de validation approprié.

    Cette fonction utilise importlib.resources pour accéder
    aux fichiers XSLT empaquetés avec la bibliothèque.

    :param xml_data: La chaîne de caractères contenant le XML de la facture.
    :param profil: Le profil de validation.
    :return: True si la validation réussit (ne lève pas d'exception).
    :raises XSLTValidationError: Si des assertions de validation échouent.
    :raises ValueError: Si le profil est inconnu.
    """
    # 1. Sélectionner la bonne ressource XSLT en fonction du profil
    try:
        if profil == FACTURX_MINIMUM:
            ref_xslt = resources.files(
                "facture_electronique.xsd.facturx-minimum._XSLT_MINIMUM"
            ).joinpath("FACTUR-X_MINIMUM.xslt")
        elif profil == FACTURX_BASIC:
            ref_xslt = resources.files(
                "facture_electronique.xsd.facturx-basic._XSLT_BASIC"
            ).joinpath("FACTUR-X_BASIC.xslt")
        elif profil == FACTURX_EN16931:
            ref_xslt = resources.files(
                "facture_electronique.xsd.facturx-EN16931._XSLT_EN16931"
            ).joinpath("FACTUR-X_EN16931.xslt")
        elif profil == FACTURX_EXTENDED:
            ref_xslt = resources.files(
                "facture_electronique.xsd.facturx-extended._XSLT_EXTENDED"
            ).joinpath("FACTUR-X_EXTENDED.xslt")
        else:
            raise ValueError(f"Profil de validation inconnu : '{profil}'")
    except (ModuleNotFoundError, FileNotFoundError):
        raise FileNotFoundError(
            f"La ressource XSLT pour le profil '{profil}' n'a pas pu être trouvée. "
            "Vérifiez que les fichiers sont bien inclus dans le paquet via pyproject.toml."
        )

    # 2. Utiliser la ressource dans un contexte sécurisé
    # `as_file` garantit que la ressource est disponible sur le disque (même si le paquet est un zip)
    # et nous donne un chemin physique temporaire (objet pathlib.Path).
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

            # La logique de gestion des erreurs reste la même
            if matches:
                messages_erreur = []
                for test_expr, id_err, location, message in matches:
                    message_propre = message.strip() if message else "Pas de message"
                    messages_erreur.append(
                        f"Test: {test_expr}\nLocation: {location}\nMessage: {message_propre}"
                    )
                raise XSLTValidationError(messages_erreur)

            # Si aucune erreur n'est trouvée (la logique originale retournait False, ce qui semble incorrect)
            # S'il n'y a pas de "failed-assert", la validation est réussie.
            return True
