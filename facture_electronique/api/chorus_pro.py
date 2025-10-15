import requests
import base64

from ..utils.http_client import HttpClient

try:
    from ..config import (
        PISTE_CLIENT_ID,
        PISTE_CLIENT_SECRET,
        PISTE_OAUTH_URL,
        PISTE_SANDBOX_OAUTH_URL,
        CHORUS_PRO_LOGIN,
        CHORUS_PRO_PASSWORD,
        CHORUS_PRO_FACTURES_BASE_URL,
        CHORUS_PRO_SANDBOX_FACTURES_BASE_URL,
    )
except ImportError:
    from ..template_config import (
        PISTE_CLIENT_ID,
        PISTE_CLIENT_SECRET,
        PISTE_OAUTH_URL,
        PISTE_SANDBOX_OAUTH_URL,
        CHORUS_PRO_LOGIN,
        CHORUS_PRO_PASSWORD,
        CHORUS_PRO_FACTURES_BASE_URL,
        CHORUS_PRO_SANDBOX_FACTURES_BASE_URL,
    )


class ChorusProAPI:
    def __init__(
        self,
        sandbox: bool = True,
        piste_client_id: str = "",
        piste_client_secret: str = "",
        cpro_login: str = "",
        cpro_password: str = "",
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
        headers = {"content-type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.piste_client_id,
            "client_secret": self.piste_client_secret,
            "scope": "openid",
        }
        response = requests.post(url, headers=headers, data=data, verify=False)
        response.raise_for_status()
        return response.json()["access_token"]

    def cpro_account(self):
        """
        Identifiant compte CPRO sous la forme 'login:password' encodé en base 64.
        Exemple : 'bG9naW46cGFzc3dvcmQ='
        """
        return base64.b64encode(
            bytes(f"{self.cpro_login}:{self.cpro_password}", "utf-8")
        ).decode("utf-8")

    def envoyer_facture(self, facture: dict) -> dict:
        """
        Envoyer une facture à Chorus Pro
        :param facture: dict contenant les informations de la facture
        :return: dict avec la réponse de l'API
        """
        response = self.client.post("/factures/v1/soumettre", json=facture)
        return response.json()

    def obtenir_statut_facture(self, facture_id: str) -> dict:
        """
        Obtenir le statut d'une facture via son ID.
        :param facture_id: l'identifiant unique de la facture
        :return: dict avec les informations de statut de la facture
        """
        response = self.client.post(
            "/factures/v1/consulter/fournisseur",
            json={"identifiantFactureCPP": facture_id},
        )
        return response.json()

    def ajouter_fichier_dans_systeme(
        self, fichier: str = "", nom: str = "", type_mime: str = "", extension: str = ""
    ):
        """La méthode ajouterFichierDansSysteme permet d’ajouter une pièce-jointe au compte utilisateur courant
        et d’en obtenir l’identifiant technique. La pièce jointe ne doit pas dépasser 10Mo.
        Si le fichier dépasse cette taille, une erreur 20003 sera remontée.
        :param fichier: String : fichier contenant la piece jointe encodé en base64
        :param nom: Nom du fichier taille max 50 cars
        :param type_mime: format de données de la pièce taille max 255 cars
        :param extension: Liste des extensions des pièces jointes autorisées par Chorus Pro : BMP;HTM;FAX;PNG;XHTML;BZ2;JPEG;PPS;XLC;CSV;JPG;PPT;PPTX ;XLM;DOC ;ODP;RTF;XLS;GIF;ODS;SVG;XML;GZ;ODT;TGZ;XSD;GZIP;P7S;TIF;XSL;HTML;PDF;TXT;ZIP ;TIFF,XLSX;DOC ;DOCX
        :return reponse de l'api
        """
        response = self.client.post(
            "/transverses/v1/ajouter/fichier",
            json={
                "pieceJointeFichier": fichier,
                "pieceJointeNom": nom,
                "pieceJointeTypeMime": type_mime,
                "pieceJointeExtension": extension,
            },
        )
        response.raise_for_status()
        return response.json()

    def consulter_structure(self, id_structure: int) -> dict:
        reponse = self.client.post(
            "/structures/v1/consulter",
            json={"codeLangue": "fr", "idStructureCPP": id_structure},
        )
        return reponse.json()

    def rechercher_organisation_siren(self, payload) -> dict:
        """
        FIXME n'a pas l'air de fonctionner... l'url n'est pas reconnue par le serveur
        https://communaute.chorus-pro.gouv.fr/documentation/base-sirene-des-entreprises-et-de-leurs-etablissements/
        Cette méthode peut rechercher les données d'une structure de type SIREN. Pour les recherches multicritères,
        le champ '_fields' permet de préciser les champs retournés par l'API. Par exemple, si on met dans le corps
        '_fields' : ['libelleOrganisation', 'raisonSociale', 'adresseElectronique'],
        la demande de retour ne contiendra que ces champs.
        Exemple [{ 'raisonSociale' : 'DIRECTION GENERALE DE L'AVIATION CIVILE ' , 'libelleOrganisation' :
        'TEST', 'adresseElectronique' : 'test@gmail.com', }]. Pour le tri, nous mettrons un tableau '_sort'.
        Les données de réponse seront triées par les champs de ce tableau.
        Par exemple : '_sort': ['libelleOrganisation','adresse','identifiant'].
        Pour le tri par ordre décroissant, nous utiliserons le même tableau mais avec le nom '_desc'.
        Par exemple : '_desc': ['ville','pays']. L'attribut structure doit être spécifié pour la recherche.
        """
        reponse = self.client.post("/organisations/v1/siren/recherche", json=payload)
        return reponse.json()

    def rechercher_structure_via_organisation(self, payload) -> dict:
        """
        https://communaute.chorus-pro.gouv.fr/documentation/base-sirene-des-entreprises-et-de-leurs-etablissements/
        Cette méthode permet de rechercher les données sur les structures
        Pour la recherche multicritères, le champ '_fields' permet de déterminer les champs retournés par l'API.
        Par exemple si l'on met dans le body '_fields': ['typeOrganisation', 'raisonSociale', 'numeroEjDoitEtreRenseigne'],
        les retours de la requête ne comprendront que ces champs exemple [{ 'raisonSociale':
        'DIRECTION GENERALE DE L'AVIATION CIVILE', 'typeOrganisation': 'PUBLIQUE', 'numeroEjDoitEtreRenseigne': true, }]
        Un attribut de la structure doit être renseigné pour la recherche.
        """
        reponse = self.client.post(
            "/organisations/v1/structures/recherche", json=payload
        )
        return reponse.json()

    def rechercher_structure(self, payload) -> dict:
        """
        La méthode rechercherStructure permet à un gestionnaire de rechercher des structures.
        https://communaute.chorus-pro.gouv.fr/documentation/guide-dutilisation-de-lannuaire-des-structures-publiques-dans-chorus-pro/
        """
        reponse = self.client.post("/structures/v1/rechercher", json=payload)
        return reponse.json()

    def rechercher_services_structure(self, id_structure: int) -> dict:
        reponse = self.client.post(
            "/structures/v1/rechercher/services", json={"idStructure": id_structure}
        )
        return reponse.json()

    def consulter_service_structure(self, id_structure: int, id_service: int) -> dict:
        """
        Consult a specific service associated with a given structure by their respective IDs.

        Sends a POST request to the endpoint '/structures/v1/consulter/service' to retrieve
        details of the service linked to a particular structure, based on the provided structure
        and service IDs. Returns the response in JSON format.

        Parameters:
        id_structure: int
            The Chorus Pro ID of the structure whose service details are to be consulted.
        id_service: int
            The Chorus Pro ID of the service to be consulted within the structure.

        Returns:
        dict
            {
                  "adressePostale": {
                        "adresse": "string",
                        "codePostal": "string",
                        "complementAdresse1": "string",
                        "complementAdresse2": "string",
                        "fax": "string",
                        "indicatifFax": "string",
                        "indicatifTelephone": "string",
                        "pays": "string",
                        "telephone": "string",
                        "ville": "string"
                  },
                  "codeRetour": 0,
                  "informationsGenerales": {
                        "codeService": "string",
                        "descriptionService": "string",
                        "nomService": "string"
                  },
                  "libelle": "TRA_MSG_00.000",
                  "nbResultatsParPage": 0,
                  "pageCourante": 0,
                  "pages": 0,
                  "parametres": {
                        "dateCreation": "2024-12-09T13:18:46.376Z",
                        "dateDebutValidite": "2024-12-09T13:18:46.376Z",
                        "dateFinValidite": "2024-12-09T13:18:46.376Z",
                        "dateModification": "2024-12-09T13:18:46.376Z",
                        "miseEnPaiement": true,
                        "numeroEngagement": true
                  },
                  "total": 0
                }
        """
        reponse = self.client.post(
            "/structures/v1/consulter/service",
            json={"idStructure": id_structure, "idService": id_service},
        )
        return reponse.json()

    def obtenir_identifiant_cpro_depuis_siret(
        self, siret: str, type_identifiant: str = "SIRET"
    ) -> int:
        # "SIRET", "UE_HORS_FRANCE", "HORS_UE", "RIDET", "TAHITI", "AUTRE", "PARTICULIER"
        payload = {
            "restreindreStructuresPrivees": False,
            "structure": {
                "identifiantStructure": siret,
                "typeIdentifiantStructure": type_identifiant,
            },
        }
        recherche_structure = self.rechercher_structure(payload)
        identifiant_cpro = 0
        if recherche_structure["parametresRetour"]["total"] == 1:
            identifiant_cpro = recherche_structure["listeStructures"][0][
                "idStructureCPP"
            ]
        return identifiant_cpro
