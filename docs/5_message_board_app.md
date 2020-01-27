# Message Board app
- Aplicación en la que los usuarios pueden publicar y leer mensajes cortos con la ayuda de una base de datos.
- Se explorará la interfaz de administración incorporada de Django
- Se agregarán pruebas
- Se subirá a github y se desplegará en Heroku
- Django proporciona soporte incorporado para varios tipos de backends de bases de datos
- Se empezará con SQLite
    + Se ejecuta a partir de un único archivo
    + No requiere una instalación compleja
    + Es una elección perfecta para proyectos pequeños.

##  Setup Inicial
- Crear un nuevo directorio para nuestro código en el Escritorio llamado `mb`
- Instalar Django en un nuevo entorno virtual
- Crear un nuevo proyecto llamado `mb_project`
- Crear una nueva aplicación `posts`
- Actualizar `settings.py`
```
$ cd ~/Desktop
$ mkdir mb
$ cd mb
$ pipenv install django
$ pipenv shell
(mb) $ django-admin startproject mb_project .
(mb) $ python manage.py startapp posts
```

FICHERO: `mb_project/settings.py`
```
# mb_project/settings.py
INSTALL_APPS = [
'django.contrib.admin',
'django.contrib.auth',
django.contrib.contenttypes',
django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'posts', # new
]
```
A continuación, ejecutar el comando `migrate` para crear una base de datos inicial basada en la configuración por defecto de Django.
```
(mb) $ python manage.py migrate
```
Ahora en el directorio habrá ahora un fichero `db.sqlite3` que representa a la base de datos SQLite.
```
(mb) $ ls
db.sqlite3 mb_project manage.py
```
> *Nota*.- Técnicamente se crea un fichero `db.sqlite3` la primera vez que se ejecuta una migración (`migrate`) o se ejecuta el servidor (`runserver`). El uso de `runserver` configura una base de datos utilizando la configuración predeterminada de Django, sin embargo, la migración sincronizará la base de datos con el estado actual de cualquier modelo de base de datos contenido en el proyecto y listado en `INSTALLED_APPS`. En otras palabras, para asegurar de que la base de datos refleja el estado actual del proyecto se tendrá que ejecutar `migrate` (y también `makemigrations`) cada vez que se actualiza un modelo. Más en breve.

- Lanzar el  servidor local y comprobar el funcionamiento
```
(mb) $ python manage.py runserver
```

## Crear un modelo de base de datos
- Crear un modelo de base de datos donde se pueda almacenar y mostrar los mensajes
de los usuarios.
- Django convertirá este modelo en una tabla de base de datos.

FICHERO: `posts/models.py`
```
# posts/models.py
from django.db import models

# Create your models here
```
Django importa un módulo `models` para ayudarnos a construir nuevos modelos de bases de datos, que "modelan" las características de los datos de la base de datos.
- Se quiere crear un modelo para almacenar el contenido textual de un mensaje en el tablero de mensajes, lo cual podemos hacer de la siguiente manera:

FICHERO: `post/models.py`
```
# posts/models.py
from django.db import models

class Post(models.Model):
    text = models.TextField()
```
- Se ha creado un nuevo modelo de base de datos llamado `Post` que tiene el campo `text` de tipo `TextField()`.

## Activating models
- Una vez creado el model tiene que ser activado
1. Primero se crea un archivo de migración con el comando `makemigrations` que genera los comandos SQL para aplicaciones preinstaladas en nuestra configuración de INSTALLED_APPS. Los archivos de migración no ejecutan esos comandos en el archivo de base de datos, sino que son una referencia de todos los cambios en los modelos. Este enfoque significa que tienen un registro de los cambios de los modelos a lo largo del tiempo.
2. En segundo lugar, construimos la base de datos actual con `migrate` que ejecuta la función en el archivo de migraciones.
```bash
(mb) $ python manage.py makemigrations posts
(mb) $ python manage.py migrar posts
```
- No es necesario incluir un nombre después de `makemigrations` o de `migrate` pero es un buen hábito para ser específico.

	+ Si tenemos dos aplicaciones separadas en nuestro proyecto, se actualizan los modelos en ambos y luego se ejecuta `makemigrations` se genererá un archivo de migraciones que contiene datos sobre **ambas** modificaciones. Esto hace que la depuración sea más difícil en el futuro. Es deseable que cada archivo de migración sea lo más pequeño y aislado posible. De esta forma, si se necesita mirar las migraciones pasadas, sólo hay un cambio por migración en lugar de uno que se aplica a múltiples aplicaciones.

## Django Admin
- Django proporciona una robusta interfaz de administración para interactuar con la base de datos (pocos frameworks ofrecen tal cosa).
    + Originado como proyecto en un periódico, los desarrolladores querían un CMS para que los periodistas pudieran escribir y editar sus historias sin tocar "código".
- Para utilizar el administrador de Django, primero necesitamos crear un superusuario que pueda iniciar sesión.

