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

# El menú continúa hasta elegir la salida.
if __name__ == "__main__":
    while True:
        print("\n1. Ver todos los posts\n2. Buscar por título\n3. Filtrar por tag\n4. Salir")
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1":
            for post in posts:
                print(f"{post['titulo']} | Autor: {post['autor']['nombre']}")
        elif opcion == "2":
            termino = input("Título a buscar: ").strip().lower()
            encontrados = 0
            if not termino:
                print("Ingresá un término de búsqueda.")
                continue
            for post in posts:
                if termino in post["titulo"].lower():
                    print(f"{post['titulo']} | Autor: {post['autor']['nombre']}")
                    encontrados += 1
            if not encontrados:
                print("No se encontraron posts.")
        elif opcion == "3":
            tag = input("Tag a filtrar: ").strip().lower()
            encontrados = 0
            if not tag:
                print("Ingresá un tag.")
                continue
            for post in posts:
                if tag in [etiqueta.lower() for etiqueta in post["tags"]]:
                    print(f"{post['titulo']} | Autor: {post['autor']['nombre']}")
                    encontrados += 1
            if not encontrados:
                print("No se encontraron posts.")
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo")
