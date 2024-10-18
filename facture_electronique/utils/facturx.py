from ..models import Facture, TypeFacture
from lxml.etree import Element, SubElement, tostring
from datetime import datetime
from collections import defaultdict

LEVEL_MINIMUM = 'minimum'
LEVEL_BASIC = 'basic'

nsmap = {
	'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
	'udt': 'urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100',
	'qdt': 'urn:un:unece:uncefact:data:standard:QualifiedDataType:100',
	'ram': 'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100',
	'rsm': 'urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100',
}

def _parse_date_chorus_vers_facturx(date_str: str) -> str:
	return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")

def ajouter_data_lignes_facturx(facture: Facture, element: Element) -> Element:
	for ligne_facture in facture.ligne_poste:
		# BG-25 1..n LIGNE DE FACTURE Groupe de termes métiers fournissant des informations sur des lignes de Facture individuelles.
		ligne = SubElement(element, "{%s}IncludedSupplyChainTradeLineItem" % nsmap['ram'])
		# BT-126 Identifiant de ligne de facture
		identifiant_ligne = SubElement(ligne, "{%s}AssociatedDocumentLineDocument" % nsmap['ram'])
		id_identifiant_ligne = SubElement(identifiant_ligne, "{%s}LineID" % nsmap['ram'])
		id_identifiant_ligne.text = str(ligne_facture.ligne_poste_numero)
		# BT-127 Commentaire fournissant des informations non structurées concernant la ligne de Facture.
		#included_note = SubElement(ligne, "{%s}IncludedNote" % nsmap['ram'])
		#included_note_content = SubElement(included_note, "{%s}Content" % nsmap['ram'])
		#included_note_content.text = ligne_facture.ligne_poste_denomination
		# BG-31 Informations sur l'article
		specified_trade_product = SubElement(ligne, "{%s}SpecifiedTradeProduct" % nsmap['ram'])
		# BT-157 Identifiant d'article basé sur un schéma enregistré.
		global_id = SubElement(specified_trade_product, "{%s}GlobalID" % nsmap['ram'])
		global_id.text = ligne_facture.ligne_poste_reference
		# BT-157-1 Scheme identifier
		global_id.set("schemeID", "")
		# BT-153 Identifiant d'article basé sur un schéma enregistré.
		name = SubElement(specified_trade_product, "{%s}Name" % nsmap['ram'])
		name.text = ligne_facture.ligne_poste_denomination
		# BG-29  Line trade agreements (price details)
		specified_trade_agreements = SubElement(ligne, "{%s}SpecifiedLineTradeAgreement" % nsmap['ram'])
		# BT-148 Price detail - item gross price
		item_gross_price = SubElement(specified_trade_agreements, "{%s}GrossPriceProductTradePrice" % nsmap['ram'])
		# BT-148
		# BR-28: The Item gross price (BT-148) shall NOT be negative.
		charge_amount = SubElement(item_gross_price, "{%s}ChargeAmount" % nsmap['ram'])
		charge_amount.text = "%.2f" % ligne_facture.ligne_poste_montant_unitaire_HT
		# BT-149-1 Item price base quantity
		basis_quantity = SubElement(item_gross_price, "{%s}BasisQuantity" % nsmap['ram'])
		basis_quantity.text = "%.2f" % ligne_facture.ligne_poste_quantite
		basis_quantity.set("unitCode", ligne_facture.ligne_poste_unite)
		# BT-147 Item price discount
		item_price_discount = SubElement(item_gross_price, "{%s}AppliedTradeAllowanceCharge" % nsmap['ram'])
		charge_indicator = SubElement(item_price_discount, "{%s}ChargeIndicator" % nsmap['ram'])
		indicator = SubElement(charge_indicator, "{%s}Indicator" % nsmap['udt'])
		indicator.text = "false"
		actual_amount = SubElement(item_price_discount, "{%s}ActualAmount" % nsmap['ram'])
		actual_amount.text = "%.2f" % (ligne_facture.ligne_poste_montant_remise_HT / ligne_facture.ligne_poste_quantite)
		# BT-146 Item net price The price of an item, exclusive of VAT, after subtracting item price discount.
		item_net_price = SubElement(specified_trade_agreements, "{%s}NetPriceProductTradePrice" % nsmap['ram'])
		charge_amount = SubElement(item_net_price, "{%s}ChargeAmount" % nsmap['ram'])
		charge_amount.text = "%.2f" % (ligne_facture.ligne_poste_montant_unitaire_HT - ligne_facture.ligne_poste_montant_remise_HT)
		# BT-149 Item price base quantity
		# Optional, if filled and if BT-148 is present (EN16931 and EXTENDED profiles), then it should be the same value than BT-149-1
		basis_quantity = SubElement(item_net_price, "{%s}BasisQuantity" % nsmap['ram'])
		basis_quantity.text = "%.2f" % ligne_facture.ligne_poste_quantite
		# BT-150 Item price base quantity unit of measure code
		basis_quantity.set("unitCode", ligne_facture.ligne_poste_unite)
		# BT-129 LINE TRADE DELIVERY
		specified_line_trade_delivery = SubElement(ligne, "{%s}SpecifiedLineTradeDelivery" % nsmap['ram'])
		# BT-129 The quantity of items (goods or services) that is charged in the Invoice line.
		# CHORUS PRO: Invoiced quantity is supported on 10 digits maximum.
		billed_quantity = SubElement(specified_line_trade_delivery, "{%s}BilledQuantity" % nsmap['ram'])
		billed_quantity.text = "%.2f" % ligne_facture.ligne_poste_quantite
		billed_quantity.set("unitCode", ligne_facture.ligne_poste_unite)
		# BG-30 Line trade settlement
		line_trade_settlement = SubElement(ligne, "{%s}SpecifiedLineTradeSettlement" % nsmap['ram'])
		# BG-30 Ligne VAT Information
		applicable_trade_taxe = SubElement(line_trade_settlement, "{%s}ApplicableTradeTax" % nsmap['ram'])
		# BT-151 Tax Type(Code)Invoiced item VAT category code, Content
		type_code = SubElement(applicable_trade_taxe, "{%s}TypeCode" % nsmap['ram'])
		type_code.text = 'VAT'
		# Invoiced item VAT category code
		category_code = SubElement(applicable_trade_taxe, "{%s}CategoryCode" % nsmap['ram'])
		category_code.text = ligne_facture.ligne_poste_tva_categorie
		# BT-152 Invoiced item VAT rate
		rate_applicable_percent = SubElement(applicable_trade_taxe, "{%s}RateApplicablePercent" % nsmap['ram'])
		rate_applicable_percent.text = "%.2f" % ligne_facture.ligne_poste_taux_tva_manuel
		# BG-26 INVOICE LINE PERIOD
		billing_specified_period = SubElement(line_trade_settlement, "{%s}BillingSpecifiedPeriod" % nsmap['ram'])
		# BT-134 Invoice line period start date
		start_date_time = SubElement(billing_specified_period, "{%s}StartDateTime" % nsmap['ram'])
		date_time_string = SubElement(start_date_time, "{%s}DateTimeString" % nsmap['udt'])
		date_time_string.set("format", "102")
		date_debut_retenue = ligne_facture.ligne_poste_date_debut or facture.date_facture
		date_time_string.text = _parse_date_chorus_vers_facturx(date_debut_retenue)
		# BT-135 Invoice line period end date
		end_date_time = SubElement(billing_specified_period, "{%s}EndDateTime" % nsmap['ram'])
		date_time_string = SubElement(end_date_time, "{%s}DateTimeString" % nsmap['udt'])
		date_time_string.set("format", "102")
		date_fin_retenue = ligne_facture.ligne_poste_date_fin or ligne_facture.ligne_poste_date_debut or facture.date_facture
		date_time_string.text = _parse_date_chorus_vers_facturx(date_fin_retenue)
		# BG-27 INVOICE LINE ALLOWANCES
		specified_trade_allowance_charge = SubElement(line_trade_settlement, "{%s}SpecifiedTradeAllowanceCharge" % nsmap['ram'])
		charge_indicator = SubElement(specified_trade_allowance_charge, "{%s}ChargeIndicator" % nsmap['ram'])
		indicator = SubElement(charge_indicator, "{%s}Indicator" % nsmap['udt'])
		indicator.text = "false"
		# BT-136 Invoice line allowance amount
		actual_amount = SubElement(specified_trade_allowance_charge, "{%s}ActualAmount" % nsmap['ram'])
		actual_amount.text = "%.2f" % ligne_facture.ligne_poste_montant_remise_HT
		if ligne_facture.ligne_poste_code_raison_reduction:
			reason_code = SubElement(specified_trade_allowance_charge, "{%s}ReasonCode" % nsmap['ram'])
			reason_code.text = ligne_facture.ligne_poste_code_raison_reduction_code
		if ligne_facture.ligne_poste_code_raison_reduction:
			reason = SubElement(specified_trade_allowance_charge, "{%s}Reason" % nsmap['ram'])
			reason.text = ligne_facture.ligne_poste_code_raison_reduction
		# BG-28 INVOICE LINE CHARGES




