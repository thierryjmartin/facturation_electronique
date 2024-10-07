from ..utils.http_client import HttpClient
from ..config import DPGF_BASE_URL


class DPGFAPI:
	def __init__(self, api_key: str):
		self.client = HttpClient(base_url=DPGF_BASE_URL, api_key=api_key)

	def envoyer_facture(self, facture: dict) -> dict:
		"""
		Envoyer une facture à DPGF
		"""
		response = self.client.post('/factures', json=facture)
		return response.json()
