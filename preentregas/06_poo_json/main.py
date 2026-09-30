from blog.modelos import Blog
from blog.datos import cargar_posts, guardar_posts
from blog.menu import mostrar_menu, pedir_texto, mostrar_posts, crear_post


def main():
    posts, avisos = cargar_posts()
    for aviso in avisos:
        print(aviso)
    blog = Blog(posts)
    while True:
        opcion = mostrar_menu()
        if opcion == 1:
            mostrar_posts(blog.listar())
        elif opcion == 2:
            termino = pedir_texto("Título a buscar: ")
            if not termino:
                print("Ingresá un término de búsqueda.")
            else:
                mostrar_posts(blog.buscar_por_titulo(termino))
        elif opcion == 3:
            tag = pedir_texto("Tag a filtrar: ")
            if not tag:
                print("Ingresá un tag.")
            else:
                mostrar_posts(blog.filtrar_por_tag(tag))
        elif opcion == 4:
            crear_post(blog)
        elif opcion == 5:
            for identificador, valido, mensaje in blog.validar():
                print(f"Post {identificador}: {mensaje}")
        elif opcion == 6:
            exito, mensaje = guardar_posts(blog.listar())
            print(mensaje)
        elif opcion == 7:
            print("¡Hasta luego! El guardado es manual con la opción 6.")
            break
        else:
            print("Opción inválida, intenta de nuevo")


if __name__ == "__main__":
    main()
