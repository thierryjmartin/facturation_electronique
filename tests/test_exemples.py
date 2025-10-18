# facture_electronique/tests/test_exemples.py

import os
import subprocess
import sys
from pathlib import Path

import pytest

# On définit le chemin de base vers le répertoire des exemples de manière robuste.
# __file__ -> chemin de ce fichier de test
# .parent -> répertoire 'tests'
# .parent -> répertoire 'facture_electronique'
CHEMIN_BASE_EXEMPLES = Path(__file__).parent.parent / "facture_electronique" / "exemples"

# Liste des scripts à tester. Facile à maintenir et à étendre.
SCRIPTS_A_TESTER = [
    "exemple.py",
    "exemple_decoupe.py",
]


@pytest.mark.parametrize("nom_script", SCRIPTS_A_TESTER)
def test_execution_exemple_sans_erreur(nom_script):
    """
    Vérifie qu'un script d'exemple s'exécute sans erreur.
    Ce test est paramétré pour s'exécuter pour chaque script dans SCRIPTS_A_TESTER.
    """
    chemin_script = CHEMIN_BASE_EXEMPLES / nom_script

    # Vérifie que le fichier script existe avant de tenter de l'exécuter
    assert chemin_script.exists(), f"Le fichier script {chemin_script} n'a pas été trouvé."

    # Création d'un environnement isolé pour le sous-processus
    env = os.environ.copy()
    env["PISTE_CLIENT_ID"] = "dummy"
    env["PISTE_CLIENT_SECRET"] = "dummy"
    env["CHORUS_PRO_LOGIN"] = "dummy"
    env["CHORUS_PRO_PASSWORD"] = "dummy"

    resultat = subprocess.run(
        [
            sys.executable,
            str(chemin_script),
        ],  # str() est nécessaire car subprocess attend des chaînes
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    message_erreur = "Le script {script} a échoué avec le code {code}.\nErreur:\n{stderr}".format(
        script=chemin_script,
        code=resultat.returncode,
        stderr=resultat.stderr,
    )

    assert resultat.returncode == 0, message_erreur
