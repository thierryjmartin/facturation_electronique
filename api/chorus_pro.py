import requests
from ..utils.http_client import HttpClient
from ..config import CHORUS_PRO_BASE_URL, PISTE_SANDBOX_URL, PISTE_CLIENT_ID, PISTE_CLIENT_SECRET


class ChorusProAPI:
	def __init__(self):
		self.token = self.get_token()
		self.client = HttpClient(base_url=CHORUS_PRO_BASE_URL, api_key=self.token)

	def get_token(self):
		url = PISTE_SANDBOX_URL
		headers = {
			"content-type": "application/x-www-form-urlencoded"
		}
		data = {
			"grant_type": "client_credentials",
			"client_id": PISTE_CLIENT_ID,
			"client_secret": PISTE_CLIENT_SECRET,
			"scope": "openid"
		}
		response = requests.post(url, headers=headers, data=data, verify=False)
		response.raise_for_status()
		return response.json()['access_token']


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


if __name__ == '__main__':
	c = ChorusProAPI()
	print(c.token)
