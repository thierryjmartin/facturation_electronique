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
