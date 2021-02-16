# 6. Blog app

- Se construirá una aplicación de Blog que permita a los usuarios crear, editar y eliminar posts.
- La página de inicio listará todos los artículos del blog
- Habrá una página de detalles dedicada a cada artículo individual.
- Se introduce CSS para el estilo y se verá cómo funciona Django con los archivos estáticos.

## 6.1. Configuración inicial
- Nuevo proyecto Django:
    - crear un nuevo directorio para el código en el Escritorio llamado blog
    - instalar Django en un nuevo entorno virtual
    - crear un nuevo proyecto de Django llamado `blog_project`
    - crear una nueva aplicación de nombre `blog`
    - realizar una migración para configurar la base de datos
    - actualizar `settings.py`

```bash
$ cd ~/Desktop 
$ mkdir blog
$ cd blog
$ pipenv install django
$ pipenv shell
(blog) $ django-admin startproject blog_project .
(blog) $ python manage.py startapp blog
(blog) $ python manage.py migrate
(blog) $ python manage.py runserver
```

FICHERO: `blog_project/settings.py`
```python
    # blog_project/settings.py
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'blog.apps.BlogConfig',        # new
    ]
```
## 6.2. Modelos de Bases de Datos
- Se asume que cada *post* tiene un título, un autor y un cuerpo que se convertirán en un modelo de base de datos:

