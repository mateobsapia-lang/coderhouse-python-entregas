def mostrar_menu():
    print("\n1. Ver todos los posts\n2. Buscar por título\n3. Filtrar por tag\n4. Validar posts\n5. Salir")
    try:
        return int(input("Elegí una opción: "))
    except ValueError:
        print("La opción debe ser un número.")
        return None


def pedir_texto(mensaje):
    return input(mensaje).strip()
