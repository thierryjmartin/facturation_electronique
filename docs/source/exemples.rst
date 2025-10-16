Exemples d'utilisation
========================

.. _exemples:

Voici quelques exemples d'utilisation de la bibliothèque.

Exemple complet
---------------

.. literalinclude:: ../../facture_electronique/exemples/exemple.py
   :language: python
   :linenos:

Exemple découpé
----------------

.. literalinclude:: ../../facture_electronique/exemples/exemple_decoupe.py
   :language: python
   :linenos:

Test de code
------------

.. testcode::

   from decimal import Decimal
   assert Decimal('1.1') + Decimal('2.2') == Decimal('3.3')
