import pytest
import base64
from unittest.mock import patch, MagicMock

from facture_electronique.api.chorus_pro import ChorusProAPI
from facture_electronique.exceptions import ErreurConfiguration
from facture_electronique.utils.http_client import HttpClient

# --- Constantes pour les tests ---
ID_CLIENT_PISTE_FICTIF = "id_piste_fictif_123"
SECRET_CLIENT_PISTE_FICTIF = "secret_piste_fictif_456"
LOGIN_CPRO_FICTIF = "login_cpro_fictif"
MOT_DE_PASSE_CPRO_FICTIF = "mdp_cpro_fictif"
JETON_ACCES_FICTIF = "un_super_jeton_jwt"

# Encodage Base64 attendu pour les identifiants fictifs
CPRO_ACCOUNT_FICTIF_ENCODE = base64.b64encode(
    bytes(f"{LOGIN_CPRO_FICTIF}:{MOT_DE_PASSE_CPRO_FICTIF}", "utf-8")
).decode("utf-8")


@pytest.fixture
def mock_variables_env(monkeypatch):
    """Fixture pytest pour simuler la présence des variables d'environnement."""
    monkeypatch.setenv("PISTE_CLIENT_ID", ID_CLIENT_PISTE_FICTIF)
    monkeypatch.setenv("PISTE_CLIENT_SECRET", SECRET_CLIENT_PISTE_FICTIF)
    monkeypatch.setenv("CHORUS_PRO_LOGIN", LOGIN_CPRO_FICTIF)
    monkeypatch.setenv("CHORUS_PRO_PASSWORD", MOT_DE_PASSE_CPRO_FICTIF)


class TestConfigurationChorusProAPI:
    """Groupe de tests dédiés à la configuration et l'initialisation de la classe."""

    def test_initialisation_reussie_avec_arguments(self):
        """Vérifie que la classe s'initialise correctement avec des arguments directs."""
        api = ChorusProAPI(
            identifiant_client_piste=ID_CLIENT_PISTE_FICTIF,
            secret_client_piste=SECRET_CLIENT_PISTE_FICTIF,
            identifiant_cpro=LOGIN_CPRO_FICTIF,
            mot_de_passe_cpro=MOT_DE_PASSE_CPRO_FICTIF,
        )
        assert api.identifiant_client_piste == ID_CLIENT_PISTE_FICTIF
        assert api.identifiant_cpro == LOGIN_CPRO_FICTIF
        assert api._client is None  # Vérifie l'initialisation paresseuse

    def test_initialisation_reussie_avec_variables_env(self, mock_variables_env):
        """Vérifie que la classe s'initialise correctement depuis les variables d'environnement."""
        api = ChorusProAPI()
        assert api.identifiant_client_piste == ID_CLIENT_PISTE_FICTIF
        assert api.secret_client_piste == SECRET_CLIENT_PISTE_FICTIF
        assert api.identifiant_cpro == LOGIN_CPRO_FICTIF
        assert api.mot_de_passe_cpro == MOT_DE_PASSE_CPRO_FICTIF

    def test_priorite_des_arguments_sur_les_variables_env(self, mock_variables_env):
        """Vérifie que les arguments fournis au constructeur ont la priorité."""
        id_piste_arg = "id_piste_argument"
        api = ChorusProAPI(identifiant_client_piste=id_piste_arg)
        # L'ID doit être celui de l'argument, pas celui de la variable d'env
        assert api.identifiant_client_piste == id_piste_arg
        # Les autres doivent provenir de l'environnement
        assert api.secret_client_piste == SECRET_CLIENT_PISTE_FICTIF

    @pytest.mark.parametrize(
        "variable_manquante",
        [
            "PISTE_CLIENT_ID",
            "PISTE_CLIENT_SECRET",
            "CHORUS_PRO_LOGIN",
            "CHORUS_PRO_PASSWORD",
        ],
    )
    def test_echec_initialisation_si_variable_manquante(
        self, monkeypatch, variable_manquante
    ):
        """Vérifie qu'une ErreurConfiguration est levée si une variable manque."""
        # On met toutes les variables sauf celle à tester
        variables = {
            "PISTE_CLIENT_ID": ID_CLIENT_PISTE_FICTIF,
            "PISTE_CLIENT_SECRET": SECRET_CLIENT_PISTE_FICTIF,
            "CHORUS_PRO_LOGIN": LOGIN_CPRO_FICTIF,
            "CHORUS_PRO_PASSWORD": MOT_DE_PASSE_CPRO_FICTIF,
        }
        del variables[variable_manquante]
        for nom, valeur in variables.items():
            monkeypatch.setenv(nom, valeur)

        with pytest.raises(ErreurConfiguration) as excinfo:
            ChorusProAPI()

        assert variable_manquante in str(excinfo.value)