FICHERO: `blog/models.py`
```python
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(
        'Título',
        max_length=200
    )
    author = models.ForeignKey(
        'auth.User',
        verbose_name='Autor',
        on_delete=models.CASCADE,
    )
    body = models.TextField(
        'Cuerpo'
    )

    def __str__(self):
        return self.title
```
- Se importan los modelos de la clase y luego se crea una subclase del modelo llamada `Post`.
- Usando esta funcionalidad de subclase se tiene acceso automáticamente a todo lo que hay dentro de `django.db.models.Models` y se pueden añadir campos y métodos adicionales según se desee.
- El título se limita a 200 caracteres y para el cuerpo se usa un campo de texto que se expandirá automáticamente según sea necesario para adaptarse al texto del usuario.
    + **Hay muchos tipos de campos disponibles en Django**; se puede ver la lista completa [aquí](https://docs.djangoproject.com/es/3.1/ref/models/fields/#field-types).
- Para el campo de autor se usa una clave foránea (`ForeignKey`) que permite una relación de *uno a muchos*: un autor puede tener muchas entradas de blog diferentes, pero no al revés.
- La referencia `auth.User` pertenece al modelo de usuario incorporado que Django proporciona para la autenticación.
- Para todas las relaciones de uno a muchos, con `ForeignKey`, también debemos especificar una opción de `on_delete`.
- En todos los campos se ha insertado el valor para `verbose_name` que recoge la etiqueta que se utilizará una vez que se presenten los datos en los templates.
- Ahora que se ha creado el nuevo modelo de base de datos, se necesita crear un nuevo registro de migración para él y migrar el cambio a la base de datos. Este proceso de dos pasos se puede completar con los siguientes comandos:
```bash
(blog) $ python manage.py makemigrations blog
(blog) $ python manage.py migrate blog
```
Base de datos configurada.


## 6.3. Admin
### 6.3.1. Para acceder a los datos:
- Crear una cuenta de superusuario
```bash
(blog) $ python manage.py createsuperuser
Username (leave blank to use 'wsv'): wsv
Email:
Password:
Password (again):
Superuser created successfully.
```

- Arrancar el servidor y abrir http://127.0.0.1:8000/admin/
- Logear con la nueva cuenta de superusuario
- !Ups! ¿Dónde está el nuevo modelo `Post`?
- Se olvidó actualizar `blog/admin.py`

FICHERO: `blog/admin.py`
```python
# blog/admin.py
from django.contrib import admin
from .models import Post


admin.site.register(Post)
```
- Refrescar ahora y añadir dos blog post para tener algunos datos de muestra con los que trabajar
    + Añadir un "autor" a cada entrada también, ya que por defecto todos los campos del modelo son obligatorios

## 6.4 URLs
```bash
(blog) $ touch blog/urls.py
```
FICHERO:`blog/urls.py`
```python
from django.urls import path
from . import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
]
```
FICHERO: `blog_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

## 6.5. Views
FICHERO: `blog/views.py`
```python
from django.views.generic import ListView
from .models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
```

## 6.6. Templates

```bash
(blog) $ mkdir templates
(blog) $ touch templates/base.html
(blog) $ touch templates/home.html
```

FICHERO: `blog_project/settings.py`
```python
TEMPLATES = [
    {
        ...
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        ...
    },
]
```

FICHERO: `templates/base.html`
```html
<html>
  <head>
    <title>Django blog</title>
  </head>
  <body>
    <header>
      <h1><a href="/">Django blog</a></h1>
    </header>
    <div class="container">
      {% block content %}
      {% endblock content %}
    </div>
  </body>
</html>
```

- El código entre `{% block content %}` y `{% endblock content %}` puede llenarse con otras plantillas.

FICHERO:  `templates/home.html`
```html
{% extends 'base.html' %}

{% block content %}
  {% for post in object_list %}
    <div class="post-entry">
      <h2><a href="">{{ post.title }}</a></h2>
      <p>{{ post.body }}</p>
    </div>
  {% endfor %}
{% endblock content %}
```

- Observar que `object_list` proviene de `ListView` y contiene todos los objetos de la vista.
- Iniciar de nuevo el servidor Django: `python manage.py runserver`
- Terrible, ¿no?

## 6.7. Ficheros estáticos
- Un poco de CSS, please
- En un proyecto Django listo para la producción, normalmente se almacenaría en una [red de distribución de contenidos (CDN, *Content Delivery Network*)](https://es.wikipedia.org/wiki/Red_de_distribuci%C3%B3n_de_contenidos) para un mejor rendimiento, pero para este caso, el almacenamiento de los archivos en local está bien.

```bash
(blog) $ mkdir static
```
- Al igual que se hizo con la carpeta de plantillas, se necesita actualizar el archivo `settings.py` para decirle a Django dónde buscar estos archivos estáticos.
- Añadir en la parte inferior del archivo, debajo de la entrada para `STATIC_URL`.

FICHERO: `blog_project/settings.py`
```python
STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
```

- Crear una carpeta `css` dentro de `static` y crear el fichero `base.css`

```bash
(blog) $ mkdir static/css
(blog) $ touch static/css/base.css
```

FICHERO: `static/css/base.css`
```css
header h1 a {
  color: red;
}
```
- Añadir el fichero estático a la plantilla añadiendo `{% load static %}` al pricipio de `base.html`
    - Como las otras plantillas se heredan de `base.html` sólo hay que añadirlo una vez

FICHERO: `templates/base.html`
```html
{% load static %}
<html>
  <head>
    <title>Django blog</title>
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
  </head>
...
```
- Ahora se pueden añadir archivos estáticos y aparecerán automáticamente en todas las plantillas.
- ¿Qué tal si se añade una fuente personalizada y algo más de CSS?

FICHERO: ` templates/base.html`
```html
{% load static %}
<html>
  <head>
    <title>Django blog</title>
    <link rel="\stylesheet" href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:4000">  <!-- new -->
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
  </head>
...
```
- Actualizar el archivo css

FICHERO: `static/css/base.css`
```css
body {
  font-family: 'Source Sans Pro', sans-serif;
  font-size: 18px;
}

header {
  border-bottom: 1px solid #999;
  margin-bottom: 2rem;
  display: flex;
}

header h1 a {
  color: red;
  text-decoration: none;
}

.nav-left {
  margin-right: auto;
}

.nav-right {
  display: flex;
  padding-top: 2rem;
}

.post-entry {
  margin-bottom: 2rem;
}

.post-entry h2 {
  margin: 0.5rem 0;
}

.post-entry h2 a,
.post-entry h2 a:visited {
  color: blue;
  text-decoration: none;
}

.post-entry p {
  margin: 0;
  font-weight: 400;
}

.post-entry h2 a:hover {
  color: red;
}
```

## 6.8. Blog pages individuales
- Ahora se puede añadir funcionalidad a las páginas de blog individuales.

- Crear una nueva vista, url y plantilla.

- Se puede usar la vista genérica basada en clases `DetailView` para simplificar las cosas.

  

FICHERO: `blog/views.py`
```python
from django.views.generic import ListView, DetailView # new
from .models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
```
- Por defecto `DetailView` proporciona un objeto de contexto que podemos usar en la plantilla llamado `objeto` o el nombre en minúsculas de nuestro modelo, `post`.
-  Además, `DetailView` espera que se le pase una clave primaria o un *slug* como identificador. Más sobre esto en breve.

```bash
(blog) $ touch templates/post_detail.html
```

FICHERO: `templates/post_detail.html`
```html
{% extends 'base.html' %}

{% block content %}
  <div class="post-entry">
    <h2>{{ post.title }}</h2>
    <p>{{ post.body }}</p>
  </div>
{% endblock content %}
```
- En la parte superior se especifica que esta plantilla hereda de base.html.
- Luego se muestra el título y cuerpo del objeto de contexto, que `DetailView` hace accesible como `post`.
- La denominación de los objetos de contexto en vistas genéricas es extremadamente confusa cuando se ve Django por primera vez. Debido a que nuestro objeto de contexto de `DetailView` es o bien el nombre de modelo `post` o bien `object`, podríamos también actualizar nuestro modelo de la siguiente manera y funcionaría exactamente igual.

FICHERO: `templates/post_detail.html`
```html
{% extends 'base.html' %}

{% block content %}
  <div class="post-entry">
    <h2>{{ object.title }}</h2>
    <p>{{ object.body }}</p>
  </div>
  
{% endblock content %}
```
- Si se encuentra confuso el uso de `post` o de `objeto`, también podemos establecer explícitamente el nombre del objeto del contexto en la vista. Así que si quisiéramos llamarlo `anything_you_want` y luego usarlo en la plantilla, el código tendría el siguiente aspecto y funcionaría igual.

FICHERO: `blog/views.py`
```python
...
class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'anything_you_want'
```
FICHERO: `templates/post_detail.html`
```html
{% extends 'base.html' %}

{% block content %}
  <div class="post-entry">
    <h2>{{ anything_you_want.title }}</h2>
    <p>{{ anything_you_want.body }}</p>
</div>

{% endblock content %}
```
- La "magia" en la denominación del objeto de contexto es un precio que se paga por la facilidad y la sencillez del uso de vistas genéricas. Son geniales si se sabe lo que se hace pero pueden ser difíciles de personalizar si se quiere un comportamiento diferente.
- Añadir una nueva URLConf para la vista

FICHERO: `blog/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
]
```
- Todas las entradas del blog comenzarán con `post/`. Lo siguiente es la clave principal de la entrada que se representará como un entero `<int:pk>`.
-  ¿Cuál es la clave primaria? Django añade automáticamente una clave primaria autoincrementada a los modelos de base de datos. Así que mientras que sólo se declaran los campos `title`, `author` y `body` en el modelo de publicación, bajo el capó, Django también añadió otro campo llamado `id`, que es la clave primaria. Se puede acceder a ella como `id` o `pk`.
- La `pk` para el primer post "Hola, Mundo" es 1. Para el segundo post, es 2. Y así sucesivamente. Por lo tanto, cuando se vaya a la página de entrada individual para el primer post, el patrón de dirección es `post/1`.
> Nota:
>
> Entender cómo funcionan claves primarias con `DetailView` es un punto de confusión muy común en los principiantes. Vale la pena releer los dos párrafos anteriores unas cuantas veces. Con la práctica se convertirá en algo natural.
- Si se inicia el servidor con `python manage.py runserver` y se va directamente a http://127.0.0.1:8000/post/1/ se verá una página dedicada para la primera entrada en el blog.
- También se puede ir a http://127.0.0.1:8000/post/2/ para ver la segunda entrada.
- Para facilitar el acceso, se debería actualizar el enlace en la página de inicio para poder acceder directamente a las entradas individuales del blog desde allí. Actualmente en `home.html` el enlace está vacío: `<a href="">` . Actualizarlo a `<a href="{% url 'post_detail' post.pk %}">`.

FICHERO: `templates/home.html`
```html
{% extends 'base.html' %}

