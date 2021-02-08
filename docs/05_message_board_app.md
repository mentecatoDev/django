# 5. Message Board app
- Aplicación en la que los usuarios pueden publicar y leer mensajes cortos con la ayuda de una base de datos.
- Se explorará la interfaz de administración incorporada de Django
- Se agregarán pruebas
- Se subirá a github y se desplegará en Heroku
- Django proporciona soporte incorporado para varios tipos de backends de bases de datos
- Se empezará con SQLite
    + Se ejecuta a partir de un único archivo
    + No requiere una instalación compleja
    + Es una elección perfecta para proyectos pequeños.

##  5.1. Setup Inicial
- Crear un nuevo directorio para el código llamado `mb`
- Instalar Django en un nuevo entorno virtual
- Crear un nuevo proyecto llamado `mb_project`
- Crear una nueva aplicación `posts`
- Actualizar `settings.py`
```bash
$ mkdir mb
$ cd mb
$ pipenv install django
$ pipenv shell
(mb) $ django-admin startproject mb_project .
(mb) $ python manage.py startapp posts
```

FICHERO: `mb_project/settings.py`
```python
	# mb_project/settings.py
	INSTALLED_APPS = [
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'posts.apps.PostsConfig', # new
	]
```
- A continuación, ejecutar el comando `migrate` para crear una base de datos inicial basada en la configuración por defecto de Django.

```
(mb) $ python manage.py migrate
```
- Ahora en el directorio habrá un fichero `db.sqlite3` que representa a la base de datos SQLite.

```bash
(mb) $ ls
db.sqlite3 mb_project manage.py
```
> *Nota*.- Técnicamente se crea un fichero `db.sqlite3` la primera vez que se ejecuta una migración (`migrate`) o se ejecuta el servidor (`runserver`). El uso de `runserver` configura una base de datos utilizando la configuración predeterminada de Django, sin embargo, la migración sincronizará la base de datos con el estado actual de cualquier modelo de base de datos contenido en el proyecto y listado en `INSTALLED_APPS`. En otras palabras, para asegurar que la base de datos refleja el estado actual del proyecto se tendrá que ejecutar `migrate` (y también `makemigrations`) cada vez que se actualiza un modelo. Más en breve.

- Lanzar el servidor local y comprobar el funcionamiento
```
(mb) $ python manage.py runserver
```

## 5.2. Crear un modelo de base de datos
- Crear un modelo de base de datos donde se pueda almacenar y mostrar los mensajes de los usuarios.
- **Django convertirá este modelo en una tabla de base de datos**.

FICHERO: `posts/models.py`
```python
from django.db import models
```
- Django importa un módulo `models` para ayudar a construir nuevos modelos de bases de datos, que "modelan" las características de los datos de la base de datos.

- Se quiere crear un modelo para almacenar el contenido textual de un mensaje en el tablero de mensajes, lo cual se puede hacer de la siguiente manera:

FICHERO: `post/models.py`
```python
from django.db import models

class Post(models.Model):     # new
    text = models.TextField() # new
```
- Se ha creado un nuevo modelo de base de datos llamado `Post` que tiene el campo `text` de tipo `TextField()`.

## 5.3. Activando modelos
- Una vez creado, el modelo tiene que ser activado
1. Primero se crea un archivo de migración con el comando `makemigrations` que genera los comandos SQL para las aplicaciones preinstaladas en nuestra configuración de `INSTALLED_APPS`. Los archivos de migración no ejecutan esos comandos en el archivo de base de datos, sino que son una referencia de todos los cambios en los modelos. Este enfoque significa que tienen un registro de los cambios de los modelos a lo largo del tiempo.
2. En segundo lugar, construimos la base de datos actual con `migrate` que ejecuta la función en el archivo de migraciones.
```bash
(mb) $ python manage.py makemigrations posts
(mb) $ python manage.py migrate posts
```
- No es necesario incluir un nombre después de `makemigrations` o de `migrate` pero es un buen hábito para ser específico.

	+ Si tenemos dos *apps* separadas en nuestro proyecto, se actualizan los modelos en ambos y luego se ejecuta `makemigrations` se genererá un archivo de migraciones que contiene datos sobre **ambas** modificaciones. Esto hace que la depuración sea más difícil en el futuro. Es deseable que cada archivo de migración sea lo más pequeño y aislado posible. De esta forma, si se necesita mirar las migraciones pasadas, sólo hay un cambio por migración en lugar de uno que se aplica a múltiples aplicaciones.

