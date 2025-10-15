# Pour les dépendances de test (CI)
pip-compile --upgrade --strip-extras requirements.in -o requirements.txt

# Pour les dépendances de développement (local)
pip-compile --upgrade --strip-extras requirements-dev.in -o requirements-dev.txt