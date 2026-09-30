import json
from pathlib import Path
from blog.modelos import Blog, Post

RUTA_POSTS = Path(__file__).resolve().parent.parent / "posts.json"


def cargar_posts(ruta=RUTA_POSTS):
    ruta = Path(ruta)
    try:
        contenido = ruta.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [], ["No existe posts.json; se inicia un blog vacío."]
    except (OSError, UnicodeError) as error:
        return [], [f"No se pudo leer el archivo: {error}"]
    if not contenido.strip():
        return [], ["El archivo está vacío; se inicia un blog vacío."]
    try:
        datos = json.loads(contenido)
    except json.JSONDecodeError as error:
        return [], [f"JSON inválido en línea {error.lineno}; no se sobrescribe automáticamente."]
    if not isinstance(datos, list):
        return [], ["El JSON debe contener una lista de posts."]
    blog = Blog()
    avisos = []
    for numero, registro in enumerate(datos, 1):
        try:
            blog.agregar(Post.desde_diccionario(registro))
        except (ValueError, TypeError) as error:
            avisos.append(f"Registro {numero} omitido: {error}")
    return blog.listar(), avisos


def guardar_posts(posts, ruta=RUTA_POSTS):
    """Valida antes de guardar; conserva copia del JSON previo."""
    ruta = Path(ruta)
    temporal = ruta.with_suffix(".tmp")
    try:
        blog = Blog(posts)
        if any(not valido for _, valido, _ in blog.validar()):
            return False, "Hay posts inválidos; no se modificó el archivo."
        texto = json.dumps([p.a_diccionario() for p in posts], ensure_ascii=False, indent=2)
        if ruta.exists():
            ruta.with_suffix(".json.bak").write_bytes(ruta.read_bytes())
        temporal.write_text(texto + "\n", encoding="utf-8")
        temporal.replace(ruta)
        return True, f"Se guardaron {len(posts)} posts en {ruta.name}."
    except (OSError, ValueError, TypeError, AttributeError) as error:
        return False, f"No se pudo guardar: {error}"
