from ..models import Facture, TypeFacture
from lxml.etree import Element, SubElement, tostring
from datetime import datetime

def gen_facturx_minimum(facture: Facture, bt_24="urn:factur-x.eu:1p0:minimum") -> Element:
	"""
	Pour Chorus Pro, permet de générer un xml qui représente une facture CleverIP selon le standard Chorus Pro (MINIMUM)
	:return: un fichier XML au format facture-x représentant la facture envoyée en argument
	"""

	nsmap = {
		'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
		'udt': 'urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100',
		'qdt': 'urn:un:unece:uncefact:data:standard:QualifiedDataType:100',
		'ram': 'urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100',
		'rsm': 'urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100',
	}
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
	# BT-24
	guide_line_scpecified_document_context_parameter = SubElement(exchanged_document_context,
																  "{%s}GuidelineSpecifiedDocumentContextParameter" %
																  nsmap['ram'])
	id = SubElement(guide_line_scpecified_document_context_parameter, "{%s}ID" % nsmap['ram'])
	id.text = bt_24

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
		datetimestring.text = datetime.strptime(facture.date_facture, "%Y-%m-%d").strftime("%Y%m%d")
	else:
		datetimestring.text = datetime.date.today().strftime("%Y%m%d")

	# BG-1 included_note. pas décrit dans le format "minimum" mais "basic" car le XSD basis minimum est commun
	# included_note = SubElement(exchanged_document, "{%s}IncludedNote" % nsmap['ram'])
	# BT-22
	# included_note_content = SubElement(included_note, "{%s}Content" % nsmap['ram'])
	# included_note_content.text = " "
	# BT-21
	# included_note_subjectcode = SubElement(included_note, "{%s}SubjectCode" % nsmap['ram'])
	# included_note_subjectcode.text = " "

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
	country_id.text = facture.fournisseur.pays_code_iso
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
	# BT-13
	buyer_order_referenced_document = SubElement(applicable_header_trade_agreement,
												 "{%s}BuyerOrderReferencedDocument" % nsmap['ram'])
	issuer_assigned_id = SubElement(buyer_order_referenced_document, "{%s}IssuerAssignedID" % nsmap['ram'])
	# a priori optionel
	issuer_assigned_id.text = facture.references.numero_bon_commande
	# BT-12 Identifiant de contrat, référence de document (pour valider XML)
	# contract_referenced_document = SubElement(applicable_header_trade_agreement, "{%s}ContractReferencedDocument" % nsmap['ram'])
	# issuer_assigned_id = SubElement(contract_referenced_document, "{%s}IssuerAssignedID" % nsmap['ram'])
	# a priori optionel
	# issuer_assigned_id.text = facture.references.numero_marche  # numéro de contrat obligatoire pour valider le xml...

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
	cross_industry_invoice = gen_facturx_minimum(facture, bt_24="urn:cen.eu:EN 16931:2017#compliant#urn:factur-x.eu:1p0:basic")

	return cross_industry_invoice


def xml_from_etree(etree):
	# Convertir l'élément en XML
	xml_string = tostring(etree, encoding='utf-8', method='xml')
	return xml_string