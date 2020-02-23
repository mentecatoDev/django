# 14. Newspaper app

- Habrá una página de artículos en la que los periodistas podrán publicar artículos, establecer permisos para que sólo el autor de un artículo pueda editarlo o borrarlo, y finalmente añadir la posibilidad de que otros usuarios escriban comentarios en cada artículo, lo que introducirá el concepto de *claves externas*.

## 14.1. Articles app

- No hay reglas rígidas sobre cómo llamar a las aplicaciones, excepto que no se puede usar el nombre de una aplicación incorporada.
- Una regla general es usar el plural del nombre de una aplicación -`posts`, `payments`, `users`, etc.- a menos que hacerlo sea obviamente incorrecto como en el caso común de `blog` donde el singular tiene más sentido.
- Crear la aplicación para los nuevos artículos.

```
(news) $ python manage.py startapp articles
```

- Añadirla a `INSTALLED_APPS` y actualizar la zona horaria ya que se marcará la hora de los artículos.
- Para averiguar la zona horaria correspondiente:
```python
>>> from pytz import all_timezones, common_timezones
>>> 'Europe/Madrid' in all_timezones
True
```

FICHERO: `newspaper_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party
    'crispy_forms',
    
    # Local
    'users',
    'pages',
    'articles', # new
]
TIME_ZONE = 'Europe/Madrid'
```

- Se define el modelo de base de datos con cuatro campos: `title`, `body`, `date`, y `author`.
- Para el campo `autor` se hará referencia al modelo de usuario personalizado `users.CustomUser` que se ha establecido en el archivo `settings.py` como `AUTH_USER_MODEL`. Por lo tanto, si se importa la configuración podemos referirnos a ella como `settings.AUTH_USER_MODEL`.
- También se implementa la 'buena mejores práctica' de definir un `get_absolute_url` desde el principio y un método `__str__` para ver el modelo en la interfaz de administración.

FICHERO: `articles/models.py`
```python
from django.conf import settings
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

def __str__(self):
    return self.title

def get_absolute_url(self):
    return reverse('article_detail', args=[str(self.id)])
```

- Como se tiene una nueva aplicación y modelo, es hora de hacer un nuevo archivo de migración y luego aplicarlo a la base de datos.

```bash
(news) $ python manage.py makemigrations articles
(news) $ python manage.py migrate
```

- En este punto es conveniente ir a la administración para jugar con el modelo antes de construir las urls/vistas/plantillas necesarias para mostrar los datos en el sitio web. Pero primero necesitamos actualizar `admin.py` para que se muestre la nueva aplicación.

FICHERO: `articles/admin.py`
```python
from django.contrib import admin
from . import models


admin.site.register(models.Article)
```

- Iniciar el servidor, ir a la página de administración y añadir algunos artículos de ejemplo.
    - No se podrá añadir la fecha porque fue añadida automáticamente por Django en nuestro nombre y no puede ser cambiada en la administración.
    - Se podrá hacer que la fecha sea editable -en aplicaciones más complejas es común tener un campo `created_at` y `updated_at`- pero para mantener las cosas simples, por ahora sólo se tendrá `date` establecida por Django al momento de la creación.

## 14.2. URLs y Vistas
- Vamos a hacer que los artículos aparezcan en `articles/`.

FICHERO: `# newspaper_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path('', include('pages.urls')),
    path('articles/', include('articles.urls')), # new
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
```

FICHERO: `articles/urls.py`
```python
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
]
```
- Crear ahora la vista usando la genérica `ListView` de Django.

FICHERO: `# articles/views.py`
```python
from django.views.generic import ListView
from . import models


class ArticleListView(ListView):
    model = models.Article
    template_name = 'article_list.html'
```

- Los dos únicos campos que se necesitan especificar son el modelo de artículo y el nombre de la plantilla que será `article_list.html`.

- El último paso es crear la plantilla.

- Bootstrap tiene un componente incorporado llamado `Cards` que se puede personalizar para los artículos individuales. Recordar que `ListView` devuelve un objeto llamado object_list que se puede iterar con un bucle for.
- Dentro de cada artículo se muestra el título, el cuerpo, el autor y la fecha. Incluso se proporcionan enlaces a las funciones de "editar" y "borrar" que aún no se han construido.


FICHERO: `templates/article_list.html`
```html
{% extends 'base.html' %}

{% block title %}Articles{% endblock %}

{% block content %}
  {% for article in object_list %}
    <div class="card">
      <div class="card-header">
        <span class="font-weight-bold">{{ article.title }}</span> &middot;
        <span class="text-muted">by {{ article.author }} | {{ article.date }}</span>
      </div>
      <div class="card-body">
        {{ article.body }}
      </div>
      <div class="card-footer text-center text-muted">
        <a href="#">Edit</a> | <a href="#">Delete</a>
      </div>
    </div>
    <br />
  {% endfor %}
{% endblock content %}
```
- Arracar el servidor y consultar la página `articles/`

