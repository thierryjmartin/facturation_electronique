import copy
from datetime import datetime

from ..models import Facture, TypeFacture, LignePoste, ModePaiement, LigneTva
from ..generated import factur_x_minimum, factur_x_basic
from ..exceptions import InvalidDataFacturxError

LEVEL_MINIMUM = 'minimum'
LEVEL_BASIC = 'basic'

nsmap = {
	'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
	'udt': 'urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100',
	'qdt': 'urn:un:unece:uncefact:data:standard:QualifiedDataType:100',
	'ram': 'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100',
	'rsm': 'urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100',
}

format_decimal = "%.2f"

def _parse_date_chorus_vers_facturx(date_str: str) -> str:
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

def get_facturx_quantity_units(unite: Facture) -> str:
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

def _gen_applicable_header_trade_agreement(facturx_minimum_ou_basic, facture):
	return facturx_minimum_ou_basic.HeaderTradeAgreementType(
			buyer_reference=facturx_minimum_ou_basic.TextType(value=facture.destinataire.code_service_executant),
			seller_trade_party=facturx_minimum_ou_basic.TradePartyType(
				name=facturx_minimum_ou_basic.TextType(value=facture.fournisseur.nom),
				specified_legal_organization=facturx_minimum_ou_basic.LegalOrganizationType(id=facturx_minimum_ou_basic.Idtype(scheme_id="0002", value=facture.fournisseur.siret)),
				postal_trade_address=facturx_minimum_ou_basic.TradeAddressType(country_id=facturx_minimum_ou_basic.CountryIdtype(value=facture.fournisseur.adresse_postale.pays_code_iso)),
				specified_tax_registration=[facturx_minimum_ou_basic.TaxRegistrationType(id=facturx_minimum_ou_basic.Idtype(scheme_id="VA", value=facture.fournisseur.numero_tva_intra,)),]
			),
			buyer_trade_party=facturx_minimum_ou_basic.TradePartyType(
				name=facturx_minimum_ou_basic.TextType(value=facture.destinataire.nom),
				specified_legal_organization=facturx_minimum_ou_basic.LegalOrganizationType(id=facturx_minimum_ou_basic.Idtype(scheme_id="0002", value=facture.destinataire.code_destinataire)),
				postal_trade_address=facturx_minimum_ou_basic.TradeAddressType(country_id=facturx_minimum_ou_basic.CountryIdtype(value=facture.destinataire.adresse_postale.pays_code_iso)),
				#specified_tax_registration=[TaxRegistrationType(), ]
			),
			buyer_order_referenced_document=facturx_minimum_ou_basic.ReferencedDocumentType(
				issuer_assigned_id=facturx_minimum_ou_basic.Idtype(value=facture.references.numero_bon_commande)
			),
		)

def gen_facturx_minimum(facture: Facture) -> factur_x_minimum.CrossIndustryInvoice:
	exchanged_document_context = factur_x_minimum.ExchangedDocumentContextType(
		guideline_specified_document_context_parameter=factur_x_minimum.DocumentContextParameterType(id=factur_x_minimum.Idtype(value="urn:factur-x.eu:1p0:minimum"))
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
				tax_basis_total_amount=factur_x_minimum.AmountType(value=format_decimal % facture.montant_total.montant_ht_total),
				tax_total_amount=[factur_x_minimum.AmountType(value=format_decimal % facture.montant_total.montant_TVA, currency_id=facture.references.devise_facture), ],
				grand_total_amount=factur_x_minimum.AmountType(value=format_decimal % facture.montant_total.montant_ttc_total),
				due_payable_amount=factur_x_minimum.AmountType(value=format_decimal % facture.montant_total.montant_a_payer)
			)
		),
	)
	f=factur_x_minimum.CrossIndustryInvoice(
		exchanged_document_context=exchanged_document_context,
		exchanged_document=exchanged_document,
		supply_chain_trade_transaction=supply_chain_trade_transaction,
	)
	return f