{% block content %}
  {% for post in object_list %}
    <div class="post-entry">
      <h2><a href="{% url 'post_detail' post.pk %}">{{ post.title }}</a></h2>
      <p>{{ post.body }}</p>
    </div>
  {% endfor %}
{% endblock content %}
```
- Se empieza diciendo a la plantilla de Django que se quiere hacer referencia a una `URLConf` usando el código `{% url ... %}`
    +  ¿Qué URL?.- La que se llama `post_detail`, que es el nombre que se le dió a `BlogDetailView` en la `URLConf` hace un momento.
    +  Si se mira a `post_detail` en `URLConf`, se observa que espera que se le pase un argumento `pk` que representa la clave primaria para la entrada del blog.
    +  Afortunadamente, Django ya ha creado e incluido este campo `pk` en el objeto `post`.
    +  Se pasa a la `URLConf` añadiéndolo en la plantilla como `post.pk`.

## 6.9. Tests
FICHERO: `blog/tests.py`
```python
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        self.post = Post.objects.create(
            title='A good title',
            body='Nice body content',
            author=self.user,
        )
    
    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body content')
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice body content')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'post_detail.html')
```
- Hay muchas cosas nuevas en estas pruebas, así que se recorrerán lentamente.
- En la parte superior se importa `get_user_model` para referenciar al usuario activo.
- Se importa `TestCase` que se ha visto antes y también `Client()` que es nuevo y se usa como un navegador web falso para simular peticiones `GET` y `POST` en una `URL`. En otras palabras, siempre que se esté probando vistas se usará `Client()`.
- En el método de configuración se añade una entrada de blog de muestra para probar y luego se confirma que tanto la representación de la cadena como el contenido son correctos.
- Luego se usa `test_post_list_view` para confirmar que la página de inicio devuelve un código de estado *HTTP 200*, contiene el texto del cuerpo y usa la plantilla `home.html` correcta.
- Finalmente `test_post_detail_view` comprueba que la página de detalles funciona como se espera y que una página incorrecta devuelve un *404*.
- Siempre es bueno probar que algo existe y que algo incorrecto no existe en las pruebas.
```bash
(testy) $ python manage.py test
```
## 6.10. Git
- Ahora también es un buen momento para el primer *commit* de git. 
```bash
(testy) $ git init
(testy) $ git status
(testy) $ git add -A
(testy) $ git commit -m 'Commit Inicial'
```

## 6.11. Conclusión
- Se ha construido una aplicación básica de blog desde cero
- Usando el administrador de Django se puede crear, editar o borrar el contenido.
- Se ha usado `DetailView` por primera vez para crear una vista individual detallada de cada entrada del blog.



|\/| [- |\| ~|~ [- ( /\ ~|~ () ^/_ '|