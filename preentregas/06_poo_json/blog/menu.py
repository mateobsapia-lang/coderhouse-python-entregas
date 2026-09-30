from blog.modelos import Autor, Post, ESTADOS


def mostrar_menu():
    print("\n1. Ver todos los posts\n2. Buscar por título\n3. Filtrar por tag\n4. Crear nuevo post\n5. Validar posts\n6. Guardar posts en JSON\n7. Salir")
    try:
        return int(input("Elegí una opción: "))
    except ValueError:
        return None


def pedir_texto(mensaje):
    return input(mensaje).strip()


def mostrar_posts(posts):
    if not posts:
        print("No se encontraron posts.")
    for post in posts:
        print(f"{post.id}. {post.titulo} | Autor: {post.autor.nombre} | Estado: {post.estado}")


def crear_post(blog):
    titulo = pedir_texto("Título: ")
    contenido = pedir_texto("Contenido: ")
    nombre = pedir_texto("Autor: ")
    etiquetas = pedir_texto("Tags separados por coma: ")
    estado = pedir_texto("Estado (borrador/publicado/archivado): ").lower()
    try:
        autor = Autor(nombre)
        tags = [t.strip() for t in etiquetas.split(",") if t.strip()]
        post = Post(blog.siguiente_id(), titulo, contenido, autor, tags, estado)
        blog.agregar(post)
        print("Post creado. Elegí 6 para guardarlo en JSON.")
    except ValueError as error:
        print(f"No se creó el post: {error}")
