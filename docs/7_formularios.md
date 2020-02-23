# 7. Formularios

- Se va a seguir trabajando sobre la aplicación Blog añadiendo Formularios para poder crear, editar o borrar cualquiera de las entradas.

## 7.1 Formularios

- Los formularios son muy comunes y difíciles de implementar correctamente.
- Cada vez que se acepta la entrada de un usuario hay preocupaciones de:
    + Seguridad (Ataques XSS)
    + Se requiere un manejo adecuado de los errores
    + Hay consideraciones de UI sobre cómo alertar al usuario de problemas con el formulario.
    + Sin mencionar la necesidad de redireccionarlo en caso de éxito.
- Afortunadamente, los formularios incorporados de Django abstraen gran parte de la dificultad y proporcionan un rico conjunto de herramientas para manejar los casos de uso común que trabajan con los formularios.

- Actualizar la plantilla base para mostrar un enlace a una página donde introducir nuevas entradas en el blog. Tomará la forma `<a href="{% url 'post_new' %}"><a/>` donde `post_new` es el nombre de la URL.

FICHERO: `templates/base.html`
```html
{% load static %}
<html>
  <head>
    <title>Django blog</title>
    <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/base.css' %}">
  </head>
  <body>
    <div class="container">
      <header>
        <div class="nav-left">
          <h1><a href="/">Django blog</a></h1>
        </div>
        <div class="nav-right">
          <a href="{% url 'post_new' %}">+ New Blog Post</a>
        </div>
      </header>
      {% block content %}
      {% endblock content %}
    </div>
  </body>
</html>
```

FICHERO: `blog/urls.py`
```python
from django.urls import path
from . import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
    path('post/new/', views.BlogCreateView.as_view(), name='post_new'),
]
```
- La url empezará con `post/new/`, la vista se llama `BlogCreateView`, y la url se llamará `post_new`.
- Crear la vista importando una nueva clase genérica llamada `CreateView` y luego heredarla para crear una nueva vista llamada `BlogCreateView`.

FICHERO: `blog/views.py`
```python
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from . models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'
```
- Dentro de `BlogCreateView` se especifica el modelo de base de datos `Post`, el nombre de la plantilla `post_new.html`, y todos los campos con `'__all__'` ya que sólo hay dos: `title` y `author`.
- El último paso es crear la plantilla, que llamaremos `post_new.html`.
```
(blog) $ touch templates/post_new.html
```

FICHERO: `templates/post_new.html`
```
{% extends 'base.html' %}

{% block content %}
    <h1>New post</h1>
    <form action="" method="post">{% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Save" />
    </form>
{% endblock %}
```
- En la línea superior se hereda la plantilla base.
- Se usan etiquetas HTML `<form>` con el método POST ya que se está enviando datos. Si se reciben datos de un formulario, por ejemplo en un cuadro de búsqueda, se utilizaría GET.
- Se añade un `{% csrf_token %}` que proporciona Django para proteger al formulario de ataques de cross-site scripting. Se debe usar en todos los formularios de Django.
- Luego para obtener los datos del formulario se usa `{{ form.as_p }}` que lo renderiza dentro etiquetas de párrafo `<p>`.
- Por último, se especifica un `input type="submit"` con el valor "Save".
- Iniciar el servidor con `python manage.py runserver` e ir a la página web en http://127.0.0.1:8000

- Hacer clic en el enlace para "+ New Blog Post" que le redirigirá a:
  http://127.0.0.1:8000/post/new/.
- Crear una nueva entrada de blog.
- ¡Ups! ¿Qué ha pasado?
  + El mensaje de error de Django se queja de que no se especificó dónde enviar al usuario después de haber enviado el formulario con éxito.
  + Se enviará al usuario a la página de detalles después de haber tenido éxito; así se podrá ver el mensaje completo.
  + Se puede seguir la sugerencia de Django y añadir un `get_absolute_url` al modelo. Esta es una buena práctica que siempre se debe hacer. Establecer una URL canónica para un objeto, de modo que aunque la estructura de las URL cambie en el futuro, la referencia al objeto específico sea la misma.
  +  En resumen, se debería añadir un método `get_absolute_url()` y `__str__()` a cada modelo que se escriba.

