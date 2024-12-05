import requests
import base64

from ..utils.http_client import HttpClient
try:
	from ..config import *
except ImportError:
	from ..template_config import *


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
		response = self.client.post(f'/factures/v1/consulter/fournisseur', json={'identifiantFactureCPP': facture_id})
		return response.json()

	def ajouter_fichier_dans_systeme(self, fichier: base64 = '', nom: str = '', type_mime: str = '', extension: str = ''):
		"""La méthode ajouterFichierDansSysteme permet d’ajouter une pièce-jointe au compte utilisateur courant
		et d’en obtenir l’identifiant technique. La pièce jointe ne doit pas dépasser 10Mo.
		Si le fichier dépasse cette taille, une erreur 20003 sera remontée.
		:param fichier: String : fichier contenant la piece jointe encodé en base64
		:param nom: Nom du fichier taille max 50 cars
		:param type_mime: format de données de la pièce taille max 255 cars
		:param extension: Liste des extensions des pièces jointes autorisées par Chorus Pro : BMP;HTM;FAX;PNG;XHTML;BZ2;JPEG;PPS;XLC;CSV;JPG;PPT;PPTX ;XLM;DOC ;ODP;RTF;XLS;GIF;ODS;SVG;XML;GZ;ODT;TGZ;XSD;GZIP;P7S;TIF;XSL;HTML;PDF;TXT;ZIP ;TIFF,XLSX;DOC ;DOCX
		:return reponse de l'api
		"""
		response = self.client.post('/transverses/v1/ajouter/fichier', json = {
				"pieceJointeFichier" : fichier,
				"pieceJointeNom" :  nom,
				"pieceJointeTypeMime" : type_mime,
				"pieceJointeExtension" : extension
				})
		response.raise_for_status()
		return response.json()

	def consulter_structure(self, id_structure: int) -> dict:
		reponse = self.client.post('/structures/v1/consulter', json={'codeLangue': 'fr', 'idStructureCPP': id_structure})
		return reponse.json()

	def rechercher_structure(self, payload) -> dict:
		reponse = self.client.post('/structures/v1/rechercher', json=payload)
		return reponse.json()

	def rechercher_services_structure(self, id_structure: int) -> dict:
		reponse = self.client.post('/structures/v1/rechercher/services', json={"idStructure": id_structure})
		return reponse.json()

	def obtenir_identifiant_cpro_depuis_siret(self, siret:str, type_identifiant:str='SIRET') -> int:
		# "SIRET", "UE_HORS_FRANCE", "HORS_UE", "RIDET", "TAHITI", "AUTRE", "PARTICULIER"
		payload = {
			"restreindreStructuresPrivees": False,
			"structure": {
				"identifiantStructure": siret,
				"typeIdentifiantStructure": type_identifiant,
			}
		}
		recherche_structure = self.rechercher_structure(payload)
		identifiant_cpro = 0
		if recherche_structure["parametresRetour"]["total"] == 1:
			identifiant_cpro = recherche_structure["listeStructures"][0]["idStructureCPP"]
		return identifiant_cpro



