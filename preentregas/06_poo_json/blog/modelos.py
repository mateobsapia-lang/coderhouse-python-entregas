from dataclasses import dataclass, field

ESTADOS = ("borrador", "publicado", "archivado")


def texto_requerido(valor, nombre):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{nombre} debe ser texto no vacío")
    return valor.strip()


@dataclass
class Autor:
    nombre: str
    bio: str = ""
    especialidad: str = ""
    redes_sociales: list = field(default_factory=list)

    def __post_init__(self):
        self.nombre = texto_requerido(self.nombre, "nombre")
        if not isinstance(self.bio, str) or not isinstance(self.especialidad, str):
            raise ValueError("bio y especialidad deben ser textos")
        if not isinstance(self.redes_sociales, list) or any(not isinstance(x, str) for x in self.redes_sociales):
            raise ValueError("redes_sociales debe ser una lista de textos")

    def a_diccionario(self):
        return {"nombre": self.nombre, "bio": self.bio,
                "especialidad": self.especialidad, "redes_sociales": list(self.redes_sociales)}

    @classmethod
    def desde_diccionario(cls, datos):
        if not isinstance(datos, dict):
            raise ValueError("autor debe ser un diccionario")
        return cls(datos.get("nombre"), datos.get("bio", ""),
                   datos.get("especialidad", ""), datos.get("redes_sociales", []))


@dataclass
class Post:
    id: int
    titulo: str
    contenido: str
    autor: Autor
    tags: list
    estado: str = "borrador"
    categoria: str = "General"

    def __post_init__(self):
        if type(self.id) is not int or self.id <= 0:
            raise ValueError("id debe ser un entero positivo")
        self.titulo = texto_requerido(self.titulo, "titulo")
        self.contenido = texto_requerido(self.contenido, "contenido")
        if not isinstance(self.autor, Autor):
            raise ValueError("autor debe ser una instancia de Autor")
        if not isinstance(self.tags, list) or any(not isinstance(t, str) or not t.strip() for t in self.tags):
            raise ValueError("tags debe ser una lista de textos no vacíos")
        self.tags = list(dict.fromkeys(t.strip() for t in self.tags))
        if self.estado not in ESTADOS:
            raise ValueError("estado no permitido")
        self.categoria = texto_requerido(self.categoria, "categoria")

    def a_diccionario(self):
        return {"id": self.id, "titulo": self.titulo, "contenido": self.contenido,
                "autor": self.autor.a_diccionario(), "tags": list(self.tags),
                "estado": self.estado, "categoria": self.categoria}

    @classmethod
    def desde_diccionario(cls, datos):
        if not isinstance(datos, dict):
            raise ValueError("post debe ser un diccionario")
        requeridas = {"id", "titulo", "contenido", "autor", "tags", "estado"}
        if not requeridas.issubset(datos):
            raise ValueError("post con claves faltantes: " + ", ".join(sorted(requeridas - datos.keys())))
        return cls(datos["id"], datos["titulo"], datos["contenido"],
                   Autor.desde_diccionario(datos["autor"]), datos["tags"],
                   datos["estado"], datos.get("categoria", "General"))


class Blog:
    def __init__(self, posts=None):
        self.posts = []
        for post in posts or []:
            self.agregar(post)

    def listar(self):
        return list(self.posts)

    def buscar_por_titulo(self, termino):
        termino = termino.strip().lower()
        return [p for p in self.posts if termino and termino in p.titulo.lower()]

    def filtrar_por_tag(self, tag):
        tag = tag.strip().lower()
        return [p for p in self.posts if tag and tag in [t.lower() for t in p.tags]]

    def agregar(self, post):
        if not isinstance(post, Post):
            raise ValueError("el blog solo admite objetos Post")
        if any(p.id == post.id for p in self.posts):
            raise ValueError("id de post duplicado")
        self.posts.append(post)

    def siguiente_id(self):
        return max((p.id for p in self.posts), default=0) + 1

    def validar(self):
        resultados = []
        ids = set()
        for post in self.posts:
            try:
                Post.desde_diccionario(post.a_diccionario())
                if post.id in ids:
                    raise ValueError("id duplicado")
                ids.add(post.id)
                resultados.append((post.id, True, "válido"))
            except (ValueError, TypeError, AttributeError) as error:
                resultados.append((getattr(post, "id", "?"), False, str(error)))
        return resultados