def gen_facturx(facture: Facture, level=LEVEL_MINIMUM, ) -> Element:
	"""
	Pour Chorus Pro, permet de générer un xml qui représente une facture CleverIP selon le standard Chorus Pro (MINIMUM)
	:return: un fichier XML au format facture-x représentant la facture envoyée en argument
	"""

	cross_industry_invoice = Element('{%s}CrossIndustryInvoice' % nsmap['rsm'], nsmap=nsmap)

	"""
	Bloc d’identification du message « rsm:ExchangedDocumentContext » (BG-2)
	✓ BT-23 : donnée facultative. 
		La balise « ram:BusinessProcessSpecifiedDocumentContextParameter », contient la valeur de l’identifiant du business process dans la balise « ram:ID ». 
		Les identifiants possibles sont par exemple ceux de ChorusPro définis dans sa documentation (A1 (dépôt facture), 
		A2 (dépôt facture déjà payée), ...) pour une facture adressée à destination du secteur public.
	✓ BT-24 : La balise « ram:GuidelineSpecifiedDocumentContextParameter », contient la valeur urn:factur-x.eu:1p0:minimum dans la balise « ram:ID »
	"""
	exchanged_document_context = SubElement(cross_industry_invoice, "{%s}ExchangedDocumentContext" % nsmap['rsm'])
	# BT-23
	document_context_parameter = SubElement(exchanged_document_context, "{%s}BusinessProcessSpecifiedDocumentContextParameter" % nsmap['ram'])
	id = SubElement(document_context_parameter, "{%s}ID" % nsmap['ram'])
	id.text = "A1" if facture.montant_total.montant_a_payer else "A2"
	# BT-24
	guide_line_scpecified_document_context_parameter = SubElement(exchanged_document_context,
																  "{%s}GuidelineSpecifiedDocumentContextParameter" %
																  nsmap['ram'])
	id = SubElement(guide_line_scpecified_document_context_parameter, "{%s}ID" % nsmap['ram'])
	if level == LEVEL_MINIMUM:
		id.text = "urn:factur-x.eu:1p0:minimum"
	else:
		id.text = "urn:cen.eu:EN 16931:2017#compliant#urn:factur-x.eu:1p0:basic"

	"""
	Bloc d’entête du Document contenant les données BT-1, BT-2 et BT-3, à l’intérieur de la balise « rsm:ExchangedDocument » 
	✓ BT-1 : numéro de facture dans la balise « ram:ID »
	✓ BT-2 : date d’émission de la facture dans la balise « udt:DateTimeString » avec l’attribut « @format » prenant la valeur 102, elle-même contenue dans la balise « ram:IssueDateTime ».
	✓ BT-3 : type de facture dans la balise « ram:TypeCode »,pour les valeurs suivantes :
		➢ 380 : Facture commerciale
		➢ 381 : Avoir (note de crédit)
		➢ 384 : Facture rectificative
		➢ 389 : Facture d’autofacturation (créée par l'acheteur pour le compte du fournisseur). Code non accepté pour ChorusPro
		➢ 261 : Avoir d’autofacturation. Code non accepté pour ChorusPro
		➢ 386 : Facture d'acompte
		➢ 751 : Informations de facture pour comptabilisation : code exigé en Allemagne pour satisfaire ses contraintes réglementaires. Code non accepté pour ChorusPro.
	"""
	exchanged_document = SubElement(cross_industry_invoice, "{%s}ExchangedDocument" % nsmap['rsm'])
	# BT-1
	id = SubElement(exchanged_document, "{%s}ID" % nsmap['ram'])
	id.text = facture.numero_facture_saisi
	# BT-3
	type_code = SubElement(exchanged_document, "{%s}TypeCode" % nsmap['ram'])
	if facture.references.type_facture == TypeFacture.avoir:
		type_code.text = "381"
	else:
		type_code.text = "380"

	# BT-2
	issue_date_time = SubElement(exchanged_document, "{%s}IssueDateTime" % nsmap['ram'])
	datetimestring = SubElement(issue_date_time, "{%s}DateTimeString" % nsmap['udt'])
	datetimestring.set("format", "102")
	if facture.date_facture:
		datetimestring.text = _parse_date_chorus_vers_facturx(facture.date_facture)
	else:
		datetimestring.text = datetime.date.today().strftime("%Y%m%d")

	if level != LEVEL_MINIMUM and facture.commentaire:
		# BG-1 included_note. pas décrit dans le format "minimum" mais "basic" car le XSD basis minimum est commun
		included_note = SubElement(exchanged_document, "{%s}IncludedNote" % nsmap['ram'])
		# BT-22
		included_note_content = SubElement(included_note, "{%s}Content" % nsmap['ram'])
		included_note_content.text = facture.commentaire
		# BT-21
		included_note_subjectcode = SubElement(included_note, "{%s}SubjectCode" % nsmap['ram'])
		"""AAI : Information générale
			SUR : Remarques fournisseur
			REG : Information réglementaire
			ABL : Information légale
			TXD : Information fiscale
			CUS : Information douanière"""
		included_note_subjectcode.text = "AAI"

	"""
	Le bloc regroupant les données de la facture sous la balise « rsm:SupplyChainTradeTransaction », composé des blocs suivants :
	✓ Bloc sous balise « ram:ApplicableHeaderTradeAgreement » contenant les données BT-10 et BT-13, et les groupes BG-4 et BG-7 :
	➢ BT-10 : référence acheteur, sous la balise « ram:BuyerReference »
				CHORUS PRO : pour le secteur public, il s'agit du "Service Executant". Il est obligatoire pour certains acheteurs. 
				Il doit appartenir au référentiel Chorus Pro. Il est limité à 100 caractères
	➢ BT-13 : numéro de commande fourni par l’acheteur, sous la double balise « ram:BuyerOrderReferencedDocument » « ram:IssuerAssignedID »
				CHORUS PRO : pour le secteur public, il s'agit de "l'Engagement Juridique". Il est obligatoire pour certains acheteurs. 
				Il convient de se référer à l'annuaire Chorus Pro pour identifier ces acheteurs.
	➢ BG-4 : groupe d’information sur le vendeur sous la balise « ram:SellerTradeParty » :
		▪ BT-27 : nom (raison sociale) du fournisseur, sous la balise « ram:Name »
		▪ BT-30 : identification légale du vendeur sous la double balise « ram:SpecifiedLegalOrganization » « ram:ID » complété d’un attribut « @schemeID » identifiant le référentiel (SIRET) : 0002.
		▪ BT-31 : numéro de TVA intracommunautaire sous la double balise « ram:SpecifiedTaxRegistration » « ram:ID » complété d’un attribut « @schemeID » égal à « VA ».
		▪ Groupe BG-5 de l’adresse postale contenant le pays du fournisseur : dans la balise « ram:CountryID » de la balise « ram:PostalTradeAddress » (FR pour la France).
	➢ BG-7 : groupe d’information de l’acheteur, sous la balise « ram:BuyerTradeParty » :
		▪ BT-44 : nom de l’acheteur (raison sociale), sous la balise « ram:Name »
		▪ BT-47 : identification légale de l’acheteur, sous la double balise « ram:SpecifiedLegalOrganization » « ram:ID » complété d’un attribut « @schemeID » identifiant le référentiel (SIRET) : 0002.
	"""
	supply_chain_trade_transaction = SubElement(cross_industry_invoice,
												"{%s}SupplyChainTradeTransaction" % nsmap['rsm'])

	if level != LEVEL_MINIMUM:
		ajouter_data_lignes_facturx(facture, supply_chain_trade_transaction)

	applicable_header_trade_agreement = SubElement(supply_chain_trade_transaction,
												   "{%s}ApplicableHeaderTradeAgreement" % nsmap['ram'])
	# BT-10
	buyer_reference = SubElement(applicable_header_trade_agreement, "{%s}BuyerReference" % nsmap['ram'])
	buyer_reference.text = facture.destinataire.code_service_executant
	# BG-4
	seller_trade_party = SubElement(applicable_header_trade_agreement, "{%s}SellerTradeParty" % nsmap['ram'])
	# BT-27
	name = SubElement(seller_trade_party, "{%s}Name" % nsmap['ram'])
	name.text = facture.fournisseur.nom
	# BT-30
	specified_legal_organisation = SubElement(seller_trade_party, "{%s}SpecifiedLegalOrganization" % nsmap['ram'])
	id = SubElement(specified_legal_organisation, "{%s}ID" % nsmap['ram'])
	id.set("schemeID", "0002")
	id.text = facture.fournisseur.siret
	# BG-5
	postal_trade_adress = SubElement(seller_trade_party, "{%s}PostalTradeAddress" % nsmap['ram'])
	country_id = SubElement(postal_trade_adress, "{%s}CountryID" % nsmap['ram'])
	country_id.text = facture.fournisseur.adresse_postale.pays_code_iso
	if level != LEVEL_MINIMUM:
		post_code = SubElement(postal_trade_adress, "{%s}PostcodeCode" % nsmap['ram'])
		post_code.text = facture.fournisseur.adresse_postale.code_postal
		line_one = SubElement(postal_trade_adress, "{%s}LineOne" % nsmap['ram'])
		line_one.text = facture.fournisseur.adresse_postale.ligne_un
		line_two = SubElement(postal_trade_adress, "{%s}LineTwo" % nsmap['ram'])
		line_two.text = facture.fournisseur.adresse_postale.ligne_deux
		city_name = SubElement(postal_trade_adress, "{%s}CityName" % nsmap['ram'])
		city_name.text = facture.fournisseur.adresse_postale.nom_ville
	# BT-31
	specified_tax_reigstration = SubElement(seller_trade_party, "{%s}SpecifiedTaxRegistration" % nsmap['ram'])
	id = SubElement(specified_tax_reigstration, "{%s}ID" % nsmap['ram'])
	id.set("schemeID", "VA")
	id.text = facture.fournisseur.numero_tva_intra
	# BG-7
	buyer_trade_party = SubElement(applicable_header_trade_agreement, "{%s}BuyerTradeParty" % nsmap['ram'])
	# BT-44
	name = SubElement(buyer_trade_party, "{%s}Name" % nsmap['ram'])
	name.text = facture.destinataire.nom
	# BT-47
	specified_legal_organisation = SubElement(buyer_trade_party, "{%s}SpecifiedLegalOrganization" % nsmap['ram'])
	id = SubElement(specified_legal_organisation, "{%s}ID" % nsmap['ram'])
	id.set("schemeID", "0002")
	id.text = facture.destinataire.code_destinataire

	postal_trade_adress = SubElement(buyer_trade_party, "{%s}PostalTradeAddress" % nsmap['ram'])
	country_id = SubElement(postal_trade_adress, "{%s}CountryID" % nsmap['ram'])
	country_id.text = facture.destinataire.adresse_postale.pays_code_iso
	if level != LEVEL_MINIMUM:
		post_code = SubElement(postal_trade_adress, "{%s}PostcodeCode" % nsmap['ram'])
		post_code.text = facture.destinataire.adresse_postale.code_postal
		line_one = SubElement(postal_trade_adress, "{%s}LineOne" % nsmap['ram'])
		line_one.text = facture.destinataire.adresse_postale.ligne_un
		line_two = SubElement(postal_trade_adress, "{%s}LineTwo" % nsmap['ram'])
		line_two.text = facture.destinataire.adresse_postale.ligne_deux
		city_name = SubElement(postal_trade_adress, "{%s}CityName" % nsmap['ram'])
		city_name.text = facture.destinataire.adresse_postale.nom_ville

	# BT-13
	buyer_order_referenced_document = SubElement(applicable_header_trade_agreement,
												 "{%s}BuyerOrderReferencedDocument" % nsmap['ram'])
	issuer_assigned_id = SubElement(buyer_order_referenced_document, "{%s}IssuerAssignedID" % nsmap['ram'])
	# a priori optionel
	issuer_assigned_id.text = facture.references.numero_bon_commande
	if level != LEVEL_MINIMUM:
		# BT-12 Identifiant de contrat, référence de document
		contract_referenced_document = SubElement(applicable_header_trade_agreement, "{%s}ContractReferencedDocument" % nsmap['ram'])
		issuer_assigned_id = SubElement(contract_referenced_document, "{%s}IssuerAssignedID" % nsmap['ram'])
		# a priori optionel
		issuer_assigned_id.text = facture.references.numero_marche  # numéro de contrat obligatoire pour valider le xml...

	"""
	Un bloc vide (car nécessaire à la conformité du message) correspondant aux informations de livraison.
	"""
	applicable_header_trade_delivery = SubElement(supply_chain_trade_transaction,
												  "{%s}ApplicableHeaderTradeDelivery" % nsmap['ram'])

	"""
	Le bloc regroupant les données de la facture sous la balise « ram:ApplicableHeaderTradeSettlement », composé des blocs suivants :
	➢ BT-5 : devise de la facture, sous la balise « ram:InvoiceCurrencyCode »
	➢ BG-22 : groupe des montants totaux de la facture, sous la balise « ram:SpecifiedTradeSettlementHeaderMonetarySummation » :
		▪ BT-109 : montant HT, sous la balise « ram:TaxBasisTotalAmount »
		▪ BT-110 : montant de la TVA, sous la balise « ram:TaxTotalAmount », complété de l’attribut de la devise de comptabilisation de la TVA (la même que la devise de la facture) « @currencyID »
		▪ BT-112 : montant TTC, sous la balise « ram:GrandTotalAmount »
		▪ BT-115 : montant net à payer, sous la balise « ram:DuePayableAmount »
	"""
	applicable_header_trade_settlement = SubElement(supply_chain_trade_transaction,
													"{%s}ApplicableHeaderTradeSettlement" % nsmap['ram'])
	# BT-5
	invoice_currency_code = SubElement(applicable_header_trade_settlement, "{%s}InvoiceCurrencyCode" % nsmap['ram'])
	invoice_currency_code.text = facture.references.devise_facture
	# BG-22
	specified_trade_settlement_header_monetary_summation = SubElement(applicable_header_trade_settlement,
																	  "{%s}SpecifiedTradeSettlementHeaderMonetarySummation" %
																	  nsmap['ram'])
	if level != LEVEL_MINIMUM:
		# BT-107
		allowance_total_amount = SubElement(specified_trade_settlement_header_monetary_summation, "{%s}AllowanceTotalAmount" % nsmap['ram'])
		allowance_total_amount.text = "%.2f" % facture.montant_total.montant_remise_globale_TTC
	# BT-109
	taxbasistotalamount = SubElement(specified_trade_settlement_header_monetary_summation, "{%s}TaxBasisTotalAmount" % nsmap['ram'])
	taxbasistotalamount.text = "%.2f" % facture.montant_total.montant_ht_total
	# BT-110
	taxtotalamount = SubElement(specified_trade_settlement_header_monetary_summation,"{%s}TaxTotalAmount" % nsmap['ram'])
	taxtotalamount.set("currencyID", facture.references.devise_facture)
	taxtotalamount.text = "%.2f" % facture.montant_total.montant_TVA
	# BT-112
	grandtotalamount = SubElement(specified_trade_settlement_header_monetary_summation,"{%s}GrandTotalAmount" % nsmap['ram'])
	grandtotalamount.text = "%.2f" % facture.montant_total.montant_ttc_total
	# BT-115
	duepayableamount = SubElement(specified_trade_settlement_header_monetary_summation, "{%s}DuePayableAmount" % nsmap['ram'])
	duepayableamount.text = "%.2f" % facture.montant_total.montant_a_payer

	return cross_industry_invoice

def gen_facturx_basic(facture: Facture) -> Element:
	cross_industry_invoice = gen_facturx(facture, level=LEVEL_BASIC)
	return cross_industry_invoice


def xml_from_etree(etree):
	# Convertir l'élément en XML
	xml_string = tostring(etree, encoding='utf-8', method='xml', xml_declaration=True, pretty_print=True, )
	return xml_string