## 14.3. Editar/Borrar

- Se necesitan nuevas urls, vistas y plantillas.
- Se puede aprovechar el hecho de que Django añade automáticamente una clave primaria a cada base de datos. Por lo tanto, el primer artículo con una clave primaria de `1` estará en `articles/1/edit/` y la ruta de borrado estará en `articles/1/delete/`.


FICHERO: `articles/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('<int:pk>/edit/',views.ArticleUpdateView.as_view(), name='article_edit'),# new
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'), # new
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'), # new
]
```

- Ahora se escribirán las vistas que usarán las vistas genéricas basadas en clases de Django para `DetailView`, `UpdateView` y `DeleteView`. Especificamos qué campos pueden ser actualizados -`title` y `body`- y dónde redirigir al usuario después de borrar un artículo: `article_list`.

FICHERO: `articles/views.py`
```python
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from . import models


class ArticleListView(ListView):
    model = models.Article
    template_name = 'article_list.html'


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = 'article_detail.html'


class ArticleUpdateView(UpdateView):
    model = models.Article
    fields = ['title', 'body', ]
    template_name = 'article_edit.html'


class ArticleDeleteView(DeleteView):
    model = models.Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
```

- Finalmente se necesita añadir las nuevas plantillas.
- Se empezará con la página de detalles que mostrará el título, la fecha, el cuerpo y el autor con enlaces para editar y borrar. También enlazará hacia atrás con todos los artículos.
- El nombre de la ruta de edición es `article_edit` y tenemos que pasarle su clave principal `article.pk`.
- El nombre de la ruta de borrado es `article_delete` y también necesita una clave primaria `article.pk`.
- La página de artículos es una `ListView` por lo que no necesita que se le pase ningún argumento adicional.

FICHERO: `templates/article_detail.html`
```html
{% extends 'base.html' %}

{% block content %}
  <div class="article-entry">
    <h2>{{ object.title }}</h2>
      <p>by {{ object.author }} | {{ object.date }}</p>
      <p>{{ object.body }}</p>
  </div>
  <p><a href="{% url 'article_edit' article.pk %}">Edit</a> | <a href="{% url 'article_delete' article.pk %}">Delete</a></p>
  <p>Back to <a href="{% url 'article_list' %}">All Articles</a>.</p>
{% endblock content %}
```

- Para las páginas de edición y borrado se puede usar el estilo del botón de Bootstrap para hacer que el botón de edición sea azul claro y el de borrado rojo.