## 5.4. Django Admin
- Django proporciona una robusta interfaz de administración para interactuar con la base de datos (pocos frameworks ofrecen tal cosa).
    + Originado como proyecto en un periódico, los desarrolladores querían un CMS para que los periodistas pudieran escribir y editar sus historias sin tocar "código".
- Para utilizar el administrador de Django, primero necesitamos crear un superusuario que pueda iniciar sesión.

``` bash
(mb) $ python manage.py createsuperuser
Username (leave blank to use 'mentecato'): mentecato
Email:
Password:
Password (again):
Superuser created successfully.
```
- Reiniciar el servidor Django con `python manage.py` y en el navegador ir
a http://127.0.0.1:8000/admin/.

- Necesitamos decirle explícitamente a Django qué mostrar en la página de administración.

FICHERO: `post/admin.py`
```python
from django.contrib import admin

from posts.models import Post # new

admin.site.register(Post)     # new
```
- Ahora crear el primer mensaje en el tablero de mensajes.
- *Problema*: La nueva entrada se llama “Post object”, lo cual no es muy útil
    + Cambiamos eso añadiendo una nueva función `__str__` como sigue:

FICHERO: `posts/models.py`
```python
# posts/models.py
from django.db import models


class Post(models.Model):
    text = models.TextField()

    def __str__(self):        # new
        return self.text[:50] # new
```

- El cometido del método `__str__` es establecer el nombre que recibirá el post. Con el código anterior lo hemos redefinido (*overriden*) para que su nombre se establezca como los primeros 50 caracteres del texto del propio post.
- Es una buena práctica añadir métodos `__str__()` a todos los modelos para aumentar la legibilidad.

## 5.5. Views/Templates/URLs
- Para poder **mostrar** el contenido de la **base de datos** en la web, hay que conectar las **vistas**, las **plantillas** y las **URLConfs**.
### 5.5.1. Vista
- Django viene equipado con el `ListView` genérico basado en clases.

FICHERO: `posts/views.py`
```python
# posts/views.py
from django.views.generic import ListView # new
from .models import Post                  # new


class HomePageView(ListView):             # new
    model = Post                          # new
    template_name = 'home.html'           # new
```
- Se importa de la colección de vistas genéricas que tiene Django la clase `ListView` para personalizarla
- Se define qué modelo se va a usar
- En la vista, se deriva la clase `ListView` para especificar el nombre del **modelo** y la referencia a la **plantilla**.
    + Internamente `ListView` devuelve una variable de contexto llamada `object_list` que hay que mostrar en la plantilla.

### 5.4.2. Plantilla
- Crear un directorio en el nivel del proyecto que se llame `templates` y una plantilla `home.html` en él
```bash
(mb) $ mkdir templates
(mb) $ touch templates/home.html
```
- Actualizar el campo `DIRS` del archivo`settings.py` para que Django sepa cómo acceder a la carpeta `templates`.

```python
# settings.py
TEMPLATES = [
    {
        ...
        'DIRS': [str(BASE_DIR.joinpath('template'))],   # new
        ...
    },
]
```
- En el archivo `home.html` se puede usar bucle `for` del lenguaje de plantillas de Django para listar todos los objetos en `object_list`.

FICHERO: `templates/home.html`
```html
<!-- templates/home.html -->						# new
<h1>Página de Inicio del Tablón de Anuncios</h1>	# new
<ul>												# new
    {% for post in object_list %}					# new
        <li>{{ post.text }}</li>					# new
    {% endfor %}									# new
</ul>												# new
```
- El nombre `object_list` no es muy apropiado así que pondremos uno más explícito a través del atributo `context_object_name`.

FICHERO: `posts/views.py`

```python
from django.views.generic import ListView
from .models import Post

class HomePageView(ListView):
	model = Post
	template_name = 'home.html'
	context_object_name = 'all_posts_list'			# new
```
- ...que cambiaremos en:

