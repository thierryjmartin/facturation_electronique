def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    words = s.split()
    if len(words) == 0:
        return text
    return words[0] + "".join(word[0].upper() + word[1:] for word in words[1:])


def transform_dict_keys(d: dict, transform_func) -> dict:
    """
    Applique une fonction de transformation à toutes les clés d'un dictionnaire, même s'il est imbriqué.

    :param d: Le dictionnaire à transformer.
    :param transform_func: Fonction à appliquer aux clés.
    :return: Nouveau dictionnaire avec les clés transformées.
    """
    if isinstance(d, dict):
        return {
            transform_func(k): transform_dict_keys(v, transform_func)
            for k, v in d.items()
        }
    elif isinstance(d, list):
        return [transform_dict_keys(item, transform_func) for item in d]
    else:
        return d
