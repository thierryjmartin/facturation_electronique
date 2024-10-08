import requests
from ..utils.http_client import HttpClient
from ..config import CHORUS_PRO_BASE_URL, PISTE_SANDBOX_URL, PISTE_CLIENT_ID, PISTE_CLIENT_SECRET


class ChorusProAPI:
	def __init__(self, api_key: str):
		self.client = HttpClient(base_url=CHORUS_PRO_BASE_URL, api_key=api_key)
		self.token = self.get_token()

	def get_token(self):
		url = PISTE_SANDBOX_URL
		headers = {
			"content-type": "application/x-www-form-urlencoded"
		}
		data = {
			"grant_type": "client_credentials",

			"scope": "openid"
		}
		response = requests.post(url, headers=headers, data=data, verify=False)

		# Afficher la réponse
		print(response.json())
		return response.json()


	def envoyer_facture(self, facture: dict) -> dict:
		"""
		Envoyer une facture à Chorus Pro
		:param facture: dict contenant les informations de la facture
		:return: dict avec la réponse de l'API
		"""
		response = self.client.post('/factures', json=facture)
		return response.json()

	def obtenir_statut_facture(self, facture_id: str) -> dict:
		"""
		Obtenir le statut d'une facture via son ID.
		:param facture_id: l'identifiant unique de la facture
		:return: dict avec les informations de statut de la facture
		"""
		response = self.client.get(f'/factures/{facture_id}/statut')
		return response.json()
