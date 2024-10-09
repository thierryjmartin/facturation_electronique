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
		response = self.client.post('/soumettre', json=facture)
		return response.json()

	def obtenir_statut_facture(self, facture_id: str) -> dict:
		"""
		Obtenir le statut d'une facture via son ID.
		:param facture_id: l'identifiant unique de la facture
		:return: dict avec les informations de statut de la facture
		"""
		response = self.client.get(f'/factures/{facture_id}/statut')
		return response.json()


if __name__ == '__main__':
	c = ChorusProAPI()
	print(c.token)

	exemple_facture = {
						  "cadreDeFacturation": {
							"codeCadreFacturation": "A1_FACTURE_FOURNISSEUR",
							"codeServiceValideur": "string",
							"codeStructureValideur": "string"
						  },
						  "commentaire": "string",
						  "dateFacture": "2024-10-08T11:30:23.463Z",
						  "destinataire": {
							"codeDestinataire": "string",
							"codeServiceExecutant": "string"
						  },
						  "fournisseur": {
							"codeCoordonneesBancairesFournisseur": 0,
							"idFournisseur": 0,
							"idServiceFournisseur": 0
						  },
						  "idUtilisateurCourant": 0,
						  "lignePoste": [
							{
							  "lignePosteDenomination": "string",
							  "lignePosteMontantRemiseHT": 0,
							  "lignePosteMontantUnitaireHT": 0,
							  "lignePosteNumero": 0,
							  "lignePosteQuantite": 0,
							  "lignePosteReference": "string",
							  "lignePosteTauxTva": "string",
							  "lignePosteTauxTvaManuel": 0,
							  "lignePosteUnite": "string"
							}
						  ],
						  "ligneTva": [
							{
							  "ligneTvaMontantBaseHtParTaux": 0,
							  "ligneTvaMontantTvaParTaux": 0,
							  "ligneTvaTaux": "string",
							  "ligneTvaTauxManuel": 0
							}
						  ],
						  "modeDepot": "SAISIE_API",
						  "montantTotal": {
							"montantAPayer": 0,
							"montantHtTotal": 0,
							"montantRemiseGlobaleTTC": 0,
							"montantTVA": 0,
							"montantTtcTotal": 0,
							"motifRemiseGlobaleTTC": "string"
						  },
						  "numeroFactureSaisi": "string",
						  "pieceJointeComplementaire": [
							{
							  "pieceJointeComplementaireDesignation": "string",
							  "pieceJointeComplementaireId": 0,
							  "pieceJointeComplementaireIdLiaison": 0,
							  "pieceJointeComplementaireNumeroLigneFacture": 0,
							  "pieceJointeComplementaireType": "string"
							}
						  ],
						  "pieceJointePrincipale": [
							{
							  "pieceJointePrincipaleDesignation": "string",
							  "pieceJointePrincipaleId": 0
							}
						  ],
						  "references": {
							"deviseFacture": "string",
							"modePaiement": "CHEQUE",
							"motifExonerationTva": "string",
							"numeroBonCommande": "string",
							"numeroFactureOrigine": "string",
							"numeroMarche": "string",
							"typeFacture": "AVOIR",
							"typeTva": "TVA_SUR_DEBIT"
						  }
						}

	c.envoyer_facture(exemple_facture)
