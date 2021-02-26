# 14. Newspaper app

Habrá una página de artículos en la que los periodistas podrán publicar, establecer permisos para que sólo el autor de un artículo pueda editarlo o borrarlo, y finalmente añadir la posibilidad de que otros usuarios escriban comentarios en cada uno de ellos, lo que introducirá el concepto de *claves externas*.

## 14.1. Articles app

- No hay reglas rígidas sobre cómo llamar a las aplicaciones, excepto que no se puede usar el nombre de una aplicación incorporada.
- Una regla general es usar el plural del nombre de una aplicación -`posts`, `payments`, `users`, etc.- a menos que hacerlo sea obviamente incorrecto como en el caso común de `blog` donde el singular tiene más sentido.
- Crear la aplicación para los nuevos artículos.

```bash
(news) $ python manage.py startapp articles
```

- Añadirla a `INSTALLED_APPS` y actualizar la [zona horaria](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) ya que se marcará la hora de los artículos.
- Para averiguar la zona horaria correspondiente:
```python
>>> from pytz import all_timezones, common_timezones
>>> 'Europe/Madrid' in all_timezones
True
```

FICHERO: `newspaper_project/settings.py`
```python
`...`

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
    'accounts.apps.AccountsConfig',
    'pages.apps.PagesConfig',
<<<<<<< HEAD
    'articles.apps.ArticlesConfig',  # new
=======
    'articles.apps.ArticlesConfig', # new
>>>>>>> d877e94a4f92a03bbffd8a7162f3c622dfcefaec
]

`...`

TIME_ZONE = 'Europe/Madrid'
```

- Se define el modelo de base de datos con cuatro campos: `title`, `body`, `date`, y `author`.
- Para el campo `autor` se hará referencia al modelo de usuario personalizado `accounts.CustomUser` que se ha establecido en el archivo `settings.py` como `AUTH_USER_MODEL`. Por lo tanto, si se importa la configuración podemos referirnos a ella como `settings.AUTH_USER_MODEL` o bien usando el método `get_user_model`. 
- También implementamos práctica recomendada de definir un método `get_absolute_url` desde el principio y un método `__str__` para ver el modelo en nuestra interfaz de administración.

FICHERO: `articles/models.py`
```python
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    body = models.TextField(verbose_name='Cuerpo')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    author = models.ForeignKey(
        get_user_model(),    					  # ó settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Autor'
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
from .models import Article


admin.site.register(Article)
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
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('articles/', include('articles.urls')), 			# new
    path('', include('pages.urls')),
<<<<<<< HEAD
=======

>>>>>>> d877e94a4f92a03bbffd8a7162f3c622dfcefaec
]
```

FICHERO: `articles/urls.py`
```python
from django.urls import path
from .views import ArticleListView


urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
]
```
- Crear ahora la vista usando la genérica `ListView` de Django.

