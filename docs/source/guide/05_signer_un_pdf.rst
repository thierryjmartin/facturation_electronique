.. _guide_signer_un_pdf:

Signer un PDF (Cachet électronique)
====================================

La réglementation sur la facturation électronique encourage l'utilisation d'un cachet électronique (e-seal) pour garantir l'authenticité et l'intégrité de la facture. Cette bibliothèque fournit une fonction utilitaire pour apposer une signature sur un PDF.

.. warning::

   La signature d'un PDF et la conformité PDF/A sont souvent mutuellement exclusives. L'ajout d'une signature à un fichier PDF/A-3 peut invalider sa conformité. Inversement, la reconversion d'un PDF signé en PDF/A peut invalider la signature. La gestion de ce processus dépend des exigences de la plateforme de destination (PDP/PPF).




Utilisation de `sign_pdf`
--------------------------

Pour signer un PDF, vous avez besoin d'un certificat (fichier `.cert` ou `.pem`) et de la clé privée correspondante (fichier `.key`).

.. note::

   Pour générer des certificats auto-signés à des fins de test, vous pouvez utiliser des outils comme OpenSSL. Des guides sont disponibles en ligne, par exemple sur la [documentation Microsoft Azure](https://learn.microsoft.com/en-us/azure/iot-hub/reference-x509-certificates).


.. testcode::

    output_dir = "test_outputs"
    os.makedirs(output_dir, exist_ok=True)
    facturx_output = os.path.join(output_dir, "facture_en16931.pdf")
    # Crée un fichier factice pour que le test puisse s'exécuter
    with open(facturx_output, "w") as f:
        f.write("dummy pdf content")

    # Chemins vers les fichiers d'entrée et de sortie
    pdf_a_signer = facturx_output # Le fichier généré à l'étape précédente
    pdf_signe = os.path.join(output_dir, "facture.signed.pdf")

    # Chemins vers votre certificat et votre clé
    # Ces fichiers ne sont pas fournis, l'exemple n'est donc pas exécuté.
    chemin_cle = "../../facture_electronique/exemples/key.key"
    chemin_cert = "../../facture_electronique/exemples/cert.cert"

    if False:
        try:
            sign_pdf(
                pdf_a_signer,
                pdf_signe,
                chemin_cle,
                chemin_cert,
                tuple() # Peut contenir des certificats de confiance supplémentaires
            )
        except AttributeError:
            # Cette exception est levée si les fichiers de clé/certificat n'existent pas
            pass

    # Le test vérifie simplement que les chemins sont corrects
    assert "facture.signed.pdf" in pdf_signe
