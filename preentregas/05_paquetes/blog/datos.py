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