FICHERO: `# articles/views.py`
```python
from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    model = Article
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
        <span class="text-muted">por {{ article.author }} | {{ article.date }}</span>
      </div>
      <div class="card-body">
        {{ article.body }}
      </div>
      <div class="card-footer text-center text-muted">
        <a href="#">Editar</a> | <a href="#">Borrar</a>
      </div>
    </div>
    <br />
  {% endfor %}
{% endblock content %}
```
- Arracar el servidor y consultar la página `articles/`
- Para más información de personalización consultar el siguiente [enlace](https://docs.djangoproject.com/es/3.1/howto/custom-template-tags/)



## 14.3. Editar/Borrar

- Se necesitan nuevas urls, vistas y plantillas.
- Se puede aprovechar el hecho de que Django añade automáticamente una clave primaria a cada base de datos. Por lo tanto, el primer artículo con una clave primaria de `1` estará en `articles/1/edit/` y la ruta de borrado estará en `articles/1/delete/`.


FICHERO: `articles/urls.py`
```python
from django.urls import path
<<<<<<< HEAD
from .views import (
=======
from .views import(
>>>>>>> d877e94a4f92a03bbffd8a7162f3c622dfcefaec
    ArticleListView,
    ArticleUpdateView, # new
    ArticleDetailView, # new
    ArticleDeleteView, # new
)

urlpatterns = [
<<<<<<< HEAD
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),	 # new
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'), 		 # new
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),# new
=======
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),# new
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'), # new
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'), # new
>>>>>>> d877e94a4f92a03bbffd8a7162f3c622dfcefaec
    path('', ArticleListView.as_view(), name='article_list'),
]
```

- Ahora se escribirán las vistas que usarán las vistas genéricas basadas en clases de Django para `DetailView`, `UpdateView` y `DeleteView`. Especificamos qué campos pueden ser actualizados -`title` y `body`- y dónde redirigir al usuario después de borrar un artículo: `article_list`.

FICHERO: `articles/views.py`
```python
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'


<<<<<<< HEAD
class ArticleUpdateView(UpdateView):{% extends 'base.html' %}

{% block content %}
  <div class="article-entry">
    <h2>{{ object.title }}</h2>
      <p>por {{ object.author }} | {{ object.date }}</p>
      <p>{{ object.body }}</p>
  </div>
  <p><a href="{% url 'article_edit' article.pk %}">Editar</a> | <a href="{% url 'article_delete' article.pk %}">Borrar</a></p>
  <p>Back to <a href="{% url 'article_list' %}">Todos los artículos</a>.</p>
{% endblock content %}
    model = Article
    fields = ('title', 'body', )
=======
class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'body', ]
>>>>>>> d877e94a4f92a03bbffd8a7162f3c622dfcefaec
    template_name = 'article_edit.html'


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
```

- Finalmente se necesita añadir las nuevas plantillas.

```bash
(news) $ touch templates/article_detail.html
(news) $ touch templates/article_edit.html
(news) $ touch templates/article_delete.html
```
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
      <p>por {{ object.author }} | {{ object.date }}</p>
      <p>{{ object.body }}</p>
  </div>
  <p><a href="{% url 'article_edit' article.pk %}">Editar</a> | <a href="{% url 'article_delete' article.pk %}">Borrar</a></p>
<<<<<<< HEAD
  <p>Volver a la <a href="{% url 'article_list' %}">lista de artículos</a>.</p>
=======
  <p>Back to <a href="{% url 'article_list' %}">Todos los artículos</a>.</p>
>>>>>>> d877e94a4f92a03bbffd8a7162f3c622dfcefaec
{% endblock content %}
```

- Para las páginas de edición y borrado se puede usar el estilo del botón de Bootstrap para hacer que el botón de edición sea azul claro y el de borrado rojo.

FICHERO: `templates/article_edit.html`
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Editar</h1>
  <form action="" method="post">{% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-info ml-2" type="submit">Actualizar</button>
  </form>
{% endblock %}
```

FICHERO: `templates/article_delete.html`
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Borrar</h1>
  <form action="" method="post">{% csrf_token %}
    <p>¿Estás seguro de que quieres borrar "{{ article.title }}"?</p>
    <button class="btn btn-danger ml- " type="submit">Confirmar</button>
  </form>
{% endblock %}
```

- Como paso final se añaden los enlaces de edición y borrado a la página de listas en la clase `div` para el `card-foot`. Serán los mismos que los añadidos a la página detalle.

FICHERO: `templates/article_list.html`
```html
...
<div class="card-footer text-center text-muted">
  <a href="{% url 'article_edit' article.pk %}">Editar</a> |
  <a href="{% url 'article_delete' article.pk %}">Borrar</a>
</div>
...
```

- Arrancar el servidor e ir a la página de `articles/` y pulsar sobre `Edit`.
- Si se actualiza el campo "título" y se hace clic en actualizar, el usuario será redirigido a la página de detalles que mostrará el nuevo cambio.
- Si se hace clic en el enlace `Delete` el usuario será redirigido a la página de borrado.
- Si se presiona el aterrador botón rojo `Confirm` el usuario será redirigido a la página de artículos donde ahora habrá una entrada menos.



## 14.Crear Page

El paso final es una página de creación de nuevos artículos que podemos hacer con el `CreateView` de Django. Nuestros tres pasos son crear una vista, una url y una plantilla. Este flujo ya debería resultar bastante familiar. En nuestro archivo de vistas agregamos `CreateView` a las importaciones de la parte superior y hacemos una nueva clase `ArticleCreateView` que especifica nuestro modelo, plantilla y los campos disponibles.

FICHERO: `articles/views.py`
```python
`...`
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
`...`
class ArticleCreateView(CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title', 'body', 'author',)
```
Nótese que nuestros campos tienen autor ya que queremos asociar un nuevo artículo con un autor, sin embargo una vez que un artículo ha sido creado no queremos que un usuario pueda cambiar el autor, por lo que ArticleUpdateView sólo tiene los campos ['title', 'body',] .
Actualizar nuestro archivo de urls con la nueva ruta para la vista.

FICHERO: `articles/urls.py`
```python
from django.urls import path
from .views import (
    ArticleListView,
    ArticleUpdateView,
    ArticleDetailView,
    ArticleDeleteView,
    ArticleCreateView, # new
)
urlpatterns = [
    path('<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/',ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'), # new
    path('', ArticleListView.as_view(), name='article_list'),
]
```

Luego, salga del servidor Control+c para crear una nueva plantilla llamada `article_new.html`.

```
(news) $ touch templates/article_new.html
```

Y actualizarlo con el siguiente código HTML.

FICHERO: `templates/article_new.html`
```html
{% extends 'base.html' %}

{% block content %}
	<h1>Nuevo artículo</h1>
	<form action="" method="post">{% csrf_token %}
		{{ form.as_p }}
		<button class="btn btn-success ml- " type="submit">Guardar</button>
	</form>
{% endblock content %}
```

Como paso final deberíamos añadir un enlace para crear nuevos artículos en nuestro navegador para que sea accesible en todas partes del sitio para los usuarios registrados.

FICHERO: `templates/base.html`
```html
<body>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="{% url 'home' %}">Newspaper</a>
    {% if user.is_authenticated %}
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a href="{% url 'article_new' %}">+ Nuevo</a>
        </li>
      </ul>
    {% endif %}
`...`
```

¿Y por qué no usar Bootstrap para mejorar nuestra página web original ahora también? Podemos actualizar `templates/home.html` como sigue.

FICHERO: `templates/home.html`
```html
{% extends 'base.html' %}

{% block title %}Home{% endblock title %}

{% block content %}
  <br/>
  <div class="jumbotron">
    <h1 class="display-4">Newspaper app</h1>
    <p class="lead">Un Periódico con Django.</p>
    <p class="lead">
      <a class="btn btn-primary btn-lg" href="{% url 'article_list' %}"
      role="button">Ver los artículos</a>
    </p>
  </div>
{% endblock content %}
```

Ya hemos terminado. Vamos a confirmar que todo funciona como se esperaba. Arranca el servidor de nuevo `python manage.py runserver` y navega a nuestra página web en: http://127.0.0.1:8000/.

Haz clic en el enlace "+ Nuevo" en la parte superior del navegador y serás redirigido a nuestra página de creación.

Adelante, crea un nuevo artículo. Luego haz clic en el botón "Guardar". Serás redirigido a la página de detalles. ¿Por qué? Porque en nuestro archivo `models.py` establecemos el método `get_absolute_url` en `article_detail`. Este es un buen enfoque porque si más tarde cambiamos el patrón de url de la página de detalles a, digamos, `articles/details/4/` , la redirección seguirá funcionando. Se utilizará cualquier ruta asociada a `article_detail`; no hay código duro para la ruta en sí misma.

Ten en cuenta también que la clave principal aquí está en el URL. Aunque sólo estamos mostrando tres artículos ahora mismo, Django no reordena las claves primarias sólo porque hayamos borrado una. En la práctica, la mayoría de los sitios del mundo real no borran nada; en su lugar, "ocultan" los campos borrados, ya que esto facilita el mantenimiento de la integridad de una base de datos y da la opción de "recuperar" más adelante si es necesario. Con nuestro enfoque actual, una vez que algo se borra, ¡se va para siempre!
Haga clic en el enlace de "Todos los artículos" para ver nuestra nueva página de artículos.

Hay un nuevo artículo en la parte inferior, como se esperaba.
## Conclusión...
Hemos creado una aplicación de artículos dedicados con la funcionalidad de CRUD. Pero aún no hay permisos o autorizaciones, lo que significa que cualquiera puede hacer cualquier cosa. Un usuario desconectado puede visitar todas las URLs y cualquier usuario conectado puede editar o eliminar un artículo existente, ¡incluso uno que no sea suyo! En el próximo capítulo añadiremos permisos y autorizaciones a nuestro proyecto para arreglar esto.

