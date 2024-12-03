import os
import copy
from datetime import datetime
from decimal import Decimal
from typing import Literal, Union, Callable, Type

from ..models import Facture, TypeFacture, LignePoste, ModePaiement, LigneTva
from ..generated import factur_x_minimum, factur_x_basic, factur_x_en16931
from ..exceptions import InvalidDataFacturxError, XSLTValidationError

FACTURX_MINIMUM = "factur-x-minimum"
FACTURX_BASIC = "factur-x-basic"
FACTURX_EN16931 = "factur-x-en16931"

def get_factur_x_module(
		factur_x_module_str: Literal[FACTURX_BASIC, FACTURX_EN16931]
) -> Type:
	"""
	Returns the Factur-X module based on the input string.

	Args:
		factur_x_module_str (Literal): The name of the Factur-X module ('factur_x_basic' or 'factur_x_en16931').

	Returns:
		module: The selected Factur-X module.

	Raises:
		ValueError: If the module string is invalid.
	"""
	module_map = {
		FACTURX_BASIC: factur_x_basic,
		FACTURX_EN16931: factur_x_en16931,
	}
	if factur_x_module_str not in module_map:
		raise ValueError(f"Invalid module: {factur_x_module_str}. Expected 'factur_x_basic' or 'factur_x_en16931'.")
	return module_map[factur_x_module_str]

def _float_vers_decimal_facturx(value: float) -> Decimal:
	"""convertit un float en Decimal voulu par factur-x"""
	format_decimal = "%.2f"
	return Decimal(format_decimal % value)

def _parse_date_chorus_vers_facturx(date_str: str) -> str:
	""" convertit une date au format chorus pro vers le format factur-x"""
	return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")

def get_facturx_type_code(facture: Facture) -> str:
	if facture.references.type_facture == TypeFacture.avoir:
		return "381"
	else:
		return "380"

def get_facturx_mode_paiement(facture: Facture) -> str:
	equiv = {
		ModePaiement.cheque: "20",
		ModePaiement.prelevement: "49",
		ModePaiement.virement: "30",
		ModePaiement.espece: "10",
		ModePaiement.autre: "57",
		ModePaiement.report: "97"
	}
	return equiv[facture.references.mode_paiement]

def get_facturx_quantity_units(unite: str) -> str:
	"""sont les suivantes:
		LTR = Litre (1 dm3)
		MTQ = Mètre cube
		KGM = Kilogramme
		MTR = Mètre
		C62 = Unité
		TNE = Tonne"""
	equiv = {
		"lot": "C62",
		"Kg": "KGM",
	}
	try:
		return equiv[unite]
	except KeyError:
		return "C62"

def _gen_applicable_header_trade_agreement(facturx, facture):
	return facturx.HeaderTradeAgreementType(
			buyer_reference=facturx.TextType(value=facture.destinataire.code_service_executant),
			seller_trade_party=facturx.TradePartyType(
				name=facturx.TextType(value=facture.fournisseur.nom),
				specified_legal_organization=facturx.LegalOrganizationType(id=facturx.Idtype(scheme_id="0002", value=facture.fournisseur.siret)),
				postal_trade_address=facturx.TradeAddressType(country_id=facturx.CountryIdtype(value=facture.fournisseur.adresse_postale.pays_code_iso)),
				specified_tax_registration=[facturx.TaxRegistrationType(id=facturx.Idtype(scheme_id="VA", value=facture.fournisseur.numero_tva_intra, )), ]
			),
			buyer_trade_party=facturx.TradePartyType(
				name=facturx.TextType(value=facture.destinataire.nom),
				specified_legal_organization=facturx.LegalOrganizationType(id=facturx.Idtype(scheme_id="0002", value=facture.destinataire.code_destinataire)),
				postal_trade_address=facturx.TradeAddressType(country_id=facturx.CountryIdtype(value=facture.destinataire.adresse_postale.pays_code_iso)),
				#specified_tax_registration=[TaxRegistrationType(), ]
			),
			buyer_order_referenced_document=facturx.ReferencedDocumentType(
				issuer_assigned_id=facturx.Idtype(value=facture.references.numero_bon_commande)
			),
		)

