import base64
import mimetypes
import os


def file_to_base64(file_path) -> str:
    """Lit un fichier et retourne son contenu encodé en base64.

    :param file_path: Le chemin vers le fichier à encoder.
    :return: Une chaîne de caractères contenant les données en base64.
    """
    with open(file_path, "rb") as file:
        # Lire le contenu du fichier en mode binaire
        file_content = file.read()
        # Convertir le contenu en base64
        base64_content = base64.b64encode(file_content)
        # Convertir les bytes base64 en chaîne de caractères
        return base64_content.decode("utf-8")


def guess_mime_type(file_path):
    """Devine le type MIME d'un fichier à partir de son nom/extension.

    :param file_path: Le chemin vers le fichier.
    :return: Le type MIME deviné (ex: 'application/pdf').
    """
    # Devine le type MIME à partir du chemin du fichier
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def get_file_extension(file_path):
    """Extrait l'extension d'un fichier en majuscules, sans le point.

    :param file_path: Le chemin vers le fichier.
    :return: L'extension en majuscules (ex: 'PDF').
    """
    # Utilise os.path.splitext pour séparer le nom de fichier de son extension
    _, extension = os.path.splitext(file_path)
    # Retourne l'extension (y compris le point)
    return extension.replace(".", "").upper()


def get_absolute_path(relative_path):
    """Convertit un chemin relatif en chemin absolu par rapport au répertoire courant.

    Attention: Le résultat dépend du répertoire de travail actuel.

    :param relative_path: Le chemin relatif.
    :return: Le chemin absolu correspondant.
    """
