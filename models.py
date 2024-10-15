from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

from .utils.strings_and_dicts import to_camel_case, transform_dict_keys


def compare_dicts(dict1, dict2):
	"""
	Compare two dictionaries recursively and return a list of differences.
	"""
	differences = []

	# Check keys in dict1 that are missing or different in dict2
	for key in dict1:
		if key not in dict2:
			differences.append(f"Key '{key}' found in dict1 but missing in dict2")
		else:
			if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
				# Recursively compare nested dictionaries
				differences.extend(
					[f"In key '{key}': {diff}" for diff in compare_dicts(dict1[key], dict2[key])]
				)
			elif dict1[key] != dict2[key]:
				differences.append(f"Value mismatch at key '{key}': dict1={dict1[key]}, dict2={dict2[key]}")

	# Check keys in dict2 that are missing in dict1
	for key in dict2:
		if key not in dict1:
			differences.append(f"Key '{key}' found in dict2 but missing in dict1")

	return differences


class CodeCadreFacturation(str, Enum):
	a1 = "A1_FACTURE_FOURNISSEUR"
	a2 = "A2_FACTURE_FOURNISSEUR_DEJA_PAYEE"
	a3 = "A9_FACTURE_SOUSTRAITANT"
	a4 = "A12_FACTURE_COTRAITANT"


class CadreDeFacturation(BaseModel):
	code_cadre_facturation: str
	code_service_valideur: Optional[str] = CodeCadreFacturation
	"""Si le cadre de facturation est un cadre de facturation de cotraitant ou de sous-traitant (A9, A12) alors le valideur doit obligatoirement être renseigné."""
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
	ligne_poste_montant_remise_HT: float
	ligne_poste_montant_unitaire_HT: float
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
	montant_remise_globale_TTC: float
	montant_TVA: float
	montant_ttc_total: float
	motif_remise_globale_TTC: str

class PieceJointeComplementaire(BaseModel):
	piece_jointe_complementaire_designation: str
	"""Nombre : identifiant technique de la pièce jointe dans le système
	RechercherPieceJointeSurStructure OU RechercherPieceJointeSurMonCompte OU AjouterFichierDansSysteme"""
	piece_jointe_complementaire_id: int
	piece_jointe_complementaire_id_liaison: int
	piece_jointe_complementaire_numero_ligne_facture: int
	piece_jointe_complementaire_type: str

class PieceJointePrincipale(BaseModel):
	'''String : champ libre désignant la pièce jointe max 100 cars'''
	piece_jointe_principale_designation: str
	'''Nombre : identifiant technique de la pièce jointe dans le système
	obtenu par deposerPdfFacture ou ajouterFichierDansSysteme'''
	piece_jointe_principale_id: int


class ModePaiement(str, Enum):
	cheque = "CHEQUE"
	prelevement = "PRELEVEMENT"
	virement = "VIREMENT"
	espece = "ESPECE"
	autre = "AUTRE"
	report = "REPORT"

class TypeFacture(str, Enum):
	facture = 'FACTURE'
	avoir = 'AVOIR'


class TypeTVA(str, Enum):
	"""La valeur à transmettre ici est déduite des données "Régime TVA" et "Exoneration" du format E1,
	selon la règle de gestion suivante :
	- Si aucune ligne de récapitulatifs taxes n'est renseignée, le TypeTVA est 'SANS_TVA'
	- Sinon si la balise RécapitulatifTaxes.Exoneration est renseignée, le TypeTVA est 'EXONERATION'
	- Sinon, le TypeTVA est celui de la balise RegimeTVA (TVA_SUR_DEBIT ou TVA_SUR_ENCAISSEMENT)"""
	tva_sur_debit = 'TVA_SUR_DEBIT'
	tva_sur_encaissment = 'TVA_SUR_ENCAISSEMENT'
	exoneration = 'EXONERATION'
	sans_tva = 'SANS_TVA'


class References(BaseModel):
	devise_facture: str
	mode_paiement: ModePaiement
	motif_exoneration_tva: Optional[str] = None
	'''1) Si le destinataire est l’état, alors le système contrôle l’existence du bon de commande (si renseigné). 
	   2) Si le destinataire indique, au niveau de son paramétrage, que le bon de commande est obligatoire 
		(StructurePublique.gestionNumeroEj = TRUE ou StructurePublique.gestionNumeroEJOuCodeService et code service non renseigné), 
		alors le système contrôle que le bon de commande est renseigné. 
	   3) Dans tous les autres cas, ces paramètres ne sont pas contrôlés.'''
	numero_bon_commande: Optional[str] = None
	'''Ce paramètre est saisissable uniquement si le type de la facture est "Avoir". Sinon, le paramètre est ignoré.'''
	numero_facture_origine: Optional[str] = None
	numero_marche: str
	type_facture: TypeFacture
	type_tva: TypeTVA


class ModeDepot(str, Enum):
	saisie_api = "SAISIE_API"
	depot_pdf_api = "DEPOT_PDF_API"
	depot_pdf_signe_api = "DEPOT_PDF_SIGNE_API"


class Facture(BaseModel):
	cadre_de_facturation: CadreDeFacturation
	destinataire: Destinataire
	fournisseur: Fournisseur
	ligne_poste: Optional[List[LignePoste]] = []
	ligne_tva: Optional[List[LigneTva]] = []
	montant_total: MontantTotal
	piece_jointe_complementaire: Optional[List[PieceJointeComplementaire]] = None
	piece_jointe_principale: Optional[List[PieceJointePrincipale]] = None
	references: References

	"""Obligatoire si le mode de Dépôt est "DEPOT_PDF_API" ou "DEPOT_PDF_SIGNE_API". Cet identifiant est unique par fournisseur. 
	En saisie API, le numeroFacture n’est pas pris en compte mais généré automatiquement par Chorus Pro. Valeur alphanumérique"""
	numero_facture_saisi: Optional[str] = None
	"""Obligatoire si le mode de Dépôt est "DEPOT_PDF_API" ou "DEPOT_PDF_SIGNE_API". Format date : AAAA-MM-JJ
	La date d'émission de la facture doit être antérieure ou égale à la date de dépôt de la facture dans le système."""
	date_facture: Optional[str] = None
	id_utilisateur_courant: Optional[int] = 0
	mode_depot: ModeDepot
	commentaire: Optional[str] # max 200 cars

	def to_chorus_pro_payload(self) -> dict:
		data = self.dict(by_alias=True, exclude_unset=True)
		transformed_data = transform_dict_keys(data, to_camel_case)
		return transformed_data

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