def _ligne_poste_facturx_basic(ligne: LignePoste, facture: Facture):
	date_debut_retenue = ligne.ligne_poste_date_debut or facture.date_facture
	date_fin_retenue = ligne.ligne_poste_date_fin or ligne.ligne_poste_date_debut or facture.date_facture

	trade_allowance_charge = None
	trade_allowance_charge_trade_agreement = None
	if ligne.ligne_poste_montant_remise_HT:
		trade_allowance_charge = factur_x_basic.TradeAllowanceChargeType(
					charge_indicator=factur_x_basic.IndicatorType(indicator=False),
					actual_amount=factur_x_basic.AmountType(value=format_decimal % (ligne.ligne_poste_montant_remise_HT * ligne.ligne_poste_quantite)),
		)

		trade_allowance_charge_trade_agreement = copy.deepcopy(trade_allowance_charge)
		trade_allowance_charge_trade_agreement.actual_amount.value=format_decimal % ligne.ligne_poste_montant_remise_HT

		if ligne.ligne_poste_code_raison_reduction_code:
			trade_allowance_charge.reason_code = factur_x_basic.AllowanceChargeReasonCodeType(
				value=ligne.ligne_poste_code_raison_reduction_code)
		if ligne.ligne_poste_code_raison_reduction:
			trade_allowance_charge.reason = factur_x_basic.TextType(value=ligne.ligne_poste_code_raison_reduction)

	ligne_unit_code = get_facturx_quantity_units(ligne.ligne_poste_unite)

	suply_chain_trade_line = factur_x_basic.SupplyChainTradeLineItemType(
		associated_document_line_document=factur_x_basic.DocumentLineDocumentType(
			line_id= factur_x_basic.Idtype(value=str(ligne.ligne_poste_numero)) #, scheme_id=),
			# included_note = factur_x_basic.NoteType(content=, subject_code=),
		),
		specified_trade_product=factur_x_basic.TradeProductType(
			#global_id=factur_x_basic.Idtype(value=ligne.ligne_poste_reference, scheme_id=''),
			name=factur_x_basic.TextType(value=ligne.ligne_poste_reference + " " + ligne.ligne_poste_denomination)
		),
		specified_line_trade_agreement=factur_x_basic.LineTradeAgreementType(
			gross_price_product_trade_price = factur_x_basic.TradePriceType(
				charge_amount = factur_x_basic.AmountType(value=format_decimal % ligne.ligne_poste_montant_unitaire_HT),
				basis_quantity = factur_x_basic.QuantityType(value=format_decimal % ligne.ligne_poste_quantite, unit_code=ligne_unit_code),
				applied_trade_allowance_charge = trade_allowance_charge_trade_agreement if trade_allowance_charge_trade_agreement else None,
			),
			net_price_product_trade_price = factur_x_basic.TradePriceType(
				charge_amount=factur_x_basic.AmountType(value="%.2f" % (ligne.ligne_poste_montant_unitaire_HT - ligne.ligne_poste_montant_remise_HT)),
				basis_quantity=factur_x_basic.QuantityType(value=format_decimal % ligne.ligne_poste_quantite, unit_code=ligne_unit_code),
				# applied_trade_allowance_charge=factur_x_basic.TradeAllowanceChargeType()
			),
		),
		specified_line_trade_delivery=factur_x_basic.LineTradeDeliveryType(
			billed_quantity=factur_x_basic.QuantityType(value=format_decimal % ligne.ligne_poste_quantite, unit_code=ligne_unit_code)
		),
		specified_line_trade_settlement=factur_x_basic.LineTradeSettlementType(
			applicable_trade_tax=factur_x_basic.TradeTaxType(
				#calculated_amount=factur_x_basic.AmountType(),
				type_code=factur_x_basic.TaxTypeCodeType(value='VAT'),
				#exemption_reason=factur_x_basic.TextType(),
				#basis_amount=factur_x_basic.AmountType(),
				category_code=factur_x_basic.TaxCategoryCodeType(value=ligne.ligne_poste_tva_categorie),
				#exemption_reason_code=factur_x_basic.CodeType(),
				#due_date_type_code=factur_x_basic.TimeReferenceCodeType(),
				rate_applicable_percent=factur_x_basic.PercentType(value=format_decimal % ligne.ligne_poste_taux_tva_manuel),
			),
			billing_specified_period=factur_x_basic.SpecifiedPeriodType(
				start_date_time=factur_x_basic.DateTimeType(date_time_string=factur_x_basic.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(date_debut_retenue), format="102")),
				end_date_time=factur_x_basic.DateTimeType(date_time_string=factur_x_basic.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(date_fin_retenue), format="102")),
			),
			specified_trade_allowance_charge=[trade_allowance_charge, ] if trade_allowance_charge else None,
			specified_trade_settlement_line_monetary_summation=factur_x_basic.TradeSettlementLineMonetarySummationType(
				line_total_amount=factur_x_basic.AmountType(value=format_decimal % (ligne.ligne_poste_montant_unitaire_HT * ligne.ligne_poste_quantite)),
			),
		),
	)
	return suply_chain_trade_line

def _ligne_tva_facturx_basic(ligne_tva: LigneTva) -> factur_x_basic.TradeTaxType:
	return factur_x_basic.TradeTaxType(
		calculated_amount=factur_x_basic.AmountType(value=format_decimal % ligne_tva.ligne_tva_montant_tva_par_taux),
		type_code=factur_x_basic.TaxTypeCodeType(value='VAT'),
		basis_amount=factur_x_basic.AmountType(value=format_decimal % ligne_tva.ligne_tva_montant_base_ht_par_taux),
		category_code=factur_x_basic.TaxCategoryCodeType(value=ligne_tva.ligne_tva_categorie),
		rate_applicable_percent=factur_x_basic.PercentType(value=format_decimal % ligne_tva.ligne_tva_taux_manuel),
	)

def est_valide_pour_facturx_basic(facture: Facture):
	if facture.montant_total.montant_remise_globale_TTC:
		raise InvalidDataFacturxError("On ne peut pas mettre une remise TTC dans Facturx basic, il faut dispatch la remise sur les différentes lignes.")