FICHERO: `blog/models.py`
```
    from django.db import models
ç   from django.urls import reverse


    class Post(models.Model):
        title = models.CharField(max_length=200)
        author = models.ForeignKey(
            'auth.User',
            on_delete=models.CASCADE,
        )
        body = models.TextField()

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('post_detail', args=[str(self.id)])
```

- `reverse` es una función muy útil que Django proporciona para referir a un objeto por el nombre de plantilla URL, en este caso `post_detail`.
```
path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
```
- Eso significa que para que esta ruta funcione debemos pasar también como argumento la `pk` o clave primaria del objeto. A pesar de que `pk` e `id` son intercambiables en Django, la documentación de Django recomienda usar `self.id` con `get_absolute_url`.
  + Así le decimos a Django que la última ubicación de una entrada de un Post es su vista `post_detail` que es `posts/<int:pk>/` por lo que la ruta para la primera entrada que hemos hecho estará en `posts/1`.
- Intentar crear una nueva entrada en el blog de nuevo en http://127.0.0.1:8000/post/new/ y se tendrá éxito al ser redirigido a la página de vista detallada donde aparece el post.
- También se notará que la entrada anterior en el blog también está ahí. Fue enviada con éxito a la base de datos pero Django no supo cómo redirigirse después de eso.
- Aunque se podría entrar en el administrador de Django para borrar los mensajes no deseados, es mejor añadir formularios para que un usuario pueda actualizar y eliminar los mensajes existentes directamente desde el sitio.

## 7.2 Actualizar Formularios

- Para empezar, se añade un nuevo enlace a `post_detail.html` para que la opción de editar una entrada de blog aparezca en una página de blog individual.

> Nota.- Si se sigue usando el contexto de la vista tal y como se dejó al final del tema previo, se tendrá el contexto `anything_you_want` que habrá que eliminar para volver a usar los habituales `object`y `post`.

FICHERO: `templates/post_detail.html`
```html
{% extends 'base.html' %}

{% block content %}
  <div class="post-entry">
    <h2>{{ object.title }}</h2>
    <p>{{ object.body }}</p>
  </div>

  <a href="{% url 'post_edit' post.pk %}">+ Edit Blog Post</a>
{% endblock content %}
```
- Se ha  añadido un enlace usando `<a href>...</a>` y la etiqueta del motor de plantillas de Django `{% url... %}`. Dentro de ella se ha especificado el nombre del objetivo de la url, que se llamará `post_edit`, y también se ha pasado el parámetro necesario, que es la clave principal del post `post.pk`.
- A continuación se crea la plantilla para la página de edición llamada `post_edit.html`.

FICHERO: `templates/post_edit.html`
```python
{% extends 'base.html' %}

{% block content %}
  <h1>Edit post</h1>
  <form action="" method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Update" />
  </form>
{% endblock %}
```
- De nuevo se usan las etiquetas HTML `<form></form>`, el `csrf_token` de Django por seguridad, el `form.as_p` para mostrar los campos de formulario con etiquetas de párrafo, y finalmente se le da el valor "Update" en el botón *submit*.
- Ahora a nuestra vista. Necesitamos importar `UpdateView` en la segunda línea superior y luego heredarla en nuestra nueva vista `BlogUpdateView`.
FICHERO: `blog/views.py`
```python
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from . models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'


class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'post_edit.html'
```
- Nótese que en `BlogUpdateView` se listan explícitamente los campos que se quieren usar `['title', 'body']` en lugar de usar `'__all__'`. Esto se debe a que se asume que el autor del post no cambia; sólo se quiere que el título y el texto sean editables.
- El último paso es actualizar el archivo `urls.py` de la siguiente manera:

FICHERO: `blog/urls.py`
```python
from django.urls import path
from . import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
    path('post/new/', views.BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/',views.BlogUpdateView.as_view(), name='post_edit'),
]
```
- En la parte superior se agrega la vista `BlogUpdateView` a la lista de vistas importadas, luego se creará un nuevo patrón de url para `/post/pk/edit` y se le dará el nombre `post_edit`.
- Ahora, si se hace click en una entrada del blog, se verá el nuevo botón *Editar*.
- Si se hace clic en *"+ Edit Blog Post"* se redirigirá a http://127.0.0.1:8000/post/1/edit/
si esa es la primera entrada en el blog.
- Tengase en cuenta que el formulario está precargado con los datos existentes en la base de datos para el post.
-  Vamos a hacer un cambio...

