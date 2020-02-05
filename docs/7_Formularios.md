# 7. Formularios
In this chapter we’ll continue working on our blog application from Chapter 5 by
adding forms so a user can create, edit, or delete any of their blog entries.
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
{% load staticfiles %}
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
- Crear la vista importando una nueva clase genérica llamada `CreateView` y luego
heredarla para crear una nueva vista llamada `BlogCreateView`.

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
- Iniciar el servidor con `python manage.py runserver` e ir a la página web en http://127.0.0.1:8000/.132















Página de inicio con el botón Nuevo
Haga clic en nuestro enlace para "+ Nueva entrada de blog" que le redirigirá a:
http://127.0.0.1:8000/post/new/.133

Blog new page
Go ahead and try to create a new blog post and submit it.134
Chapter 6: Forms
Blog new page
Oops! What happened?135
Chapter 6: Forms
Blog new page

Django’s error message is quite helpful. It’s complaining that we did not specify where
to send the user after successfully submitting the form. Let’s send a user to the detail
page after success; that way they can see their completed post.
We can follow Django’s suggestion and add a get_absolute_url to our model. This is a
best practice that you should always do. It sets a canonical URL for an object so even if
the structure of your URLs changes in the future, the reference to the specific object
is the same. In short, you should add a get_absolute_url() and __str__() method to
each model you write.

