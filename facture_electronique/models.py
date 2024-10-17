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

class PostalAddress(BaseModel):
	postcode: Optional[str] = None
	line_one: Optional[str] = None
	city_name: Optional[str] = None
	pays_code_iso: Optional[str] = ''  # utilisé dans facturx mais pas dans l'API Chorus

class Destinataire(BaseModel):
	nom: Optional[str] = '' # utilisé dans facturx mais pas dans l'API Chorus
	postal_trade_address: Optional[PostalAddress] = None  # utilisé dans facturx mais pas dans l'API Chorus
	code_destinataire: str # SIRET
	code_service_executant: Optional[str] = None


class Fournisseur(BaseModel):
	nom: Optional[str] = '' # utilisé dans facturx mais pas dans l'API Chorus
	siret: Optional[str] = ''  # utilisé dans facturx mais pas dans l'API Chorus
	numero_tva_intra: Optional[str] = '' # utilisé dans facturx mais pas dans l'API Chorus
	postal_trade_address: Optional[PostalAddress] = None  # utilisé dans facturx mais pas dans l'API Chorus
	code_coordonnees_bancaires_fournisseur: Optional[int] = 0
	id_fournisseur: int # identifiant chorus pro
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
	id_utilisateur_courant: Optional[int] = 0
	mode_depot: ModeDepot
	commentaire: Optional[str] # max 200 cars

	def to_chorus_pro_payload(self) -> dict:
		data = self.dict(by_alias=True, exclude_unset=True)
		cle_a_detruire = [ # des champs sont pour facturx mais ne fonctionnent pas dans la payload cpro
			("fournisseur", "pays_code_iso"),
			("fournisseur", "nom"),
			("fournisseur", "siret"),
			("destinataire", "nom"),
		]
		for elt in cle_a_detruire:
			try:
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




