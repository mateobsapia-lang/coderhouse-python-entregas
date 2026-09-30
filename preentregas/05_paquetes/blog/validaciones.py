from blog.datos import estados_post

def errores_post(post):
    """Devuelve errores de estructura sin acceder a claves inseguras."""
    if not isinstance(post, dict):
        return ["el post debe ser un diccionario"]
    errores = []
    obligatorias = {"id", "titulo", "contenido", "autor", "tags", "estado"}
    faltantes = obligatorias - post.keys()
    if faltantes:
        errores.append("faltan claves: " + ", ".join(sorted(faltantes)))
    if type(post.get("id")) is not int or post.get("id", 0) <= 0:
        errores.append("id debe ser un entero positivo")
    for campo in ("titulo", "contenido"):
        if not isinstance(post.get(campo), str) or not post.get(campo, "").strip():
            errores.append(campo + " debe ser texto no vacío")
    autor = post.get("autor")
    if not isinstance(autor, dict):
        errores.append("autor debe ser un diccionario")
    elif not isinstance(autor.get("nombre"), str) or not autor.get("nombre", "").strip():
        errores.append("autor debe tener nombre no vacío")
    tags = post.get("tags")
    if not isinstance(tags, list) or any(not isinstance(t, str) or not t.strip() for t in tags):
        errores.append("tags debe ser una lista de textos no vacíos")
    if post.get("estado") not in estados_post:
        errores.append("estado no permitido")
    return errores


def validar_post(post):
    return not errores_post(post)
