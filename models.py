from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CadreDeFacturation(BaseModel):
	code_cadre_facturation: str
	code_service_valideur: Optional[str] = None
	code_structure_valideur: Optional[str] = None

class Destinataire(BaseModel):
	code_destinataire: str
	code_service_executant: Optional[str] = None

class Fournisseur(BaseModel):
	code_coordonnees_bancaires_fournisseur: Optional[int] = 0
	id_fournisseur: int
	id_service_fournisseur: Optional[int] = None

class LignePoste(BaseModel):
	ligne_poste_denomination: str
	ligne_poste_montant_remise_ht: float
	ligne_poste_montant_unitaire_ht: float
	ligne_poste_numero: int
	ligne_poste_quantite: float
	ligne_poste_reference: str
	ligne_poste_taux_tva: str
	ligne_poste_taux_tva_manuel: float
	ligne_poste_unite: str

class LigneTva(BaseModel):
	ligne_tva_montant_base_ht_par_taux: float
	ligne_tva_montant_tva_par_taux: float
	ligne_tva_taux: Optional[str] = None
	ligne_tva_taux_manuel: Optional[float] = None

class MontantTotal(BaseModel):
	montant_a_payer: float
	montant_ht_total: float
	montant_remise_globale_ttc: float
	montant_tva: float
	montant_ttc_total: float
	motif_remise_globale_ttc: str

class PieceJointeComplementaire(BaseModel):
	piece_jointe_complementaire_designation: str
	piece_jointe_complementaire_id: int
	piece_jointe_complementaire_id_liaison: int
	piece_jointe_complementaire_numero_ligne_facture: int
	piece_jointe_complementaire_type: str

class PieceJointePrincipale(BaseModel):
	piece_jointe_principale_designation: str
	piece_jointe_principale_id: int

class References(BaseModel):
	devise_facture: str
	mode_paiement: str
	motif_exoneration_tva: Optional[str] = None
	numero_bon_commande: Optional[str] = None
	numero_facture_origine: Optional[str] = None
	numero_marche: str
	type_facture: str
	type_tva: str

