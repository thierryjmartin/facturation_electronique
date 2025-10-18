import subprocess
import sys
import os


def test_exemple_principal_runs_without_error():
    """Vérifie que le script principal d'exemple s'exécute sans erreur."""
    script_path = "facture_electronique/exemples/exemple.py"

    # Utilise sys.executable pour garantir l'utilisation du même interpréteur Python
    # que celui qui exécute pytest.
    # On ajoute les identifiants fictifs à l'environnement pour ce sous-processus.
    env = os.environ.copy()
    env["PISTE_CLIENT_ID"] = "dummy"
    env["PISTE_CLIENT_SECRET"] = "dummy"
    env["CHORUS_PRO_LOGIN"] = "dummy"
    env["CHORUS_PRO_PASSWORD"] = "dummy"

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        env=env,
        check=False,  # On ne veut pas que subprocess lève une erreur, on la gère nous-mêmes
    )

    # Affiche la sortie d'erreur du script si le test échoue pour faciliter le débogage
    assert (
        result.returncode == 0
    ), f"Le script {script_path} a échoué avec le code {result.returncode}.\nErreur:\n{result.stderr}"


def test_exemple_decoupe_runs_without_error():
    """Vérifie que le script découpé d'exemple s'exécute sans erreur."""
    script_path = "facture_electronique/exemples/exemple_decoupe.py"

    env = os.environ.copy()
    env["PISTE_CLIENT_ID"] = "dummy"
    env["PISTE_CLIENT_SECRET"] = "dummy"
    env["CHORUS_PRO_LOGIN"] = "dummy"
    env["CHORUS_PRO_PASSWORD"] = "dummy"

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert (
        result.returncode == 0
    ), f"Le script {script_path} a échoué avec le code {result.returncode}.\nErreur:\n{result.stderr}"