FICHERO: `templates/article_edit.html`
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Edit</h1>
  <form action="" method="post">{% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-info ml-2" type="submit">Update</button>
  </form>
{% endblock %}
```

FICHERO: `templates/article_delete.html`
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Delete</h1>
  <form action="" method="post">{% csrf_token %}
    <p>Are you sure you want to delete "{{ article.title }}"?</p>
    <button class="btn btn-danger ml- " type="submit">Confirm</button>
  </form>
{% endblock %}
```

- Como paso final se añaden los enlaces de edición y borrado a la página de listas en la clase `div` para el `card-foot`. Serán los mismos que los añadidos a la página detalle.

FICHERO: `templates/article_list.html`
```html
...
<div class="card-footer text-center text-muted">
  <a href="{% url 'article_edit' article.pk %}">Edit</a> |
  <a href="{% url 'article_delete' article.pk %}">Delete</a>
</div>
...
```

- Arrancar el servidor e ir a la página de `articles/` y pulsar sobre `Edit`.
- Si se actualiza el campo "título" y se hace clic en actualizar, el usuario será redirigido a la página de detalles que mostrará el nuevo cambio.
- Si se hace clic en el enlace `Delete` el usuario será redirigido a la página de borrado.
- Si se presiona el aterrador botón rojo `Confirm` el usuario será redirigido a la página de artículos donde ahora habrá una entrada menos.





00000000000000000000000000000000000000000000000000000000000000000000000000000





## 14.Crear la page

El paso final es una página de creación de nuevos artículos que podemos hacer con el CreateView de Django. Nuestros tres pasos son crear una vista, una url y una plantilla. Este flujo ya debería resultar bastante familiar. En nuestro archivo de vistas agregamos CreateView a las importaciones de la parte superior y hacemos una nueva clase ArticleCreateView que especifica nuestro modelo, plantilla y los campos disponibles.

FICHERO: `articles/views.py`
```python
...
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class ArticleCreateView(CreateView):
    model = models.Article
    template_name = 'article_new.html'
    fields = ['title', 'body', 'author',]
...
```
Nótese que nuestros campos tienen autor ya que queremos asociar un nuevo artículo con un autor, sin embargo una vez que un artículo ha sido creado no queremos que un usuario pueda cambiar el autor, por lo que ArticleUpdateView sólo tiene los campos ['title', 'body',] .
Actualizar nuestro archivo de urls con la nueva ruta para la vista.

FICHERO: `articles/urls.py`
```python
...
urlpatterns = [
    ...
    path('new/', views.ArticleCreateView.as_view(), name='article_new'),
    ...
]
```

Luego, salga del servidor Control+c para crear una nueva plantilla llamada article_new.html .

```
(news) $ touch templates/article_new.html
```

Y actualizarlo con el siguiente código HTML.

FICHERO: `templates/article_new.html`
```
{% extends 'base.html' %}
{% block content %}
<h1>New article</h1>
<form action="" method="post">{% csrf_token %}
{{ form.as_p }}
<button class="btn btn-success ml- " type="submit">Save</button>
</form>
{% endblock %}
```

Como paso final deberíamos añadir un enlace para crear nuevos artículos en nuestro navegador para que sea accesible en todas partes del sitio para los usuarios registrados.

FICHERO: `templates/base.html`
```
...
<body>
<nav class="navbar navbar-expand-md navbar-dark bg-dark mb- ">
<a class="navbar-brand" href="{% url 'home' %}">Newspaper</a>
{% if user.is_authenticated %}
<ul class="navbar-nav mr-auto">
<li class="nav-item"><a href="{% url 'article_new' %}">+ New</a></li>
</ul>
{% endif %}
<button class="navbar-toggler" type="button" data-toggle="collapse" data-tar\
get="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-\
label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
...
```

¿Y por qué no usar Bootstrap para mejorar nuestra página web original ahora también? Podemos actualizar plantillas/home.html como sigue.

FICHERO: `templates/home.html`
```
{% extends 'base.html' %}
{% block title %}Home{% endblock %}
{% block content %}
<div class="jumbotron">
<h1 class="display- ">Newspaper app</h1>
<p class="lead">A Newspaper website built with Django.</p>
<p class="lead">
<a class="btn btn-primary btn-lg" href="{% url 'article_list' %}" role="butt\
on">View All Articles</a>
</p>
</div>
{% endblock %}
```

Ya hemos terminado. Vamos a confirmar que todo funciona como se esperaba. Arranca el servidor de nuevo python manage.py runserver y navega a nuestra página web en: http://127.0.0.1:8000/.273

Página principal con nuevo enlace en la navegación
Haz clic en el enlace "+ Nuevo" en la parte superior del navegador y serás redirigido a nuestra página de creación.

Crear página
Adelante, crea un nuevo artículo. Luego haz clic en el botón "Guardar". Serás redirigido a la página de detalles. ¿Por qué? Porque en nuestro archivo models.py establecemos el método get_-absolute_url en article_detail . Este es un buen enfoque porque si más tarde cambiamos el patrón de url de la página de detalles a, digamos, artículos/detalles/ / , la redirección seguirá funcionando. Se utilizará cualquier ruta asociada a article_detail; no hay código duro de la ruta en sí.

Página de detalles
Tengan en cuenta también que la clave principal aquí está en el URL. Aunque sólo estamos mostrando tres artículos ahora mismo, Django no reordena las claves primarias sólo porque hayamos borrado una. En la práctica, la mayoría de los sitios del mundo real no borran nada; en su lugar, "ocultan" los campos borrados, ya que esto facilita el mantenimiento de la integridad de una base de datos y da la opción de "recuperar" más adelante si es necesario. Con nuestro enfoque actual, una vez que algo se borra, ¡se va para siempre!
Haga clic en el enlace de "Todos los artículos" para ver nuestra nueva página de artículos.

Página de artículos actualizada
Hay un nuevo artículo en la parte inferior como se esperaba.
## Conclusión...
Hemos creado una aplicación de artículos dedicados con la funcionalidad de CRUD. Pero aún no hay permisos o autorizaciones, lo que significa que cualquiera puede hacer cualquier cosa. Un usuario desconectado puede visitar todas las URLs y cualquier usuario conectado puede editar o eliminar un artículo existente, ¡incluso uno que no sea suyo! En el próximo capítulo añadiremos permisos y autorizaciones a nuestro proyecto para arreglar esto.