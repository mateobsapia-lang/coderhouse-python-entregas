"""Pruebas funcionales: entradas reales, búsqueda, validación y persistencia."""
from pathlib import Path
import copy
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = Path(__file__).resolve().parents[1]
ETAPAS = RAIZ / 'preentregas'

def ejecutar(ruta, entrada=''):
    return subprocess.run([sys.executable, str(ruta)], input=entrada,
                          text=True, encoding='utf-8', capture_output=True,
                          env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}, timeout=15)

def importar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

class EtapasConsola(unittest.TestCase):
    def test_estructura_datos(self):
        m = importar('estructura', ETAPAS/'02_estructuras/estructura_blog.py')
        self.assertIsInstance(m.perfil_autor['redes_sociales'], list)
        self.assertEqual(m.estados_post, ('borrador','publicado','archivado'))
        self.assertEqual(len(m.etiquetas_blog), 3)
        self.assertGreaterEqual(len(m.posts), 3)
        self.assertTrue(all(p['autor'] is m.perfil_autor for p in m.posts))
        self.assertTrue(all({'id','titulo','contenido','autor','categoria','tags','estado'} <= p.keys() for p in m.posts))
        r = ejecutar(ETAPAS/'02_estructuras/estructura_blog.py')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Autor del segundo post: Mateo Sapia', r.stdout)

    def test_menu_interactivo(self):
        r = ejecutar(ETAPAS/'03_interactivo/sistema_blog.py', 'x\n1\n2\nPYTHON\n2\nzzzz\n3\nDJANGO\n3\n\n4\n')
        self.assertEqual(r.returncode, 0, r.stderr)
        for texto in ['Opción inválida, intenta de nuevo', 'Autor: Mateo Sapia', 'No se encontraron posts.', 'Ingresá un tag.', '¡Hasta luego!']:
            self.assertIn(texto, r.stdout)
        self.assertGreaterEqual(r.stdout.count('Mi primer post en Python |'), 2)
        self.assertGreaterEqual(r.stdout.count('Primeros pasos con Django |'), 2)

    def test_funciones_busqueda_validacion(self):
        m = importar('funciones', ETAPAS/'04_funciones/sistema_blog_modular.py')
        self.assertEqual([p['id'] for p in m.buscar_por_titulo(m.posts,'PYTHON')], [1])
        self.assertEqual([p['id'] for p in m.filtrar_por_tag(m.posts,'python')], [1,2])
        self.assertTrue(m.validar_post(m.posts[0]))
        self.assertFalse(m.validar_post(m.posts[3]))
        for malo in [None, [], {'id':1}, {**m.posts[0], 'autor': 'texto'}, {**m.posts[0], 'tags': None}, {**m.posts[0], 'contenido':' '}]:
            self.assertFalse(m.validar_post(malo))
            m.listar_posts([malo])

    def test_menus_modulares(self):
        for archivo in ['04_funciones/sistema_blog_modular.py', '05_paquetes/main.py']:
            with self.subTest(archivo=archivo):
                r = ejecutar(ETAPAS/archivo, 'texto\n99\n1\n2\nPYTHON\n2\n\n3\nDJANGO\n3\nzzzz\n4\n5\n')
                self.assertEqual(r.returncode, 0, r.stderr)
                for texto in ['La opción debe ser un número', 'Post 4: inválido', 'Post 1: válido', '¡Hasta luego!', 'No se encontraron posts.']:
                    self.assertIn(texto,r.stdout)

class Persistencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ETAPAS/'06_poo_json'))
        from blog.modelos import Autor, Post, Blog
        from blog.datos import cargar_posts, guardar_posts
        cls.Autor, cls.Post, cls.Blog = Autor, Post, Blog
        cls.cargar = staticmethod(cargar_posts)
        cls.guardar = staticmethod(guardar_posts)

    def test_roundtrip_y_busquedas(self):
        autor = self.Autor('Prueba')
        post = self.Post(1,'Python práctico','Contenido',autor,['Python'],'publicado')
        blog = self.Blog([post])
        self.assertIsInstance(post.autor,self.Autor)
        self.assertEqual(blog.buscar_por_titulo('PYTHON'),[post])
        self.assertEqual(blog.filtrar_por_tag('pYtHoN'),[post])
        with tempfile.TemporaryDirectory() as td:
            ruta=Path(td)/'posts.json'
            self.assertTrue(self.guardar(blog.listar(),ruta)[0])
            recuperados, avisos=self.cargar(ruta)
            self.assertEqual(avisos,[])
            self.assertIsInstance(recuperados[0],self.Post)
            self.assertEqual(recuperados[0].a_diccionario(),post.a_diccionario())
            self.assertTrue(self.guardar(recuperados,ruta)[0])
            self.assertTrue(ruta.with_suffix('.json.bak').exists())

    def test_archivos_incorrectos(self):
        with tempfile.TemporaryDirectory() as td:
            ruta=Path(td)/'posts.json'
            self.assertEqual(self.cargar(ruta)[0],[])
            for contenido in ['', '{mal', '{}', '[{}]', '[null]']:
                ruta.write_text(contenido,encoding='utf-8')
                posts, avisos=self.cargar(ruta)
                self.assertEqual(posts,[])
                self.assertTrue(avisos)

    def test_validacion_datos(self):
        with self.assertRaises(ValueError):
            self.Post(1,'Titulo','Contenido','autor como texto',[])
        with self.assertRaises(ValueError):
            self.Post.desde_diccionario({'titulo':'incompleto'})
        with self.assertRaises(ValueError):
            self.Post(1,' ','Contenido',self.Autor('Autor'),[])
        p=self.Post(1,'Titulo','Contenido',self.Autor('Autor'),[])
        with self.assertRaises(ValueError):
            self.Blog([p,p])

    def test_crear_guardar_cerrar_reabrir(self):
        with tempfile.TemporaryDirectory() as td:
            carpeta=Path(td)/'app'
            shutil.copytree(ETAPAS/'06_poo_json',carpeta,ignore=shutil.ignore_patterns('__pycache__','*.bak'))
            r=ejecutar(carpeta/'main.py','x\n4\nPrueba persistente\nContenido de prueba\nAutor prueba\nPython,JSON\npublicado\n6\n7\n')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('Se guardaron 4 posts',r.stdout)
            r=ejecutar(carpeta/'main.py','1\n2\nPERSISTENTE\n3\njson\n5\n7\n')
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertGreaterEqual(r.stdout.count('Prueba persistente'),3)
            self.assertIn('Post 4: válido',r.stdout)

if __name__=='__main__':
    unittest.main(verbosity=2)