class TestAppelsAPIChorusPro:
    """Groupe de tests pour les méthodes publiques qui interagissent avec l'API."""

    @patch("facture_electronique.api.chorus_pro.requests.post")
    def test_initialisation_paresseuse_de_la_session(
        self, mock_post, mock_variables_env
    ):
        """
        Vérifie que l'appel d'authentification n'est fait qu'une seule fois.
        """
        # Simuler une réponse réussie du serveur d'authentification
        mock_reponse_auth = MagicMock()
        mock_reponse_auth.json.return_value = {"access_token": JETON_ACCES_FICTIF}
        mock_post.return_value = mock_reponse_auth

        api = ChorusProAPI()

        # On patch aussi le client interne pour ne pas dépendre de son implémentation
        with patch.object(HttpClient, "post") as mock_client_post:
            # Premier appel à une méthode publique
            api.envoyer_facture({"donnees": "facture1"})

            # Vérifier que l'authentification a bien eu lieu
            mock_post.assert_called_once()

            # Second appel à une autre méthode publique
            api.obtenir_statut_facture("id_facture_123")

            # L'authentification ne doit PAS avoir été rappelée
            mock_post.assert_called_once()
            assert mock_client_post.call_count == 2

    @patch("facture_electronique.api.chorus_pro.requests.post")
    @patch.object(HttpClient, "post")
    def test_envoyer_facture(
        self, mock_client_post, mock_auth_post, mock_variables_env
    ):
        """
        Vérifie la méthode envoyer_facture de bout en bout (avec mocks).
        """
        # 1. Configuration des Mocks
        mock_reponse_auth = MagicMock()
        mock_reponse_auth.json.return_value = {"access_token": JETON_ACCES_FICTIF}
        mock_auth_post.return_value = mock_reponse_auth

        reponse_api_attendue = {"statut": "succes", "id": 42}
        # Important : on doit simuler la méthode json() sur la *valeur de retour* du post mocké
        mock_client_post.return_value.json.return_value = reponse_api_attendue

        # 2. Appel de la méthode
        api = ChorusProAPI(sandbox=True)
        donnees_facture = {"numero": "FACT-001"}
        resultat = api.envoyer_facture(donnees_facture)

        # 3. Assertions
        # a) Vérifier l'appel d'authentification
        mock_auth_post.assert_called_once_with(
            api.URL_OAUTH_SANDBOX,
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": ID_CLIENT_PISTE_FICTIF,
                "client_secret": SECRET_CLIENT_PISTE_FICTIF,
                "scope": "openid",
            },
            verify=True,
        )

        # b) Vérifier que le client HttpClient a été correctement configuré
        assert api._client.base_url == api.URL_API_SANDBOX

        # Le comportement important n'est pas de stocker la clé, mais de l'utiliser
        # pour configurer le header d'autorisation. C'est ce que nous vérifions.
        en_tete_auth_attendu = f"Bearer {JETON_ACCES_FICTIF}"
        assert api._client.headers["Authorization"] == en_tete_auth_attendu
        assert api._client.headers["cpro-account"] == CPRO_ACCOUNT_FICTIF_ENCODE

        # c) Vérifier l'appel à l'API Chorus Pro
        mock_client_post.assert_called_once_with(
            "/factures/v1/soumettre", json=donnees_facture
        )

        # d) Vérifier que le résultat est correct
        assert resultat == reponse_api_attendue

    @patch("facture_electronique.api.chorus_pro.ChorusProAPI._initialiser_session")
    def test_obtenir_statut_facture_appelle_correctement_le_client(
        self, mock_init, mock_variables_env
    ):
        """Vérifie que obtenir_statut_facture appelle le bon endpoint avec le bon payload."""
        api = ChorusProAPI()
        api._client = MagicMock()  # On assigne un mock pour le client

        id_facture = "CPP-FACT-987"
        api.obtenir_statut_facture(id_facture)

        # Vérifier que l'initialisation a été appelée
        mock_init.assert_called_once()

        # Vérifier que la méthode post du client a été appelée avec les bons arguments
        api._client.post.assert_called_once_with(
            "/factures/v1/consulter/fournisseur",
            json={"identifiantFactureCPP": id_facture},
        )
