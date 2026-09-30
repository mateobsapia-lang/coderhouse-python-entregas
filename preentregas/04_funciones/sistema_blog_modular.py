# Datos de muestra de un blog sobre aprendizaje de programación.
perfil_autor = {
    "nombre": "Mateo Sapia",
    "bio": "Aprendiendo Python y documentando cada paso del proyecto.",
    "especialidad": "Desarrollo Python",
    "redes_sociales": ["GitHub", "LinkedIn"],
}
estados_post = ("borrador", "publicado", "archivado")
etiquetas_blog = {"Python", "Django", "Git", "Python"}  # Sin duplicados.
posts = [
    {"id": 1, "titulo": "Mi primer post en Python",
     "contenido": "Variables y colecciones permiten representar los datos del blog.",
     "autor": perfil_autor, "categoria": "Python",
     "tags": ["Python", "Inicio"], "estado": estados_post[1]},
    {"id": 2, "titulo": "Organizar un proyecto con Git",
     "contenido": "Los commits descriptivos documentan la evolución del código.",
     "autor": perfil_autor, "categoria": "Herramientas",
     "tags": ["Git", "Python"], "estado": estados_post[0]},
    {"id": 3, "titulo": "Primeros pasos con Django",
     "contenido": "Un proyecto Django reúne la configuración de sus aplicaciones.",
     "autor": perfil_autor, "categoria": "Desarrollo web",
     "tags": ["Django", "Web"], "estado": estados_post[2]},
]

# Registro incompleto intencional: prueba de validación.
posts.append({"id": 4, "titulo": "", "autor": perfil_autor, "tags": "Python", "estado": "desconocido"})

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

def mostrar_menu():
    print("\n1. Ver todos los posts\n2. Buscar por título\n3. Filtrar por tag\n4. Validar posts\n5. Salir")
    try:
        return int(input("Elegí una opción: "))
    except ValueError:
        print("La opción debe ser un número.")
        return None


def pedir_texto(mensaje):
    return input(mensaje).strip()

if __name__ == "__main__":
    while True:
        opcion = mostrar_menu()
        if opcion == 1:
            listar_posts(posts)
        elif opcion == 2:
            listar_posts(buscar_por_titulo(posts, pedir_texto("Título a buscar: ")))
        elif opcion == 3:
            listar_posts(filtrar_por_tag(posts, pedir_texto("Tag a filtrar: ")))
        elif opcion == 4:
            for indice, post in enumerate(posts, 1):
                if validar_post(post):
                    print(f"Post {indice}: válido")
                else:
                    print(f"Post {indice}: inválido - {'; '.join(errores_post(post))}")
        elif opcion == 5:
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo")
