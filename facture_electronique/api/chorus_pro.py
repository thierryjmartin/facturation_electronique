import requests
import base64
import os

from ..utils.http_client import HttpClient
from ..exceptions import ErreurConfiguration


class ChorusProAPI:
    """Client pour interagir avec l'API Chorus Pro.

    Cette classe gère l'authentification auprès de PISTE (le portail d'API du gouvernement)
    et fournit des méthodes pour les opérations courantes sur Chorus Pro, comme la soumission
    et la consultation de factures.

    L'authentification et la session HTTP sont initialisées de manière paresseuse,
    c'est-à-dire uniquement lors du premier appel à une méthode de l'API.
    """

    URL_OAUTH_PROD = "https://oauth.piste.gouv.fr/api/oauth/token"
    URL_OAUTH_SANDBOX = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"
    URL_API_PROD = "https://api.piste.gouv.fr/cpro"
    URL_API_SANDBOX = "https://sandbox-api.piste.gouv.fr/cpro"

    def __init__(
        self,
        sandbox: bool = True,
        identifiant_client_piste: str = None,
        secret_client_piste: str = None,
        identifiant_cpro: str = None,
        mot_de_passe_cpro: str = None,
    ):
        """Initialise le client API.

        Les paramètres peuvent être fournis directement ou lus depuis les variables d'environnement.

        :param sandbox: Si True, utilise l'environnement de sandbox de Chorus Pro. Par défaut à True.
        :param identifiant_client_piste: L'identifiant client pour l'API PISTE.
                Peut être lu depuis la variable d'environnement `PISTE_CLIENT_ID`.
        :param secret_client_piste: Le secret client pour l'API PISTE.
                Peut être lu depuis la variable d'environnement `PISTE_CLIENT_SECRET`.
        :param identifiant_cpro: Le login de l'utilisateur pour Chorus Pro.
                Peut être lu depuis la variable d'environnement `CHORUS_PRO_LOGIN`.
        :param mot_de_passe_cpro: Le mot de passe de l'utilisateur pour Chorus Pro.
                Peut être lu depuis la variable d'environnement `CHORUS_PRO_PASSWORD`.
        :raises ErreurConfiguration: Si une des informations requises est manquante.
        """
        self.sandbox = sandbox

        # La logique de chargement de la configuration reste la même, elle est excellente
        self.identifiant_client_piste = identifiant_client_piste or os.getenv(
            "PISTE_CLIENT_ID"
        )
        if not self.identifiant_client_piste:
            raise ErreurConfiguration("PISTE_CLIENT_ID")

        self.secret_client_piste = secret_client_piste or os.getenv(
            "PISTE_CLIENT_SECRET"
        )
        if not self.secret_client_piste:
            raise ErreurConfiguration("PISTE_CLIENT_SECRET")

        self.identifiant_cpro = identifiant_cpro or os.getenv("CHORUS_PRO_LOGIN")
        if not self.identifiant_cpro:
            raise ErreurConfiguration("CHORUS_PRO_LOGIN")

        self.mot_de_passe_cpro = mot_de_passe_cpro or os.getenv("CHORUS_PRO_PASSWORD")
        if not self.mot_de_passe_cpro:
            raise ErreurConfiguration("CHORUS_PRO_PASSWORD")

        self._client = None
        self._token = None

    def _initialiser_session(self):
        """
        Méthode privée qui gère l'authentification et la création du _client HTTP.
        N'est appelée qu'une seule fois, lors du premier besoin.
        """
        if self._client is None:
            self._token = self._obtenir_jeton()

            url_base = self.URL_API_PROD if not self.sandbox else self.URL_API_SANDBOX

            self._client = HttpClient(base_url=url_base, api_key=self._token)
            self._client.headers["cpro-account"] = self._creer_compte_cpro_base64()

    def _obtenir_jeton(self):
        """Obtient un jeton d'accès OAuth2 auprès de l'API PISTE."""
        url = self.URL_OAUTH_PROD if not self.sandbox else self.URL_OAUTH_SANDBOX
        headers = {"content-type": "application/x-www-form-urlencoded"}
        donnees = {
            "grant_type": "client_credentials",
            "client_id": self.identifiant_client_piste,
            "client_secret": self.secret_client_piste,
            "scope": "openid",
        }
        reponse = requests.post(url, headers=headers, data=donnees, verify=True)
        reponse.raise_for_status()
        return reponse.json()["access_token"]

    def _creer_compte_cpro_base64(self):
        """
        Crée l'en-tête d'authentification Chorus Pro encodé en base64.

        L'identifiant est sous la forme 'login:password'.
        """
        identifiants_bruts = f"{self.identifiant_cpro}:{self.mot_de_passe_cpro}"
        return base64.b64encode(bytes(identifiants_bruts, "utf-8")).decode("utf-8")

    def envoyer_facture(self, facture: dict) -> dict:
        """Soumet une facture à Chorus Pro.

        Correspond à l'opération `/factures/v1/soumettre`.

        :param facture: Un dictionnaire représentant la facture à soumettre.
        :return: La réponse JSON de l'API.
        """
        self._initialiser_session()
        response = self._client.post("/factures/v1/soumettre", json=facture)
        return response.json()

    def obtenir_statut_facture(self, facture_id: str) -> dict:
        """Consulte le statut d'une facture sur Chorus Pro.

        Correspond à l'opération `/factures/v1/consulter/fournisseur`.

        :param facture_id: L'identifiant technique de la facture sur Chorus Pro.
        :return: La réponse JSON de l'API contenant le statut.
        """
        self._initialiser_session()
        response = self._client.post(
            "/factures/v1/consulter/fournisseur",
            json={"identifiantFactureCPP": facture_id},
        )
        return response.json()

    def ajouter_fichier_dans_systeme(
        self, fichier: str = "", nom: str = "", type_mime: str = "", extension: str = ""
    ):
        """Ajoute une pièce jointe au compte utilisateur courant.

        La pièce jointe ne doit pas dépasser 10Mo.
        Correspond à l'opération `/transverses/v1/ajouter/fichier`.

        :param fichier: Le contenu du fichier encodé en base64.
        :param nom: Le nom du fichier (max 50 caractères).
        :param type_mime: Le type MIME du fichier.
        :param extension: L'extension du fichier (ex: "PDF", "JPG").
        :return: La réponse JSON de l'API, contenant l'identifiant de la pièce jointe.
        """
        self._initialiser_session()
        response = self._client.post(
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
        """Consulte les informations détaillées d'une structure.

        :param id_structure: L'identifiant technique Chorus Pro de la structure.
        :return: La réponse JSON de l'API.
        """
        self._initialiser_session()
        reponse = self._client.post(
            "/structures/v1/consulter",
            json={"codeLangue": "fr", "idStructureCPP": id_structure},
        )
        return reponse.json()

    def rechercher_organisation_siren(self, payload) -> dict:
        """Recherche les données d'une organisation via son SIREN.

        NOTE: L'endpoint semble inactif ou déprécié.
        Voir: https://communaute.chorus-pro.gouv.fr/documentation/base-sirene-des-entreprises-et-de-leurs-etablissements/

        :param payload: Le dictionnaire de critères de recherche.
        :return: La réponse JSON de l'API.
        """
        self._initialiser_session()
        reponse = self._client.post("/organisations/v1/siren/recherche", json=payload)
        return reponse.json()

    def rechercher_structure_via_organisation(self, payload) -> dict:
        """Recherche des données sur les structures via l'organisation.

        Voir: https://communaute.chorus-pro.gouv.fr/documentation/base-sirene-des-entreprises-et-de-leurs-etablissements/

        :param payload: Le dictionnaire de critères de recherche.
        :return: La réponse JSON de l'API.
        """
        self._initialiser_session()
        reponse = self._client.post(
            "/organisations/v1/structures/recherche", json=payload
        )
        return reponse.json()

    def rechercher_structure(self, payload) -> dict:
        """
        La méthode rechercherStructure permet à un gestionnaire de rechercher des structures.
        Voir: https://communaute.chorus-pro.gouv.fr/documentation/guide-dutilisation-de-lannuaire-des-structures-publiques-dans-chorus-pro/

        :param payload: Le dictionnaire de critères de recherche.
        :return: La réponse JSON de l'API.
        """
        self._initialiser_session()
        reponse = self._client.post("/structures/v1/rechercher", json=payload)
        return reponse.json()

    def rechercher_services_structure(self, id_structure: int) -> dict:
        """Recherche les services associés à une structure.

        :param id_structure: L'identifiant technique Chorus Pro de la structure.
        :return: La réponse JSON de l'API listant les services.
        """
        self._initialiser_session()
        reponse = self._client.post(
            "/structures/v1/rechercher/services", json={"idStructure": id_structure}
        )
        return reponse.json()

    def consulter_service_structure(self, id_structure: int, id_service: int) -> dict:
        """Consulte les informations détaillées d'un service.

        :param id_structure: L'identifiant technique Chorus Pro de la structure.
        :param id_service: L'identifiant technique Chorus Pro du service.
        :return: La réponse JSON de l'API.
        """
        self._initialiser_session()
        reponse = self._client.post(
            "/structures/v1/consulter/service",
            json={"idStructure": id_structure, "idService": id_service},
        )
        return reponse.json()

    def obtenir_identifiant_cpro_depuis_siret(
        self, siret: str, type_identifiant: str = "SIRET"
    ) -> int:
        """Recherche une structure par son SIRET et retourne son ID Chorus Pro.

        Cette méthode est un raccourci pour `rechercher_structure` qui ne retourne
        que l'ID si une seule structure correspond.

        :param siret: Le numéro de SIRET de la structure.
        :param type_identifiant: Le type d'identifiant (par défaut "SIRET").
        :return: L'identifiant Chorus Pro (`idStructureCPP`) si une seule structure est trouvée, sinon 0.
        """
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
