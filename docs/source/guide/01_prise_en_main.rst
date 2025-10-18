.. _guide_prise_en_main:

Prise en main
=============

Installation
------------

Assurez-vous d'avoir installé la bibliothèque. Si vous travaillez depuis le code source, vous pouvez l'installer en mode éditable :

.. code-block:: bash

   pip install -e .


Initialisation de l'API
-----------------------

Le point d'entrée principal pour interagir avec l'API Chorus Pro est la classe `ChorusProAPI`.

.. testcode::

   from facture_electronique.api.chorus_pro import ChorusProAPI

   # Initialisation pour l'environnement de sandbox (recommandé pour les tests)
   client_chorus_sandbox = ChorusProAPI(sandbox=True)

   # Initialisation pour l'environnement de production
   client_chorus_production = ChorusProAPI(sandbox=False)

   assert client_chorus_sandbox.sandbox is True
   assert client_chorus_production.sandbox is False

Par défaut, le client est initialisé en mode production (`sandbox=False`). Il est vivement recommandé d'utiliser l'environnement de test (sandbox) fourni par Chorus Pro pour tous vos développements.


Construire une Adresse Électronique
------------------------------------

Un concept clé de la facturation électronique est l'**adresse électronique**. C'est l'identifiant unique qui permet d'acheminer une facture à son destinataire. La norme (AFNOR XP Z12-014) définit des formats précis pour ces adresses, notamment pour les entreprises françaises, basées sur le SIREN.

Les formats peuvent être simples (juste un SIREN) ou complexes (ex: `SIREN_SIRET_CODEROUTAGE`).

Pour simplifier la création de ces adresses et éviter les erreurs, il est **fortement recommandé** d'utiliser le constructeur `ConstructeurAdresse`.

.. testcode::

    from facture_electronique.models import ConstructeurAdresse, AdresseElectronique, SchemeID

    # Cas 1: Adresse simple avec un SIREN (le plus courant)
    adresse_simple = ConstructeurAdresse(siren="123456789").construire()
    print(adresse_simple.identifiant)

    # Cas 2: Adresse pour un établissement spécifique via un SIRET
    adresse_etablissement = (
        ConstructeurAdresse(siren="123456789")
        .avec_siret("12345678901234")
        .construire()
    )
    print(adresse_etablissement.identifiant)

    # Cas 3: Adresse complexe avec un code de routage (secteur public)
    adresse_service = (
        ConstructeurAdresse(siren="123456789")
        .avec_siret("12345678901234")
        .avec_code_routage("SERVICE_COMPTA")
        .construire()
    )
    print(adresse_service.identifiant)

.. testoutput::

    123456789
    123456789_12345678901234
    123456789_12345678901234_SERVICE_COMPTA


.. note::

   Bien que l'utilisation du `ConstructeurAdresse` soit recommandée, il est toujours possible de créer une `AdresseElectronique` manuellement si vous avez déjà l'identifiant complet. Ceci est utile pour les schémas non-français ou si l'identifiant est stocké pré-formaté.

   .. code-block:: python

      # Exemple pour un identifiant GLN
      adresse_gln = AdresseElectronique(identifiant="3354650000000", scheme_id=SchemeID.GLN)

      # Exemple pour un SIREN français pré-formaté
      adresse_preformatee = AdresseElectronique(identifiant="123456789_MONSUFFIXE", scheme_id=SchemeID.FR_SIREN)