def gen_facturx_minimum(facture: Facture) -> factur_x_minimum.CrossIndustryInvoice:
	exchanged_document_context = factur_x_minimum.ExchangedDocumentContextType(
		guideline_specified_document_context_parameter=factur_x_minimum.DocumentContextParameterType(id=factur_x_minimum.Idtype(value="urn:factur-x.eu:1p0:minimum")) # urn:factur-x.eu:1p0:minimum
	)
	exchanged_document = factur_x_minimum.ExchangedDocumentType(
		id=factur_x_minimum.Idtype(value=facture.numero_facture_saisi),
		type_code=factur_x_minimum.DocumentCodeType(value=get_facturx_type_code(facture)),
		issue_date_time=factur_x_minimum.DateTimeType(date_time_string=factur_x_minimum.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(facture.date_facture), format="102")),
	)
	supply_chain_trade_transaction = factur_x_minimum.SupplyChainTradeTransactionType(
		applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(factur_x_minimum, facture),
		applicable_header_trade_delivery=factur_x_minimum.HeaderTradeDeliveryType(),
		applicable_header_trade_settlement=factur_x_minimum.HeaderTradeSettlementType(
			invoice_currency_code=factur_x_minimum.CurrencyCodeType(value=facture.references.devise_facture),
			specified_trade_settlement_header_monetary_summation=factur_x_minimum.TradeSettlementHeaderMonetarySummationType(
				tax_basis_total_amount=factur_x_minimum.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_ht_total)),
				tax_total_amount=[factur_x_minimum.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_TVA), currency_id=facture.references.devise_facture), ],
				grand_total_amount=factur_x_minimum.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_ttc_total)),
				due_payable_amount=factur_x_minimum.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_a_payer))
			)
		),
	)
	f=factur_x_minimum.CrossIndustryInvoice(
		exchanged_document_context=exchanged_document_context,
		exchanged_document=exchanged_document,
		supply_chain_trade_transaction=supply_chain_trade_transaction,
	)
	return f