FICHERO: `templates/home.html`
```html
...
    {% for post in all_posts_list %}				# new
...
```

- Modificamos las urls del proyecto en:

FICHERO: `mb_project/urls.py`

```python
# mb_project/urls.py
from django.contrib import admin
from django.urls import path, include	# new


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),	# new
]
```
- Crearemos el fichero `urls.py` a nivel de app
```
(mb) $ touch posts/urls.py
```
- ...con el siguiente contenido:

FICHERO: `posts/urls.py`
```python
from django.urls import path						# new
from .views import HomePageView						# new


urlpatterns = [										# new
    path('', HomePageView.as_view(), name='home'),	# new
]													# new
```
- Reiniciar el servidor que ahora mostrará los post del tablón de mensajes
- Añádanse más posts ;-)
- No olvidar
```
(mb) $ git init
(mb) $ git add -A
(mb) $ git commit -m 'Commit inicial'
```
## 5.6. Tests
- Se necesita usar `TestCase` en lugar de `SimpleTestCase` dado que ahora tenemos una base de datos y no solo una página estática.
- Se creará una base de datos con la que se pueden hacer pruebas (tal y como se haría en una base de datos real).
- Se empezará añadiendo un mensaje de muestra al campo de la base de datos de texto para luego comprobar que se almacena correctamente.
- Es importante que todos los métodos de prueba comiencen con `test_` para que Django sepa cómo manejarlos

FICHERO: `posts/test.py`
```python
	# posts/tests.py
	from django.test import TestCase
ç	from .models import Post
	
	
ç	class PostModelTest(TestCase):

ç	    def setUp(self):
ç	        Post.objects.create(text='just a test')

ç	    def test_text_content(self):
ç	        post = Post.objects.get(id=1)
ç	        expected_object_name = f'{post.text}'
ç	        self.assertEqual(expected_object_name, 'just a test')
```
1. Importa el módulo `TestCase` que permite crear una base de datos de muestra
2. Importa el modelo `Post`
3. Se crea una nueva clase `PostModelTest` y se le añade un método `setUp`
para crear una nueva base de datos con una sola entrada: `'just a test'`

- Se ejecuta `test_text_content` para comprobar que el campo de la base de datos realmente contiene `just a test`.
    + Se crea una variable llamada `post` que representa el primer `id` del modelo Post.
    + Django asigna automáticamente esta identificación
- La siguiente línea usa "cadenas f", que son una adición muy interesante desde Python 3.6, y permiten poner variables directamente en las cadenas siempre y cuando estén rodeadas de corchetes `{}`
- Se establece `expected_object_name` como el valor de la cadena en `post.text` que permitirá hacer la prueba
- En la última línea se usa `assertEqual` para comprobar que la entrada recién creada coincide con la dispuesta al principio
- Ejecutar la prueba con `python manage.py test`

```bash
(mb) $ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
---------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...
```
- A pesar de lo aparentemente complicado del asunto pronto se verá que en la mayor parte de los casos, los tests son repetitivos.
- El segundo test comprueba una sola página: la *homepage*. En concreto comprueba que exista (lanza una respuesta HTTP 200). Usa la vista `home` y la plantilla `home.html`.
-  
Se necesita añadir un `import` más para `reverse` y una nueva clase `HomePageViewTest`
```python
from django.test import TestCase
from django.urls import reverse  #new
from .models import Post


class PostModelTest(TestCase):
 
    def setUp(self):
        Post.objects.create(text='just a test')

    def test_text_content(self):
        post=Post.objects.get(id=1)
        expected_object_name = f'{post.text}'
        self.assertEqual(expected_object_name, 'just a test')


class HomePageViewTest(TestCase): 						# new

    def setUp(self):									# new
        Post.objects.create(text='this is another test')# new

    def test_view_url_exists_at_proper_location(self):  # new
        resp = self.client.get('/')                     # new
        self.assertEqual(resp.status_code, 200)         # new

     def test_view_url_by_name(self):                   # new
        resp = self.client.get(reverse('home'))         # new
        self.assertEqual(resp.status_code, 200)         # new

    def test_view_uses_correct_template(self):          # new
        resp = self.client.get(reverse('home'))         # new
        self.assertEqual(resp.status_code, 200)         # new
        self.assertTemplateUsed(resp, 'home.html')      # new
```
- Ejecutando el test:
```bash
(mb) $ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 4 tests in 0.036s

OK
Destroying test database for alias 'default'...
```
- 4 test: `test_text_content`, `test_view_url_exists_at_proper_location`, `test_view_url_by_name` y  `test_view_uses_correct_template`.
- Cualquier función que tenga la palabra `test*` al principio y exista en un fichero `tests.py` se lanzará cuando se ejecuta el comando `python manage.py test`.