- Y después de pulsar el botón "Update" somos redirigidos a la vista de detalles del *post* en el que se puede ver el cambio. Esto se debe a la configuración `get_absolute_url`.
- Si se navega a la página principal se podrás ver el cambio junto a todas las demás entradas.

## 7.3 Borrar la vista

- El proceso de creación de un formulario para borrar entradas del blog es muy similar al de la actualización de un post.
- Se usará otra vista genérica basada en clases, `DeleteView`, y se necesita crear una vista, una url y una plantilla para la funcionalidad.
- Se comenzará por agregar un enlace para eliminar los post del blog en la página de blog individual, `post_detail.html`.

FICHERO: `templates/post_detail.html`
```python
{% extends 'base.html' %}

{% block content %}
  <div class="post-entry">
    <h2>{{ object.title }}</h2>
    <p>{{ object.body }}</p>
  </div>

  <p><a href="{% url 'post_edit' post.pk %}">+ Edit Blog Post</a></p>
  <p><a href="{% url 'post_delete' post.pk %}">+ Delete Blog Post</a></p>
{% endblock content %}
```
- A continuación, se crea un nuevo archivo para la plantilla de la página de borrado.

FICHERO: `templates/post_delete.html`
```
{% extends 'base.html' %}

{% block content %}
  <h1>Delete post</h1>
  <form action="" method="post">{% csrf_token %}
    <p>Are you sure you want to delete "{{ post.title }}"?</p>
    <input type="submit" value="Confirm" />
  </form>
{% endblock %}
```
> Nota: se usa `post.title` para mostrar el título de la entrada en el blog. También se podría usar `object.title` ya que también lo proporciona `DetailView`.
- Ahora se actualiza el archivo `views.py`, importando `DeleteView` y `reverse_lazy` en la parte superior, y luego creamos una nueva vista que hereda de `DeleteView`.

FICHERO: `blog/views.py`
```python
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . models import Post


class BlogListView(ListView):
    model = PostChapter
    template_name = 'home.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = '__all__'


class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'post_edit.html'


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
```
- Se usa `reverse_lazy` en vez de sólo `reverse` para que no ejecute la redirección URL hasta que la vista haya terminado de borrar la entrada del blog.

  

- Finalmente agregar una url importando la vista `BlogDeleteView` y agregando un nuevo patrón:

FICHERO: `blog/urls.py`
```python
from django.urls import path
from . import views
urlpatterns = [
path('', views.BlogListView.as_view(), name='home'),
path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
path('post/new/', views.BlogCreateView.as_view(), name='post_new'),
path('post/<int:pk>/edit/',
views.BlogUpdateView.as_view(), name='post_edit'),
path('post/<int:pk>/delete/',
views.BlogDeleteView.as_view(), name='post_delete'),
]
```

## 7.4 Tests
- Se ha añadido un método `get_absolute_url` al modelo y nuevas vistas para crear, actualizar y editar entradas. Eso significa que se necesitan cuatro nuevas pruebas:
  + def test_get_absolute_url
  + def test_post_create_view
  + def test_post_update_view
  + def test_post_delete_view

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

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), '/post/1/')
 
    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated text',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)
```
- Se espera que la url de la prueba esté en `post/1/` ya que sólo hay un post y el `1` es la clave primaria que Django añade automáticamente. Para testar la creación de la vista se crea una nueva respuesta y luego se asegura que se pase la respuesta (código de estado 200) y contenga nuestro el título y texto del cuerpo.
- Para actualizar la vista, se accede al primer post que tiene un `pk` de `1` que se pasa como único argumento y confirmamos que resulta en una redirección 302.
- Finalmente se prueba la vista de borrado confirmando que si eliminamos un post el código de estado es 200 para que sea exitoso.
- Siempre hay más pruebas que pueden ser añadidas, pero esto al menos da cobertura a todas las nuevas funcionalidades.

## 7.5 Conclusión
- En una pequeña cantidad de código se ha construido una aplicación de blog que permite crear, leer, actualizar y borrar entradas de blog. Esta funcionalidad básica se conoce por el acrónimo CRUD: Create-Read-Update-Delete. Aunque hay múltiples maneras de lograr esta misma funcionalidad -se podría haber usado vistas basadas en funciones o haber escrito unas vistas propias basadas en clases- se ha demostrado lo poco de código que se necesita en Django para que esto suceda.