def _ligne_poste_facturx_basic_ou_en16931(ligne: LignePoste, facture: Facture, factur_x_module: Type) -> Union[factur_x_basic.SupplyChainTradeLineItemType, factur_x_en16931.SupplyChainTradeLineItemType]:
	date_debut_retenue = ligne.ligne_poste_date_debut or facture.date_facture
	date_fin_retenue = ligne.ligne_poste_date_fin or ligne.ligne_poste_date_debut or facture.date_facture

	trade_allowance_charge = None
	trade_allowance_charge_trade_agreement = None
	if ligne.ligne_poste_montant_remise_HT:
		trade_allowance_charge = factur_x_module.TradeAllowanceChargeType(
					charge_indicator=factur_x_module.IndicatorType(indicator=False),
					actual_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(ligne.ligne_poste_montant_remise_HT * ligne.ligne_poste_quantite)),
		)

		trade_allowance_charge_trade_agreement = copy.deepcopy(trade_allowance_charge)
		trade_allowance_charge_trade_agreement.actual_amount.value=_float_vers_decimal_facturx(ligne.ligne_poste_montant_remise_HT)

		if ligne.ligne_poste_code_raison_reduction_code:
			trade_allowance_charge.reason_code = factur_x_module.AllowanceChargeReasonCodeType(
				value=ligne.ligne_poste_code_raison_reduction_code)
		if ligne.ligne_poste_code_raison_reduction:
			trade_allowance_charge.reason = factur_x_module.TextType(value=ligne.ligne_poste_code_raison_reduction)

	ligne_unit_code = get_facturx_quantity_units(ligne.ligne_poste_unite)

	suply_chain_trade_line = factur_x_module.SupplyChainTradeLineItemType(
		associated_document_line_document=factur_x_module.DocumentLineDocumentType(
			line_id= factur_x_module.Idtype(value=str(ligne.ligne_poste_numero)) #, scheme_id=),
			# included_note = factur_x_module.NoteType(content=, subject_code=),
		),
		specified_trade_product=factur_x_module.TradeProductType(
			#global_id=factur_x_module.Idtype(value=ligne.ligne_poste_reference, scheme_id=''),
			name=factur_x_module.TextType(value=ligne.ligne_poste_reference + " " + ligne.ligne_poste_denomination)
		),
		specified_line_trade_agreement=factur_x_module.LineTradeAgreementType(
			gross_price_product_trade_price = factur_x_module.TradePriceType(
				charge_amount = factur_x_module.AmountType(value=_float_vers_decimal_facturx(ligne.ligne_poste_montant_unitaire_HT)),
				basis_quantity = factur_x_module.QuantityType(value=_float_vers_decimal_facturx(ligne.ligne_poste_quantite), unit_code=ligne_unit_code),
				applied_trade_allowance_charge = trade_allowance_charge_trade_agreement if trade_allowance_charge_trade_agreement else None,
			),
			net_price_product_trade_price = factur_x_module.TradePriceType(
				charge_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(ligne.ligne_poste_montant_unitaire_HT - ligne.ligne_poste_montant_remise_HT)),
				basis_quantity=factur_x_module.QuantityType(value=_float_vers_decimal_facturx(ligne.ligne_poste_quantite), unit_code=ligne_unit_code),
				# applied_trade_allowance_charge=factur_x_module.TradeAllowanceChargeType()
			),
		),
		specified_line_trade_delivery=factur_x_module.LineTradeDeliveryType(
			billed_quantity=factur_x_module.QuantityType(value=_float_vers_decimal_facturx(ligne.ligne_poste_quantite), unit_code=ligne_unit_code)
		),
		specified_line_trade_settlement=factur_x_module.LineTradeSettlementType(
			applicable_trade_tax=factur_x_module.TradeTaxType(
				#calculated_amount=factur_x_module.AmountType(),
				type_code=factur_x_module.TaxTypeCodeType(value='VAT'),
				#exemption_reason=factur_x_module.TextType(),
				#basis_amount=factur_x_module.AmountType(),
				category_code=factur_x_module.TaxCategoryCodeType(value=ligne.ligne_poste_tva_categorie),
				#exemption_reason_code=factur_x_module.CodeType(),
				#due_date_type_code=factur_x_module.TimeReferenceCodeType(),
				rate_applicable_percent=factur_x_module.PercentType(value=_float_vers_decimal_facturx(ligne.ligne_poste_taux_tva_manuel)),
			),
			billing_specified_period=factur_x_module.SpecifiedPeriodType(
				start_date_time=factur_x_module.DateTimeType(date_time_string=factur_x_module.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(date_debut_retenue), format="102")),
				end_date_time=factur_x_module.DateTimeType(date_time_string=factur_x_module.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(date_fin_retenue), format="102")),
			),
			specified_trade_allowance_charge=[trade_allowance_charge, ] if trade_allowance_charge else None,
			specified_trade_settlement_line_monetary_summation=factur_x_module.TradeSettlementLineMonetarySummationType(
				line_total_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(ligne.ligne_poste_montant_unitaire_HT * ligne.ligne_poste_quantite)),
			),
		),
	)
	return suply_chain_trade_line

def _ligne_tva_facturx_basic_ou_en_16931(ligne_tva: LigneTva, factur_x_module: Type) -> Union[factur_x_basic.TradeTaxType, factur_x_en16931.TradeTaxType]:
	return factur_x_module.TradeTaxType(
		calculated_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(ligne_tva.ligne_tva_montant_tva_par_taux)),
		type_code=factur_x_module.TaxTypeCodeType(value='VAT'),
		basis_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(ligne_tva.ligne_tva_montant_base_ht_par_taux)),
		category_code=factur_x_module.TaxCategoryCodeType(value=ligne_tva.ligne_tva_categorie),
		rate_applicable_percent=factur_x_module.PercentType(value=_float_vers_decimal_facturx(ligne_tva.ligne_tva_taux_manuel)),
	)

def est_valide_pour_facturx_basic(facture: Facture) -> None:
	if facture.montant_total.montant_remise_globale_TTC:
		raise InvalidDataFacturxError("On ne peut pas mettre une remise TTC dans Facturx basic, il faut dispatch la remise sur les différentes lignes.")