``` bash
(mb) $ python manage.py createsuperuser
Username (leave blank to use 'wsv'): wsv
Email:
Password:
Password (again):
Superuser created successfully.
```
- Reiniciar el servidor Django con `python manage.py` y en el navegador ir
a http://127.0.0.1:8000/admin/.

- Necesitamos decirle explícitamente a Django qué mostrar en la página de administración.
FICHERO: `post/admin.py`
```
# posts/admin.py
from django.contrib import admin

from .models import Post

admin.site.register(Post)
```
- Ahora crear el primer mensaje en el tablero de mensajes.
- *Problema*: La nueva entrada se llama “Post object”, lo cual no es muy útil
    + Cambiamos eso añadiendo una nueva función `__str__` como sigue:

FICHERO: `posts/models.py`
```
# posts/models.py
from django.db import models


class Post(models.Model):
    text = models.TextField()


def __str__(self):
    """A string representation of the model."""
    return self.text[:50]
```

- Es una buena práctica añadir métodos `str()` a todos los modelos para aumentar la legibilidad.

## Views/Templates/URLs
- Para poder mostrar el contenido de la base de datos en la web, hay que conectar las vistas, las plantillas y las URLConfs.
### Vista
- Django viene equipado con el `ListView` genérico basado en clases.

FICHERO: `posts/views.py`
```
# posts/views.py
from django.views.generic import ListView
from .models import Post


class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
```
- Importar `ListView`
- Definir qué modelo se va a usar
- En la vista, se deriva la clase `ListView` para especificar el nombre del modelo y la referencia de la plantilla.
    + Internamente `ListView` devuelve un ojeto llamado `object_list` que hay que mostrar en la plantilla.

### Plantilla
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```
- En el archivo `home.html` se puede usar bucle `for` del lenguaje de plantillas de Django para listar todos los objetos en `object_list`.
FICHERO: `templates/home.html`
```html
<!-- templates/home.html -->
<h1>Message board homepage</h1>
<ul>
    {% for post in object_list %}
        <li>{{ post }}</li>
    {% endfor %}
</ul>
```
### URLConfs
FICHERO: `mb_project/urls.py`
```
# mb_project/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]
```
- Crear el fichero `urls.py` a nivel de app
```
(mb) $ touch posts/urls.py
```
...con el siguiente contenido:
FICHERO: `posts/urls.py`
```
# posts/urls.py
from django.urls import path


from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]
```
- Reiniciar el servidor que ahora mostrará los post del tablón de mensajes
- Añádanse más posts ;-)
- No olvidar
```
(mb) $ git init
(mb) $ git add -A
(mb) $ git commit -m 'Realiza el commit inicial'
```
### Tests
- Se necesita usar `TestCase` dado que ahora tenemos una base de datos y no solo una página estática.
- Se creará una base de datos con la que se pueden hacer pruebas (no se hacen con la base de datos real).
- Se empezará añadiendo un mensaje de muestra al campo de la base de datos de texto para luego comprobar que se almacena correctamente.
- Es importante que todos los métodos de prueba comiencen con `test_` para que Django sepa cómo manejarlos

FICHERO: `posts/test.py`
```python
# posts/tests.py
from django.test import TestCase
from .models import Post


class PostModelTest(TestCase):

    def setUp(self):
        Post.objects.create(text='just a test')

    def test_text_content(self):
        post=Post.objects.get(id=1)
        expected_object_name = f'{post.text}'
        self.assertEqual(expected_object_name, 'just a test')
