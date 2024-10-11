import requests
import base64
from ..utils.http_client import HttpClient
from ..config import *


class ChorusProAPI:
	def __init__(self,
				 sandbox: bool=True,
				 piste_client_id: str = '',
				 piste_client_secret: str = '',
				 cpro_login: str = '',
				 cpro_password: str = '',
				 ):
		self.sandbox = sandbox
		self.piste_client_id = piste_client_id or PISTE_CLIENT_ID
		self.piste_client_secret = piste_client_secret or PISTE_CLIENT_SECRET
		self.cpro_login = cpro_login or CHORUS_PRO_LOGIN
		self.cpro_password = cpro_password or CHORUS_PRO_PASSWORD

		self.token = self.get_token()
		url = CHORUS_PRO_FACTURES_BASE_URL
		if self.sandbox:
			url = CHORUS_PRO_SANDBOX_FACTURES_BASE_URL
		self.client = HttpClient(base_url=url, api_key=self.token)
		self.client.headers["cpro-account"] = self.cpro_account()

	def get_token(self):
		url = PISTE_OAUTH_URL
		if self.sandbox:
			url = PISTE_SANDBOX_OAUTH_URL
		headers = {
			"content-type": "application/x-www-form-urlencoded"
		}
		data = {
			"grant_type": "client_credentials",
			"client_id": self.piste_client_id,
			"client_secret": self.piste_client_secret,
			"scope": "openid"
		}
		response = requests.post(url, headers=headers, data=data, verify=False)
		response.raise_for_status()
		return response.json()['access_token']

	def cpro_account(self):
		"""
		Identifiant compte CPRO sous la forme 'login:password' encodé en base 64.
		Exemple : 'bG9naW46cGFzc3dvcmQ='
		"""
		return base64.b64encode(bytes(f"{self.cpro_login}:{self.cpro_password}", 'utf-8')).decode('utf-8')

	def envoyer_facture(self, facture: dict) -> dict:
		"""
		Envoyer une facture à Chorus Pro
		:param facture: dict contenant les informations de la facture
		:return: dict avec la réponse de l'API
		"""
		response = self.client.post('/factures/v1/soumettre', json=facture)
		return response.json()

	def obtenir_statut_facture(self, facture_id: str) -> dict:
		"""
		Obtenir le statut d'une facture via son ID.
		:param facture_id: l'identifiant unique de la facture
		:return: dict avec les informations de statut de la facture
		"""
		response = self.client.get(f'/factures/{facture_id}/statut')
		return response.json()

	def consulter_structure(self, id_structure: int) -> dict:
		reponse = self.client.post('/structures/v1/consulter', json={'codeLangue': 'fr', 'idStructureCPP': id_structure})
		return reponse.json()

	def rechercher_structure(self, payload) -> dict:
		reponse = self.client.post('/structures/v1/rechercher', json=payload)
		return reponse.json()