def gen_facturx_basic_ou_en_16931(facture: Facture, factur_x_module_str: Literal[FACTURX_BASIC, FACTURX_EN16931]) -> Union[factur_x_basic.CrossIndustryInvoice, factur_x_en16931.CrossIndustryInvoice]:
	factur_x_module = get_factur_x_module(factur_x_module_str)

	est_valide_pour_facturx_basic(facture)

	document_context_type_parameter = {
		FACTURX_BASIC: "urn:cen.eu:en16931:2017#compliant#urn:factur-x.eu:1p0:basic",
		FACTURX_EN16931: "urn:cen.eu:en16931:2017"
	}
	exchanged_document_context = factur_x_module.ExchangedDocumentContextType(
		guideline_specified_document_context_parameter=factur_x_module.DocumentContextParameterType(id=factur_x_module.Idtype(value=document_context_type_parameter[factur_x_module_str]))
	)
	exchanged_document = factur_x_module.ExchangedDocumentType(
		id=factur_x_module.Idtype(value=facture.numero_facture_saisi),
		type_code=factur_x_module.DocumentCodeType(value=get_facturx_type_code(facture)),
		issue_date_time=factur_x_module.DateTimeType(date_time_string=factur_x_module.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(facture.date_facture), format="102")),
	)
	supply_chain_trade_transaction = factur_x_module.SupplyChainTradeTransactionType(
		included_supply_chain_trade_line_item=[_ligne_poste_facturx_basic_ou_en16931(ligne, facture, factur_x_module) for ligne in facture.ligne_poste],
		applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(factur_x_module, facture),
		applicable_header_trade_delivery=factur_x_module.HeaderTradeDeliveryType(),
		applicable_header_trade_settlement=factur_x_module.HeaderTradeSettlementType(
			creditor_reference_id=factur_x_module.Idtype(),
			payment_reference=factur_x_module.TextType(),
			# tax_currency_code=factur_x_module.CurrencyCodeType(value=facture.references.devise_facture),
			# payee_trade_party=factur_x_module.TradePartyType(), utile si le bénéficiare est différent du fournisseur
			specified_trade_settlement_payment_means = [factur_x_module.TradeSettlementPaymentMeansType(
				type_code=factur_x_module.PaymentMeansCodeType(value=get_facturx_mode_paiement(facture)),
				# payer_party_debtor_financial_account=factur_x_module.DebtorFinancialAccountType(ibanid=),
				# payee_party_creditor_financial_account=factur_x_module.CreditorFinancialAccountType(ibanid=,proprietary_id=,)
			),],
			applicable_trade_tax=[_ligne_tva_facturx_basic_ou_en_16931(ligne_tva, factur_x_module) for ligne_tva in facture.ligne_tva],
			# billing_specified_period=factur_x_module.SpecifiedPeriodType(),
			#specified_trade_allowance_charge=[factur_x_module.TradeAllowanceChargeType(
			#	charge_indicator=factur_x_module.IndicatorType(indicator=False),
			#	actual_amount=factur_x_module.AmountType(value=format_decimal % facture.montant_total.montant_remise_globale_TTC),
			#	reason=factur_x_module.TextType(value=facture.montant_total.motif_remise_globale_TTC),
			#	category_trade_tax=factur_x_module.TradeTaxType(
			#		type_code=factur_x_module.TaxTypeCodeType("VAT"),
			#		category_code=factur_x_module.TaxCategoryCodeType(value=TvaCategories.tva_cat_S),
			#		rate_applicable_percent=factur_x_module.PercentType(value=format_decimal % facture.ligne_tva[0].ligne_tva_taux_manuel)
			#	)
			#),],
			specified_trade_payment_terms=factur_x_module.TradePaymentTermsType(
				due_date_date_time=factur_x_module.DateTimeType(date_time_string=factur_x_module.DateTimeType.DateTimeString(format="102", value=_parse_date_chorus_vers_facturx(facture.date_echeance_paiement))),
			),
			invoice_currency_code=factur_x_module.CurrencyCodeType(value=facture.references.devise_facture),
			#invoice_referenced_document=[factur_x_module.ReferencedDocumentType(),], # Numéro de facture antérieure ?
			#receivable_specified_trade_accounting_account=factur_x_module.TradeAccountingAccountType(),
			specified_trade_settlement_header_monetary_summation=factur_x_module.TradeSettlementHeaderMonetarySummationType(
				line_total_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_ht_total)),
				allowance_total_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_remise_globale_TTC)),
				tax_basis_total_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_ht_total)),
				tax_total_amount=[factur_x_module.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_TVA), currency_id=facture.references.devise_facture), ],
				grand_total_amount=factur_x_module.AmountType(value=_float_vers_decimal_facturx(facture.montant_total.montant_ttc_total)),
				total_prepaid_amount=factur_x_module.AmountType(value= _float_vers_decimal_facturx(facture.montant_total.acompte)),
				due_payable_amount=factur_x_module.AmountType(value= _float_vers_decimal_facturx(facture.montant_total.montant_a_payer))
			)
		),
	)
	f=factur_x_module.CrossIndustryInvoice(
		exchanged_document_context=exchanged_document_context,
		exchanged_document=exchanged_document,
		supply_chain_trade_transaction=supply_chain_trade_transaction,
	)
	return f