```
1. Importa el módulo `TestCase` que permite crear una base de datos de muestra
2. Importa el modelo `Post`
3. Se crea una nueva clase `PostModelTest` y se le añade un método `setUp`
para crear una nueva base de datos con una sola entrada: "just a test"

- Ejecutar `test_text_content`, para comprobar que el campo de la base de datos realmente contiene `just a test`.
    + Se crea una variable llamada `post` que representa el primer `id` en el modelo de Post.
    + Django asigna automáticamente esta identificación
- La siguiente línea usa "cadenas f", que son una adición muy interesante a Python 3.6, y permiten poner variables directamente en las cadenas siempre y cuando estén rodeadas de corchetes {}
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
- A pesar de lo aparentemente complicado del asunto pronto se verá que en la mayor parte de los casos, los tests son repetitivos
-  our second test. The first test was on the model but now we want test our
  one and only page: the homepage. Specifically, we want to test that it exists (throws
  an HTTP 200 response), uses the home view, and uses the home.html template.
  We’ll need to add one more import at the top for reverse and a brand new class
  HomePageViewTest for our test.88
  Chapter 4: Message Board app
  Code
  from django.test import TestCase
  from django.urls import reverse
  from .models import Post
  class PostModelTest(TestCase):
  def setUp(self):
  Post.objects.create(text='just a test')
  def test_text_content(self):
  post=Post.objects.get(id= )
  expected_object_name = f'{post.text}'
  self.assertEqual(expected_object_name, 'just a test')
  class HomePageViewTest(TestCase):
  def setUp(self):
  Post.objects.create(text='this is another test')
  def test_view_url_exists_at_proper_location(self):
  resp = self.client.get('/')
  self.assertEqual(resp.status_code,
  )
  def test_view_url_by_name(self):
  resp = self.client.get(reverse('home'))
  self.assertEqual(resp.status_code,
  )89
  Chapter 4: Message Board app
  def test_view_uses_correct_template(self):
  resp = self.client.get(reverse('home'))
  self.assertEqual(resp.status_code,
  )
  self.assertTemplateUsed(resp, 'home.html')
  If you run our tests again you should see that they pass.
  Command Line
  (mb) $ python manage.py test
  Creating test database for alias 'default'...
  System check identified no issues (
  silenced).

.
----------------------------------------------------------------------
Ran
tests in
.
s
OK
Destroying test database for alias 'default'...
Why does it say four tests? Remember that our setUp methods are not actually tests,
they merely let us run subsequent tests. Our four actual tests are test_text_content ,
test_view_url_exists_at_proper_location , test_view_url_by_name , and test_view_-
uses_correct_template .
Any function that has the word test* at the beginning and exists in a tests.py file will
be run when we execute the command python manage.py test .
We’re done adding code for our testing so it’s time to commit the changes to git.90
Chapter 4: Message Board app
Command Line
(mb) $ git add -A
(mb) $ git commit -m 'added tests'
## Bitbucket
We also need to store our code on Bitbucket. This is a good habit to get into in
case anything happens to your local computer and it also allows you to share and
collaborate with other developers.
You should already have a Bitbucket account from Chapter 3 so go ahead and create
a new repo which we’ll call mb-app .
Bitbucket create app
On the next page click on the bottom link for “I have an existing project”. Copy the
two commands to connect and then push the repository to Bitbucket.Chapter 4: Message Board app
91
It should look like this, replacing wsvincent (my username) with your Bitbucket
username:
Command Line
(mb) $ git remote add origin git@bitbucket.org:wsvincent/mb-app.git
(mb) $ git push -u origin master
## Heroku configuration
You should also already have a Heroku account setup and installed from Chapter 3.
We need to make the following changes to our Message Board project to deploy it
online:
• update Pipfile.lock
• new Procfile
• install gunicorn
• update settings.py
Within your Pipfile specify the version of Python we’re using, which is . . Add these
two lines at the bottom of the file.
Code
# Pipfile
[requires]
python_version = " . "
Run pipenv lock to generate the appropriate Pipfile.lock .Chapter 4: Message Board app
92
Command Line
(mb) $ pipenv lock
Then create a Procfile which tells Heroku how to run the remote server where our
code will live.
Command Line
(mb) $ touch Procfile
For now we’re telling Heroku to use gunicorn as our production server and look in our
mb_project.wsgi file for further instructions.
Command Line
web: gunicorn mb_project.wsgi --log-file -
Next install gunicorn which we’ll use in production while still using Django’s internal
server for local development use.
Command Line
(mb) $ pipenv install gunicorn
Finally update ALLOWED_HOSTS in our settings.py file.
Code
# mb_project/settings.py
ALLOWED_HOSTS = ['*']
We’re all done! Add and commit our new changes to git and then push them up to
Bitbucket.93
Chapter 4: Message Board app
Command Line
(mb) $ git status
(mb) $ git add -A
(mb) $ git commit -m 'New updates for Heroku deployment'
(mb) $ git push -u origin master
## Heroku deployment
Make sure you’re logged into your correct Heroku account.
Command Line
(mb) $ heroku login
Then run the create command and Heroku will randomly generate an app name for
you. You can customize this later if desired.
Command Line
(mb) $ heroku create
Creating app... done,
https://agile-inlet-
agile-inlet-
.herokuapp.com/ | https://git.heroku.com/agile-inlet-
.git
Set git to use the name of your new app when you push code to Heroku. My Heroku-
generated name is agile-inlet-
so the command looks like this.
\94
Chapter 4: Message Board app
Command Line
(mb) $ heroku git:remote -a agile-inlet-
Tell Heroku to ignore static files which we’ll cover in-depth when deploying our Blog
app later in the book.
Command Line
(mb) $ heroku config:set DISABLE_COLLECTSTATIC=
Push the code to Heroku and add free scaling so it’s actually running online, otherwise
the code is just sitting there.
Command Line
(mb) $ git push heroku master
(mb) $ heroku ps:scale web=
If you open the new project with heroku open it will automatically launch a new
browser window with the URL of your app. Mine is live at:
https://agile-inlet-25811.herokuapp.com/.
Live siteChapter 4: Message Board app
95
## Conclusion
We’ve now built, tested, and deployed our first database-driven app. While it’s
deliberately quite basic, now we know how to create a database model, update it
with the admin panel, and then display the contents on a web page. But something is
missing, no?
In the real-world, users need forms to interact with our site. After all, not everyone
should have access to the admin panel. In the next chapter we’ll build a blog appli-
cation that uses forms so that users can create, edit, and delete posts. We’ll also add
styling via CSS.