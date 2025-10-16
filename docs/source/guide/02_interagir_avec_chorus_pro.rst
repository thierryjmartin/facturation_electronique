.. _guide_interagir_avec_chorus_pro:

Interagir avec l'API Chorus Pro
================================

Chorus Pro fournit des API pour récupérer des informations sur les structures publiques (entreprises, services de l'État, etc.). Voici la cinématique nominale pour obtenir des informations détaillées.



.. note::

   Les extraits de code suivants sont conçus pour être exécutés dans un environnement où les identifiants de l'API Chorus Pro sont configurés. Pour les besoins de la documentation, les appels réels sont désactivés, mais le code présenté est fonctionnel.


Étape 1 : Rechercher une structure
----------------------------------

La première étape consiste à rechercher une structure à l'aide de critères comme son numéro de SIRET. L'API `rechercher_structure` renvoie une liste de structures correspondantes, avec leur identifiant technique Chorus Pro (`idStructureCPP`).

.. testcode::

    payload_recherche = {
        "parametres": {
            "nbResultatsParPage": 10,
            "pageResultatDemandee": 1,
        },
        "structure": {
            "identifiantStructure": "26073617692140",
            "typeIdentifiantStructure": "SIRET",
        },
    }

    # L'appel réel à l'API
    if False:
        reponse = c.rechercher_structure(payload_recherche)
        # Vous pouvez ensuite extraire l'idStructureCPP de la réponse
        # id_structure_cpp = reponse["listeStructures"][0]["idStructureCPP"]

    assert payload_recherche["structure"]["typeIdentifiantStructure"] == "SIRET"


Étape 2 : Consulter les détails d'une structure
------------------------------------------------

Avec l'`idStructureCPP` obtenu, vous pouvez appeler `consulter_structure` pour obtenir des informations détaillées, notamment si un numéro d'engagement ou un code service est obligatoire pour facturer cette structure.

.. testcode::

    # Remplacez par un ID obtenu à l'étape précédente
    id_structure_cpp = 26300989

    if False:
        details_structure = c.consulter_structure(id_structure_cpp)
        # details_structure contiendra les informations

    assert isinstance(id_structure_cpp, int)


Étape 3 : Rechercher les services d'une structure
--------------------------------------------------

Une structure peut être divisée en plusieurs services, chacun ayant son propre `code_service`. L'API `rechercher_services_structure` permet de lister les services actifs pour une structure donnée.

.. testcode::

    # Remplacez par un ID obtenu à l'étape 1
    id_structure_cpp = 26300989

    if False:
        services = c.rechercher_services_structure(id_structure_cpp)
        # services contiendra la liste des services

    assert isinstance(id_structure_cpp, int)


Étape 4 : Consulter les détails d'un service
----------------------------------------------

Enfin, avec l'`idService` obtenu, `consulter_service_structure` vous donnera les paramètres spécifiques à ce service.

.. testcode::

    id_structure_cpp = 26311042
    id_service = 10657669

    if False:
        details_service = c.consulter_service_structure(id_structure=id_structure_cpp, id_service=id_service)

    assert isinstance(id_service, int)