def gen_facturx_basic(facture: Facture) -> factur_x_basic.CrossIndustryInvoice:
	est_valide_pour_facturx_basic(facture)
	return gen_facturx_basic_ou_en_16931(facture, factur_x_module_str=FACTURX_BASIC)

def est_valide_facturx_en16931(facture: Facture) -> None:
	est_valide_pour_facturx_basic(facture)

def gen_facturx_en16931(facture: Facture) -> factur_x_en16931.CrossIndustryInvoice:
	est_valide_facturx_en16931(facture)
	return gen_facturx_basic_ou_en_16931(facture, factur_x_module_str=FACTURX_EN16931)

def xml_from_facture_xsdata(facture) -> str:
	""" gènère un xml depuis les données sous forme de classes xsdata """
	from xsdata.formats.dataclass.serializers import XmlSerializer
	from xsdata.formats.dataclass.context import XmlContext
	from xsdata.formats.dataclass.serializers.config import SerializerConfig

	nsmap = {
		'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
		'udt': 'urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100',
		'qdt': 'urn:un:unece:uncefact:data:standard:QualifiedDataType:100',
		'ram': 'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100',
		'rsm': 'urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100',
	}

	config = SerializerConfig(indent="  ")
	serializer = XmlSerializer(context=XmlContext(), config=config)
	xml_data = serializer.render(facture, ns_map=nsmap)
	return xml_data

current_file_dir = os.path.dirname(os.path.dirname(__file__))
chemin_xldt_minimum = os.path.join(current_file_dir, "xsd", "facturx-minimum", "_XSLT_MINIMUM", "Factur-X_1.07.2_MINIMUM.xslt")
chemin_xldt_basic = os.path.join(current_file_dir, "xsd", "facturx-basic", "_XSLT_BASIC", "Factur-X_1.07.2_BASIC.xslt")
chemin_xldt_en16931 = os.path.join(current_file_dir, "xsd", "facturx-EN16931", "_XSLT_EN16931", "Factur-X_1.07.2_EN16931.xslt")

def valider_xml_xldt(xml_data: str, chemin_xldt: str) -> bool:
	from saxonche import PySaxonProcessor
	import re

	with PySaxonProcessor(license=False) as proc:
		xsltproc = proc.new_xslt30_processor()
		document = proc.parse_xml(xml_text=xml_data)
		executable = xsltproc.compile_stylesheet(stylesheet_file=chemin_xldt)
		output = executable.transform_to_string(xdm_node=document)
		pattern = re.compile(r'<svrl:failed-assert\s+test="([^"]+)"\s+location="([^"]+)">\s+<svrl:text>\s+([^"]+)</svrl:text>')
		matches = pattern.findall(output)
		if not matches:
			return False
		res = ""
		for match in matches:
			test_expr, location, message = match
			res += f"Test: {test_expr}\nLocation: {location}\nMessage: {message.strip() if message else 'Pas de message'}\n\n"
		raise XSLTValidationError(res)