class Facture(BaseModel):
	cadre_de_facturation: CadreDeFacturation
	commentaire: Optional[str]
	date_facture: datetime
	destinataire: Destinataire
	fournisseur: Fournisseur
	id_utilisateur_courant: Optional[int] = 0
	ligne_poste: List[LignePoste]
	ligne_tva: List[LigneTva]
	mode_depot: str
	montant_total: MontantTotal
	numero_facture_saisi: Optional[str] = None
	piece_jointe_complementaire: Optional[List[PieceJointeComplementaire]] = None
	piece_jointe_principale: Optional[List[PieceJointePrincipale]] = None
	references: References

	def to_chorus_pro_payload(self) -> dict:
		# Transformer l'instance en dictionnaire en gérant les champs None
		data = self.dict(by_alias=True, exclude_unset=True)

		# Conversion en format camelCase si nécessaire
		return {
			"modeDepot": data.get("mode_depot"),
			"numeroFactureSaisi": data.get("numero_facture_saisi"),
			"destinataire": {
				"codeDestinataire": self.destinataire.code_destinataire,
				"codeServiceExecutant": getattr(self.destinataire, "code_service_executant", None)
			},
			"fournisseur": {
				"idFournisseur": self.fournisseur.id_fournisseur,
				"codeCoordonneesBancairesFournisseur": getattr(self.fournisseur,
															   "code_coordonnees_bancaires_fournisseur", None),
				"idServiceFournisseur": getattr(self.fournisseur, "id_service_fournisseur", None)
			},
			"cadreDeFacturation": {
				"codeCadreFacturation": self.cadre_de_facturation.code_cadre_facturation,
				"codeStructureValideur": self.cadre_de_facturation.code_structure_valideur
			},
			"references": {
				"deviseFacture": self.references.devise_facture,
				"typeFacture": self.references.type_facture,
				"typeTva": self.references.type_tva,
				"motifExonerationTva": self.references.motif_exoneration_tva,
				"numeroMarche": self.references.numero_marche,
				"numeroBonCommande": self.references.numero_bon_commande,
				"numeroFactureOrigine": self.references.numero_facture_origine,
				"modePaiement": self.references.mode_paiement
			},
			"lignePoste": [
				{
					"lignePosteNumero": lp.ligne_poste_numero,
					"lignePosteReference": lp.ligne_poste_reference,
					"lignePosteDenomination": lp.ligne_poste_denomination,
					"lignePosteQuantite": lp.ligne_poste_quantite,
					"lignePosteUnite": lp.ligne_poste_unite,
					"lignePosteMontantUnitaireHT": lp.ligne_poste_montant_unitaire_ht,
					"lignePosteMontantRemiseHT": lp.ligne_poste_montant_remise_ht,
					"lignePosteTauxTva": lp.ligne_poste_taux_tva,
					"lignePosteTauxTvaManuel": lp.ligne_poste_taux_tva_manuel
				} for lp in self.ligne_poste
			],
			"ligneTva": [
				{
					"ligneTvaTaux": lt.ligne_tva_taux,
					"ligneTvaTauxManuel": lt.ligne_tva_taux_manuel,
					"ligneTvaMontantBaseHtParTaux": lt.ligne_tva_montant_base_ht_par_taux,
					"ligneTvaMontantTvaParTaux": lt.ligne_tva_montant_tva_par_taux
				} for lt in self.ligne_tva
			],
			"montantTotal": {
				"montantHtTotal": self.montant_total.montant_ht_total,
				"montantTVA": self.montant_total.montant_tva,
				"montantTtcTotal": self.montant_total.montant_ttc_total,
				"montantRemiseGlobaleTTC": self.montant_total.montant_remise_globale_ttc,
				"motifRemiseGlobaleTTC": self.montant_total.motif_remise_globale_ttc,
				"montantAPayer": self.montant_total.montant_a_payer
			},
			"commentaire": self.commentaire,
		}

	def to_facturx_basic(self):
		from xml.etree.ElementTree import Element, SubElement, tostring

		# Namespace Factur-X (ceci doit être ajusté selon la norme exacte, ici on se concentre sur la structure)
		ns = {"rsm": "urn:factur-x:basic"}

		# Création de l'élément racine
		invoice = Element('rsm:CrossIndustryInvoice', nsmap=ns)

		# Ajouter l'en-tête de l'invoice
		header_trade = SubElement(invoice, 'rsm:ExchangedDocumentContext')
		header_id = SubElement(header_trade, 'rsm:ID')
		header_id.text = '123456789'  # Exemple d'ID

		# Bloc de l'acheteur (Buyer)
		trade_party_buyer = SubElement(invoice, 'rsm:BuyerTradeParty')
		buyer_id = SubElement(trade_party_buyer, 'rsm:ID')
		buyer_id.text = self.destinataire.code_destinataire

		# Bloc du fournisseur (Seller)
		trade_party_seller = SubElement(invoice, 'rsm:SellerTradeParty')
		seller_id = SubElement(trade_party_seller, 'rsm:ID')
		seller_id.text = str(self.fournisseur.id_fournisseur)

		# Références
		references = SubElement(invoice, 'rsm:ApplicableHeaderTradeAgreement')
		order_reference = SubElement(references, 'rsm:BuyerOrderReferencedDocument')
		order_reference_id = SubElement(order_reference, 'rsm:ID')
		order_reference_id.text = self.references.numero_bon_commande or ''

		# Bloc de la facture (Invoice)
		trade_settlement = SubElement(invoice, 'rsm:ApplicableHeaderTradeSettlement')
		invoice_currency = SubElement(trade_settlement, 'rsm:InvoiceCurrencyCode')
		invoice_currency.text = self.references.devise_facture

		# Montants de la facture
		total_monetary_summation = SubElement(trade_settlement, 'rsm:SpecifiedTradeSettlementMonetarySummation')
		line_total_amount = SubElement(total_monetary_summation, 'rsm:LineTotalAmount')
		line_total_amount.text = str(self.montant_total.montant_ht_total)
		tax_total_amount = SubElement(total_monetary_summation, 'rsm:TaxTotalAmount')
		tax_total_amount.text = str(self.montant_total.montant_tva)
		payable_amount = SubElement(total_monetary_summation, 'rsm:GrandTotalAmount')
		payable_amount.text = str(self.montant_total.montant_a_payer)

		# Ajouter les lignes de la facture (Invoice Lines)
		for i, poste in enumerate(self.ligne_poste, start=1):
			invoice_line = SubElement(invoice, 'rsm:IncludedSupplyChainTradeLineItem')
			line_id = SubElement(invoice_line, 'rsm:AssociatedDocumentLineDocument')
			line_id_value = SubElement(line_id, 'rsm:LineID')
			line_id_value.text = str(poste.ligne_poste_numero)

			line_description = SubElement(invoice_line, 'rsm:SpecifiedTradeProduct')
			item_name = SubElement(line_description, 'rsm:Name')
			item_name.text = poste.ligne_poste_denomination

			# Montant unitaire HT
			trade_price = SubElement(invoice_line, 'rsm:SpecifiedLineTradeAgreement')
			unit_price = SubElement(trade_price, 'rsm:GrossPriceProductTradePrice')
			unit_price_amount = SubElement(unit_price, 'rsm:ChargeAmount')
			unit_price_amount.text = str(poste.ligne_poste_montant_unitaire_ht)

			# Quantité
			trade_delivery = SubElement(invoice_line, 'rsm:SpecifiedLineTradeDelivery')
			billed_quantity = SubElement(trade_delivery, 'rsm:BilledQuantity')
			billed_quantity.text = str(poste.ligne_poste_quantite)

			# Total de la ligne
			trade_settlement = SubElement(invoice_line, 'rsm:SpecifiedLineTradeSettlement')
			net_amount = SubElement(trade_settlement, 'rsm:SpecifiedTradeSettlementLineMonetarySummation')
			net_amount_value = SubElement(net_amount, 'rsm:LineTotalAmount')
			net_amount_value.text = str(poste.ligne_poste_montant_unitaire_ht * poste.ligne_poste_quantite)

			# TVA applicable
			tax = SubElement(trade_settlement, 'rsm:ApplicableTradeTax')
			tax_rate = SubElement(tax, 'rsm:RateApplicablePercent')
			tax_rate.text = str(poste.ligne_poste_taux_tva_manuel)

		# Convertir l'élément en XML
		xml_string = tostring(invoice, encoding='utf-8', method='xml').decode('utf-8')

		return xml_string