Open the models.py file. Add an import on the second line for reverse and a new get_-
absolute_url method.
Command Line
FICHERO: `blog/models.py`
```
from django.db import models
from django.urls import reverse
class Post(models.Model):
title = models.CharField(max_length=
)
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

Reverse is a very handy utility function Django provides us to reference an object by
its URL template name, in this case post_detail . If you recall our URL pattern it is the
following:137

Code
path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
That means in order for this route to work we must also pass in an argument with the
pk or primary key of the object. Confusingly pk and id are interchangeable in Django
though the Django docs recommend using self.id with get_absolute_url . So we’re
telling Django that the ultimate location of a Post entry is its post_detail view which
is posts/<int:pk>/ so the route for the first entry we’ve made will be at posts/ .
Try to create a new blog post again at http://127.0.0.1:8000/post/new/ and you’ll find
upon success you are redirected to the detailed view page where the post appears.
Blog new page with input
You’ll also notice that our earlier blog post is also there. It was successfully sent to the
database, but Django didn’t know how to redirect us after that.
Blog homepage with four posts
While we could go into the Django admin to delete unwanted posts, it’s better if we
add forms so a user can update and delete existing posts directly from the site.

## Update Form
The process for creating an update form so users can edit blog posts should feel
familiar. We’ll again use a built-in Django class-based generic view, UpdateView, and
create the requisite template, url, and view.
To start, let’s add a new link to post_detail.html so that the option to edit a blog post
appears on an individual blog page.

FICHERO: `templates/post_detail.html`
```
{% extends 'base.html' %}
{% block content %}
<div class="post-entry">
<h2>{{ object.title }}</h2>
<p>{{ object.body }}</p>
</div>
<a href="{% url 'post_edit' post.pk %}">+ Edit Blog Post</a>
{% endblock content %}
```
We’ve added a link using <a href>...</a> and the Django template engine’s {% url
... %} tag. Within it we’ve specified the target name of our url, which will be called
post_edit and also passed the parameter needed, which is the primary key of the post
post.pk .
Next we create the template for our edit page called post_edit.html .
Command Line
(blog) $ touch templates/post_edit.html
And add the following code:
FICHERO: `templates/post_edit.html`
```
{% extends 'base.html' %}
{% block content %}
<h1>Edit post</h1>
<form action="" method="post">{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Update" />
</form>
{% endblock %}
```
We again use HTML <form></form> tags, Django’s csrf_token for security, form.as_p
to display our form fields with paragraph tags, and finally give it the value “Update”
on the submit button.
Now to our view. We need to import UpdateView on the second-from-the-top line and
then subclass it in our new view BlogUpdateView .
FICHERO: `blog/views.py`
```
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
Notice that in BlogUpdateView we are explicitly listing the fields we want to use
['title', 'body'] rather than using '__all__' . This is because we assume that the
author of the post is not changing; we only want the title and text to be editable.
The final step is to update our urls.py file as follows:142
Chapter 6: Forms
Code
# blog/urls.py
from django.urls import path
from . import views
urlpatterns = [
path('', views.BlogListView.as_view(), name='home'),
path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post_detail'),
path('post/new/', views.BlogCreateView.as_view(), name='post_new'),
path('post/<int:pk>/edit/',
views.BlogUpdateView.as_view(), name='post_edit'),
]
At the top we add our view BlogUpdateView to the list of imported views, then created
a new url pattern for /post/pk/edit and given it the name post_edit .
Now if you click on a blog entry you’ll see our new Edit button.
Blog page with edit button143
Chapter 6: Forms
If you click on “+ Edit Blog Post” you’ll be redirected to http://127.0.0.1:8000/post/1/edit/
if it’s your first blog post.
Blog edit page
Note that the form is pre-filled with our database’s existing data for the post. Let’s
make a change...144
Chapter 6: Forms
Blog edit page
And after clicking the “Update” button we are redirected to the detail view of the
post where you can see the change. This is because of our get_absolute_url setting.
Navigate to the homepage and you can see the change next to all the other entries.145
Chapter 6: Forms
Blog homepage with edited post
Delete View
The process for creating a form to delete blog posts is very similar to that for updating
a post. We’ll use yet another generic class-based view, DeleteView, to help and need
to create a view, url, and template for the functionality.
Let’s start by adding a link to delete blog posts on our individual blog page, post_-
detail.html .Chapter 6: Forms
146
Code
<!-- templates/post_detail.html -->
{% extends 'base.html' %}
{% block content %}
<div class="post-entry">
<h2>{{ object.title }}</h2>
<p>{{ object.body }}</p>
</div>
<p><a href="{% url 'post_edit' post.pk %}">+ Edit Blog Post</a></p>
<p><a href="{% url 'post_delete' post.pk %}">+ Delete Blog Post</a></p>
{% endblock content %}
Then create a new file for our delete page template. First quit the local server Control-
c and then type the following command:
Command Line
(blog) $ touch templates/post_delete.html
And fill it with this code:Chapter 6: Forms
147
Code
<!-- templates/post_delete.html -->
{% extends 'base.html' %}
{% block content %}
<h1>Delete post</h1>
<form action="" method="post">{% csrf_token %}
<p>Are you sure you want to delete "{{ post.title }}"?</p>
<input type="submit" value="Confirm" />
</form>
{% endblock %}
Note we are using post.title here to display the title of our blog post. We could also
just use object.title as it too is provided by DetailView .
Now update our views.py file, by importing DeleteView and reverse_lazy at the top,
then create a new view that subclasses DeleteView .
Code
# blog/views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . models import Post
class BlogListView(ListView):
model = PostChapter 6: Forms
148
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
We use reverse_lazy as opposed to just reverse so that it won’t execute the URL
redirect until our view has finished deleting the blog post.
Finally add a url by importing our view BlogDeleteView and adding a new pattern:Chapter 6: Forms
149
Code
# blog/urls.py
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
If you start the server again python manage.py runserver and refresh the individual
post page you’ll see our “Delete Blog Post” link.150
Chapter 6: Forms
Blog delete post
Clicking on the link takes us to the delete page for the blog post, which displays the
name of the blog post.
Blog delete post page
If you click on the “Confirm” button, it redirects you to the homepage where the blog
post has been deleted!151
Chapter 6: Forms
Homepage with post deleted
So it works!
Tests
Time for tests to make sure everything works now–and in the future–as expected.
We’ve added a get_absolute_url method to our model and new views for create,
update, and edit posts. That means we need four new tests:
• def test_get_absolute_url
• def test_post_create_view
• def test_post_update_view
• def test_post_delete_view
Update your existing tests.py file as follows.Chapter 6: Forms
Code
# blog/tests.py
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
152153
Chapter 6: Forms
def test_get_absolute_url(self):
self.assertEquals(self.post.get_absolute_url(), '/post/ /')
def test_post_content(self):
self.assertEqual(f'{self.post.title}', 'A good title')
self.assertEqual(f'{self.post.author}', 'testuser')
self.assertEqual(f'{self.post.body}', 'Nice body content')
def test_post_list_view(self):
response = self.client.get(reverse('home'))
self.assertEqual(response.status_code,
)
self.assertContains(response, 'Nice body content')
self.assertTemplateUsed(response, 'home.html')
def test_post_detail_view(self):
response = self.client.get('/post/ /')
no_response = self.client.get('/post/
self.assertEqual(response.status_code,
/')
)
self.assertEqual(no_response.status_code,
)
self.assertContains(response, 'A good title')
self.assertTemplateUsed(response, 'post_detail.html')
def test_post_create_view(self):
response = self.client.post(reverse('post_new'), {
'title': 'New title',
'body': 'New text',
'author': self.user,
})154
Chapter 6: Forms
self.assertEqual(response.status_code,
)
self.assertContains(response, 'New title')
self.assertContains(response, 'New text')
def test_post_update_view(self):
response = self.client.post(reverse('post_edit', args=' '), {
'title': 'Updated title',
'body': 'Updated text',
})
self.assertEqual(response.status_code,
)
def test_post_delete_view(self):
response = self.client.get(
reverse('post_delete', args=' '))
self.assertEqual(response.status_code,
)
We expect the url of our test to be at post/ / since there’s only one post and the
is its primary key Django adds automatically for us. To test create view we make a
new response and then ensure that the response goes through (status code 200) and
contains our new title and body text. For update view we access the first post–which
has a pk of
which is passed in as the only argument–and we confirm that it results
in a 302 redirect. Finally we test our delete view by confirming that if we delete a post
the status code is 200 for success.
There’s always more tests that can be added but this at least has coverage on all our
new functionality.

## Conclusión
In a small amount of code we’ve built a blog application that allows for creating,
reading, updating, and deleting blog posts. This core functionality is known by
the acronym CRUD: Create-Read-Update-Delete. While there are multiple ways to
achieve this same functionality–we could have used function-based views or written
our own class-based views–we’ve demonstrated how little code it takes in Django to
make this happen.
In the next chapter we’ll add user accounts and login, logout, and signup functionality.