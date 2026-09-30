from blog.validaciones import errores_post, validar_post

def listar_posts(lista):
    if not lista:
        print("No se encontraron posts.")
    for posicion, post in enumerate(lista, 1):
        errores = errores_post(post)
        if errores:
            print(f"Registro {posicion} omitido: {'; '.join(errores)}")
            continue
        print(f"{post['titulo']} | Autor: {post['autor']['nombre']} | Estado: {post['estado']}")


def buscar_por_titulo(lista, termino):
    termino = termino.strip().lower()
    if not termino:
        print("Ingresá un término de búsqueda.")
        return []
    return [post for post in lista if validar_post(post) and termino in post['titulo'].lower()]


def filtrar_por_tag(lista, tag):
    tag = tag.strip().lower()
    if not tag:
        print("Ingresá un tag.")
        return []
    return [post for post in lista if validar_post(post)
            and tag in [valor.lower() for valor in post['tags']]]
