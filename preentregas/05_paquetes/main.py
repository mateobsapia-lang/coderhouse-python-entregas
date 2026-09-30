from blog.datos import posts
from blog.menu import mostrar_menu, pedir_texto
from blog.operaciones import listar_posts, buscar_por_titulo, filtrar_por_tag
from blog.validaciones import validar_post, errores_post

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