if __name__ == '__main__':
	c = ChorusProAPI()
	print(c.token)

	# exemple_facture = {
	# 					  "cadreDeFacturation": {
	# 						"codeCadreFacturation": "A1_FACTURE_FOURNISSEUR",
	# 						"codeServiceValideur": "string",
	# 						"codeStructureValideur": "string"
	# 					  },
	# 					  "commentaire": "string",
	# 					  "dateFacture": "2024-10-08T11:30:23.463Z",
	# 					  "destinataire": {
	# 						"codeDestinataire": "string",
	# 						"codeServiceExecutant": "string"
	# 					  },
	# 					  "fournisseur": {
	# 						"codeCoordonneesBancairesFournisseur": 0,
	# 						"idFournisseur": "26073617692140",
	# 						"idServiceFournisseur": "SERVICE_PRIVE_1_26073617692140",
	# 					  },
	# 					  "idUtilisateurCourant": 0,
	# 					  "lignePoste": [
	# 						{
	# 						  "lignePosteDenomination": "string",
	# 						  "lignePosteMontantRemiseHT": 0,
	# 						  "lignePosteMontantUnitaireHT": 0,
	# 						  "lignePosteNumero": 0,
	# 						  "lignePosteQuantite": 0,
	# 						  "lignePosteReference": "string",
	# 						  "lignePosteTauxTva": "string",
	# 						  "lignePosteTauxTvaManuel": 0,
	# 						  "lignePosteUnite": "string"
	# 						}
	# 					  ],
	# 					  "ligneTva": [
	# 						{
	# 						  "ligneTvaMontantBaseHtParTaux": 0,
	# 						  "ligneTvaMontantTvaParTaux": 0,
	# 						  "ligneTvaTaux": "string",
	# 						  "ligneTvaTauxManuel": 0
	# 						}
	# 					  ],
	# 					  "modeDepot": "SAISIE_API",
	# 					  "montantTotal": {
	# 						"montantAPayer": 0,
	# 						"montantHtTotal": 0,
	# 						"montantRemiseGlobaleTTC": 0,
	# 						"montantTVA": 0,
	# 						"montantTtcTotal": 0,
	# 						"motifRemiseGlobaleTTC": "string"
	# 					  },
	# 					  "numeroFactureSaisi": "string",
	# 					  "pieceJointeComplementaire": [
	# 						{
	# 						  "pieceJointeComplementaireDesignation": "string",
	# 						  "pieceJointeComplementaireId": 0,
	# 						  "pieceJointeComplementaireIdLiaison": 0,
	# 						  "pieceJointeComplementaireNumeroLigneFacture": 0,
	# 						  "pieceJointeComplementaireType": "string"
	# 						}
	# 					  ],
	# 					  "pieceJointePrincipale": [
	# 						{
	# 						  "pieceJointePrincipaleDesignation": "string",
	# 						  "pieceJointePrincipaleId": 0
	# 						}
	# 					  ],
	# 					  "references": {
	# 						"deviseFacture": "string",
	# 						"modePaiement": "CHEQUE",
	# 						"motifExonerationTva": "string",
	# 						"numeroBonCommande": "string",
	# 						"numeroFactureOrigine": "string",
	# 						"numeroMarche": "string",
	# 						"typeFacture": "AVOIR",
	# 						"typeTva": "TVA_SUR_DEBIT"
	# 					  }
	# 					}

	exemple_facture = {
		"modeDepot": "SAISIE_API",
		"numeroFactureSaisi": None,

		"destinataire": {
			"codeDestinataire": "99986401570264", # SIRET  trouvé via une recherche...
			#"codeServiceExecutant": "DIRINFRA"
		},
		"fournisseur": {
			# j'ai retrouvé ce code en faisant une recherche de fournisseur..., j'aurais pu chercher par siret ?
			# le SIRET de mon fournisseur 26073617692140
			"idFournisseur": 26300989,
			#"typeIdentifiantFournisseur": "SIRET",
		#	"idServiceFournisseur": 26073617692140,
		#	"codeCoordonneesBancairesFournisseur": 132
		},
		"cadreDeFacturation": {
			"codeCadreFacturation": "A1_FACTURE_FOURNISSEUR",
			"codeStructureValideur": None
		},
		"references": {
			"deviseFacture": "EUR",
			"typeFacture": "FACTURE",
			"typeTva": "TVA_SUR_DEBIT",
			"motifExonerationTva": None,
			"numeroMarche": "VABFM001",
			"numeroBonCommande": None,
			"numeroFactureOrigine": None,
			"modePaiement": "ESPECE"
		},
		"lignePoste": [
			{
				"lignePosteNumero": 1,
				"lignePosteReference": "R1",
				"lignePosteDenomination": "D1",
				"lignePosteQuantite": 10,
				"lignePosteUnite": "lot",
				"lignePosteMontantUnitaireHT": 50.000000,
				"lignePosteMontantRemiseHT": None,
				"lignePosteTauxTva": "TVA5",
				"lignePosteTauxTvaManuel": None
			}
			, {
				"lignePosteNumero": 2,
				"lignePosteReference": "R2",
				"lignePosteDenomination": "D2",
				"lignePosteQuantite": 12,
				"lignePosteUnite": "Kg",
				"lignePosteMontantUnitaireHT": 36.000000,
				"lignePosteMontantRemiseHT": None,
				"lignePosteTauxTva": None,
				"lignePosteTauxTvaManuel": 2.1
			}
			, {
				"lignePosteNumero": 3,
				"lignePosteReference": "R3",
				"lignePosteDenomination": "D3",
				"lignePosteQuantite": 16,
				"lignePosteUnite": "lot",
				"lignePosteMontantUnitaireHT": 24.000000,
				"lignePosteMontantRemiseHT": None,
				"lignePosteTauxTva": None,
				"lignePosteTauxTvaManuel": 5
			}
			, {
				"lignePosteNumero": 4,
				"lignePosteReference": "XX",
				"lignePosteDenomination": "XX",
				"lignePosteQuantite": 1,
				"lignePosteUnite": "lot",
				"lignePosteMontantUnitaireHT": 10.000000,
				"lignePosteMontantRemiseHT": None,
				"lignePosteTauxTva": "TVA5",
				"lignePosteTauxTvaManuel": None
			}
		],
		"ligneTva": [
			{
				"ligneTvaTauxManuel": None,
				"ligneTvaTaux": "TVA5",
				"ligneTvaMontantBaseHtParTaux": 510.000000,
				"ligneTvaMontantTvaParTaux": 102.000000
			}
			, {
				"ligneTvaTauxManuel": 2.1,
				"ligneTvaTaux": None,
				"ligneTvaMontantBaseHtParTaux": 432.000000,
				"ligneTvaMontantTvaParTaux": 9.072000
			}
			, {
				"ligneTvaTauxManuel": 5,
				"ligneTvaTaux": None,
				"ligneTvaMontantBaseHtParTaux": 384.000000,
				"ligneTvaMontantTvaParTaux": 19.200000
			}
		],
		"montantTotal": {
			"montantHtTotal": 1326.000000,
			"montantTVA": 130.272000,
			"montantTtcTotal": 1406.272000,
			"montantRemiseGlobaleTTC": 50.000000,
			"motifRemiseGlobaleTTC": "Geste commercial",
			"montantAPayer": 1400.000000
		},
		"commentaire": "Création_VABF_SoumettreFacture"
	}

	c.envoyer_facture(exemple_facture)
	c.consulter_structure(26300989)
	#c.consulter_structure(1)

	payload={
			  "parametres": {
				"nbResultatsParPage": 10,
				"pageResultatDemandee": 1,
				"triColonne": "IdentifiantStructure",
				"triSens": "Descendant"
			  },
			  "restreindreStructuresPrivees": False,
			  "structure": {
				#"adresseCodePays": "string",
				#"adresseCodePostal": "string",
				#"adresseVille": "string",
				#"estMOA": true,
				#"estMOAUniquement": true,
				"identifiantStructure": "26073617692140",
				#"libelleStructure": "string",
				#"nomStructure": "string",
				#"prenomStructure": "string",
				#"raisonSocialeStructure": "string",
				#"statutStructure": "ACTIF",
				"typeIdentifiantStructure": "SIRET",
				#"typeStructure": "PUBLIQUE"
			  }
			}

	c.rechercher_structure(payload)
