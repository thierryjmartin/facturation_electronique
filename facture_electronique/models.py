from pydantic import BaseModel, PositiveFloat
from enum import Enum
from typing import List, Optional

from .utils.strings_and_dicts import to_camel_case, transform_dict_keys


class CodeCadreFacturation(str, Enum):
	a1 = "A1_FACTURE_FOURNISSEUR"
	a2 = "A2_FACTURE_FOURNISSEUR_DEJA_PAYEE"
	a3 = "A9_FACTURE_SOUSTRAITANT"
	a4 = "A12_FACTURE_COTRAITANT"


class CadreDeFacturation(BaseModel):
	code_cadre_facturation: str
	code_service_valideur: Optional[CodeCadreFacturation] = "A1_FACTURE_FOURNISSEUR"
	"""Si le cadre de facturation est un cadre de facturation de cotraitant ou de sous-traitant (A9, A12) alors le valideur doit obligatoirement être renseigné."""
	code_structure_valideur: Optional[str] = None


class AdressePostale(BaseModel):
	code_postal: Optional[str] = None
	ligne_un: Optional[str] = None
	ligne_deux: Optional[str] = None
	nom_ville: Optional[str] = None
	pays_code_iso: Optional[str] = ''


class Destinataire(BaseModel):
	nom: Optional[str] = '' # utilisé dans facturx mais pas dans l'API Chorus
	adresse_postale: Optional[AdressePostale] = None  # utilisé dans facturx mais pas dans l'API Chorus
	code_destinataire: str # SIRET
	code_service_executant: Optional[str] = None


class Fournisseur(BaseModel):
	nom: Optional[str] = '' # utilisé dans facturx mais pas dans l'API Chorus
	siret: Optional[str] = ''  # utilisé dans facturx mais pas dans l'API Chorus
	numero_tva_intra: Optional[str] = '' # utilisé dans facturx mais pas dans l'API Chorus
	adresse_postale: Optional[AdressePostale] = None  # utilisé dans facturx mais pas dans l'API Chorus
	code_coordonnees_bancaires_fournisseur: Optional[int] = 0
	id_fournisseur: int # identifiant chorus pro
	id_service_fournisseur: Optional[int] = None


class TvaCategories(str, Enum):
	# Défini dans facturx BASIC - Invoiced item VAT category code
	# The VAT category codes are as follows:
	tva_cat_S = 'S' # S = Standard VAT rate (standard)
	tva_cat_zero_rated_good = 'Z' # Z = Zero rated goods (NON APPLICABLE EN FRANCE)
	tva_cat_exempt = 'E' # E = VAT exempt
	tva_cat_reverse_charge = 'AE' # AE = Reverse charge
	tva_cat_intra_community_supply = 'K' # K = Intra-Community supply (specific reverse charge)
	tva_cat_export_outside_EU = 'G' # G = Exempt VAT for Export outside EU
	tva_cat_outside_vat_scope = 'O' # O = Outside VAT scope
	tva_cat_canary = 'L' # L = Canary Islands
	tva_cat_ceuta = 'M' # M = Ceuta and Mellila


class RaisonReductionCode(str, Enum):
	raison_reduction_code_advertising = 'AA' # AA = Advertising discount
	raison_reduction_packing_supplement = 'ABL' # ABL = Packing supplement
	raison_reduction_code_other_services = 'ADR' # ADR = Other services
	raison_reduction_code_removal = 'ADT' # ADT = Removal
	raison_reduction_cdoe_transportation_cost = 'FC' # FC = transportation costs
	raison_reduction_code_financial_expences = 'FI' # FI = Financial expenses
	raison_reduction_code_labeling = 'LA' # LA = Labeling


class LignePoste(BaseModel):
	ligne_poste_numero: int
	ligne_poste_reference: str
	ligne_poste_denomination: str
	ligne_poste_quantite: float
	ligne_poste_unite: str
	ligne_poste_montant_unitaire_HT: PositiveFloat
	ligne_poste_montant_remise_HT: float
	ligne_poste_taux_tva: str
	ligne_poste_taux_tva_manuel: float
	ligne_poste_tva_categorie: Optional[TvaCategories] = None  # pour facturx basic
	ligne_poste_date_debut: Optional[str] = None  # pour facturx basic
	ligne_poste_date_fin : Optional[str] = None # pour facturx basic
	ligne_poste_code_raison_reduction_code: Optional[RaisonReductionCode] = None # pour facturx basic
	ligne_poste_code_raison_reduction: Optional[str] = None


class LigneTva(BaseModel):
	ligne_tva_montant_base_ht_par_taux: float
	ligne_tva_montant_tva_par_taux: float
	ligne_tva_taux: Optional[str] = None
	ligne_tva_taux_manuel: Optional[float] = None
	ligne_tva_categorie: Optional[TvaCategories] = None  # pour facturx basic


class MontantTotal(BaseModel):
	acompte: Optional[float] = 0 # facturx basic.
	montant_a_payer: float
	montant_ht_total: float
	montant_remise_globale_TTC: float # les remises globales TTC ne vont pas avec Chorus pro, il faudrait plutot des lignes de remises HT ou charges HT avec chacune leur taux de tva
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
	piece_jointe_principale_id: Optional[int] = 0


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
	date_echeance_paiement: Optional[str] = None # obligatoire pour facturx basic
	id_utilisateur_courant: Optional[int] = 0
	mode_depot: ModeDepot
	commentaire: Optional[str] # max 200 cars

	def to_chorus_pro_payload(self) -> dict:
		data = self.dict(by_alias=True, exclude_unset=True)
		cle_a_detruire = [ # des champs sont pour facturx mais ne fonctionnent pas dans la payload cpro
			("date_echeance_paiement", ),
			("fournisseur", "pays_code_iso"),
			("fournisseur", "nom"),
			("fournisseur", "siret"),
			("destinataire", "nom"),
			("montant_total", "acompte")
		]
		for elt in cle_a_detruire:
			try:
				if len(elt) == 1:
					del data[elt[0]]
				else:
					del data[elt[0]][elt[1]]
			except KeyError:
				# element inexistant, c'est ce qu'on veut
				continue
		transformed_data = transform_dict_keys(data, to_camel_case)
		return transformed_data

	def to_facturx_minimum(self):
		from .utils.facturx import gen_facturx_minimum
		return gen_facturx_minimum(self)

	def to_facturx_basic(self):
		from .utils.facturx import gen_facturx_basic
		return gen_facturx_basic(self)