def gen_facturx_basic(facture: Facture) -> factur_x_basic.CrossIndustryInvoice:
	est_valide_pour_facturx_basic(facture)
	exchanged_document_context = factur_x_basic.ExchangedDocumentContextType(
		guideline_specified_document_context_parameter=factur_x_basic.DocumentContextParameterType(id=factur_x_basic.Idtype(value="urn:cen.eu:EN 16931:2017#compliant#urn:factur-x.eu:1p0:basic"))
	)
	exchanged_document = factur_x_basic.ExchangedDocumentType(
		id=factur_x_basic.Idtype(value=facture.numero_facture_saisi),
		type_code=factur_x_basic.DocumentCodeType(value=get_facturx_type_code(facture)),
		issue_date_time=factur_x_basic.DateTimeType(date_time_string=factur_x_basic.DateTimeType.DateTimeString(value=_parse_date_chorus_vers_facturx(facture.date_facture), format="102")),
	)
	supply_chain_trade_transaction = factur_x_basic.SupplyChainTradeTransactionType(
		included_supply_chain_trade_line_item=[_ligne_poste_facturx_basic(ligne, facture) for ligne in facture.ligne_poste],
		applicable_header_trade_agreement=_gen_applicable_header_trade_agreement(factur_x_basic, facture),
		applicable_header_trade_delivery=factur_x_basic.HeaderTradeDeliveryType(),
		applicable_header_trade_settlement=factur_x_basic.HeaderTradeSettlementType(
			creditor_reference_id=factur_x_basic.Idtype(),
			payment_reference=factur_x_basic.TextType(),
			# tax_currency_code=factur_x_basic.CurrencyCodeType(value=facture.references.devise_facture),
			# payee_trade_party=factur_x_basic.TradePartyType(), utile si le bénéficiare est différent du fournisseur
			specified_trade_settlement_payment_means = [factur_x_basic.TradeSettlementPaymentMeansType(
				type_code=factur_x_basic.PaymentMeansCodeType(value=get_facturx_mode_paiement(facture)),
				# payer_party_debtor_financial_account=factur_x_basic.DebtorFinancialAccountType(ibanid=),
				# payee_party_creditor_financial_account=factur_x_basic.CreditorFinancialAccountType(ibanid=,proprietary_id=,)
			),],
			applicable_trade_tax=[_ligne_tva_facturx_basic(ligne_tva) for ligne_tva in facture.ligne_tva ],
			# billing_specified_period=factur_x_basic.SpecifiedPeriodType(),
			#specified_trade_allowance_charge=[factur_x_basic.TradeAllowanceChargeType(
			#	charge_indicator=factur_x_basic.IndicatorType(indicator=False),
			#	actual_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_remise_globale_TTC),
			#	reason=factur_x_basic.TextType(value=facture.montant_total.motif_remise_globale_TTC),
			#	category_trade_tax=factur_x_basic.TradeTaxType(
			#		type_code=factur_x_basic.TaxTypeCodeType("VAT"),
			#		category_code=factur_x_basic.TaxCategoryCodeType(value=TvaCategories.tva_cat_S),
			#		rate_applicable_percent=factur_x_basic.PercentType(value=format_decimal % facture.ligne_tva[0].ligne_tva_taux_manuel)
			#	)
			#),],
			specified_trade_payment_terms=factur_x_basic.TradePaymentTermsType(
				due_date_date_time=factur_x_basic.DateTimeType(date_time_string=factur_x_basic.DateTimeType.DateTimeString(format="102", value=_parse_date_chorus_vers_facturx(facture.date_echeance_paiement))),
			),
			invoice_currency_code=factur_x_basic.CurrencyCodeType(value=facture.references.devise_facture),
			#invoice_referenced_document=[factur_x_basic.ReferencedDocumentType(),], # Numéro de facture antérieure ?
			#receivable_specified_trade_accounting_account=factur_x_basic.TradeAccountingAccountType(),
			specified_trade_settlement_header_monetary_summation=factur_x_basic.TradeSettlementHeaderMonetarySummationType(
				line_total_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_ht_total),
				allowance_total_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_remise_globale_TTC),
				tax_basis_total_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_ht_total),
				tax_total_amount=[factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_TVA, currency_id=facture.references.devise_facture), ],
				grand_total_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_ttc_total),
				total_prepaid_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.acompte),
				due_payable_amount=factur_x_basic.AmountType(value=format_decimal % facture.montant_total.montant_a_payer)
			)
		),
	)
	f=factur_x_basic.CrossIndustryInvoice(
		exchanged_document_context=exchanged_document_context,
		exchanged_document=exchanged_document,
		supply_chain_trade_transaction=supply_chain_trade_transaction,
	)
	return f

def xml_from_facture_xsdata(facture) -> str:
	from xsdata.formats.dataclass.serializers import XmlSerializer
	from xsdata.formats.dataclass.context import XmlContext
	from xsdata.formats.dataclass.serializers.config import SerializerConfig
	config = SerializerConfig(indent="  ")
	serializer = XmlSerializer(context=XmlContext(), config=config)
	xml_data = serializer.render(facture, ns_map=nsmap)
	return xml_data