- Hora de hacer *commit* de los cambios.
```bash
(mb) $ git add -A
(mb) $ git commit -m 'added tests'
```
## 5.7. GitHub
- Subir el proyecto...
## 5.8. Heroku configuration
- Hay que hacer los siguientes cambios al projecto para desplegarlo online:
    + Actualizar `Pipfile.lock`
    + Crear `Procfile`
    + Instalar `gunicorn`
    + Actualizar `settings.py`

### 5.8.1. Actualizar `Pipfile.lock`
- Especificar la versión de python que se está usando
FICHERO: `Pipfile`
```Pipfile
# Pipfile
[requires]
python_version = "3.8"
```
Ejecutar `pipenv lock` para generar el `Pipfile.lock` adecuado.
```bash
(mb) $ pipenv lock
```
### 5.8.2. Crear `Procfile`
- Le dirá a Heroku *cómo* ejecutar el servidor remoto donde habita el código.
```bash
(mb) $ touch Procfile
```
### 5.8.3. Instalar `gunicorn`
- Por ahora Heroku usa `gunicorn` como servidor de producción y mira en el fichero `mb_project.wsgi` para más instrucciones.

```
web: gunicorn mb_project.wsgi --log-file -
```

- Luego, se instala `gunicorn`, que se usará en producción mientras se siga usando el servidor interno de Django para desarrollo local.

```
(mb) $ pipenv install gunicorn
```
### 5.8.4. Actualizar `settings.py`
- Anteriormente, establecíamos `ALLOWED_HOSTS` en `*`, lo que significaba aceptar todos los hosts; esto es una atajo peligroso. Podemos, y debemos, ser más específicos. Los dos hosts locales en los que se ejecuta Django son: `localhost:8000` y `127.0.0.1:8000`. También sabemos que, una vez desplegado, cualquier sitio Heroku terminará con `.herokuapp.com`. Podemos añadir las tres rutas a nuestra configuración.


  FICHERO: mb_project/settings.py
```python
# mb_project/settings.py
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']
```
- Ahora `commit` y `push`
```
(mb) $ git status
(mb) $ git add -A
(mb) $ git commit -m 'Actualiza el despliegue en Heroku'
(mb) $ git push -u origin master
```
## 5.9. Despliegue en Heroku
- *Login*
```bash
(mb) $ heroku login
```
- *Create*.- Genera un nombre aleatorio para la aplicación
```bash
(mb) $ heroku create
Creating app... done,agile-inlet-25811
https://agile-inlet-25811.herokuapp.com/ | https://git.heroku.com/agile-inlet-25811.git
```
- Establecer a git para usar el nombre de la nueva aplicación cuando se suba el código a Heroku.
```bash
(mb) $ heroku git:remote -a agile-inlet-25811
```
- Indicar a que ignore los archivos estáticos (se tratará más adelante).
```
(mb) $ heroku config:set DISABLE_COLLECTSTATIC=1
```
-  Subir el código a Heroku y añadir escalado gratuito para que se ejecute realmente en línea, de lo contrario el código sólo se quedará alojado.
```
(mb) $ git push heroku master
(mb) $ heroku ps:scale web=1
```
- Abrir el código con `heroku open` y automáticamente mostrará un navegador con la URL de la aplicación.

## 5.10. Conclusión
- Se ha construido, probado e implementado la primera aplicación básica basada en una base de datos.
- Faltarían formularios para interactuar con el sitio (el panel de administración no es lo adecuado).
- Se creará una aplicación de blog con formularios para que los usuarios puedan crear, editar y borrar mensajes.
- Se le añadirá estilo a través de CSS.



|\/| [- |\| ~|~ [- ( /\ ~|~ () ^/_ '|                             