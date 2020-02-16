# 11. Bootstrap

- El desarrollo de la web requiere de muchas habilidades. No sólo hay que programar un sitio web para que funcione correctamente, los usuarios también esperan que se vea bien. Cuando se está creando todo desde cero, puede ser abrumador añadir también todo el HTML/CSS necesario para un sitio atractivo.
- Afortunadamente está **Bootstrap**, el marco de trabajo más popular para construir proyectos *responsivos* y para móviles. En lugar de escribir nuestro propio CSS y JavaScript para las características comunes de diseño de sitios web, podemos confiar en Bootstrap para hacer el trabajo pesado. Esto significa que con sólo una pequeña cantidad de código de nuestra parte podemos tener rápidamente sitios web de gran apariencia. Y si queremos hacer cambios personalizados a medida que el proyecto avanza, también es fácil anular Bootstrap cuando sea necesario.
- Cuando centrarse en la funcionalidad de un proyecto y no en el diseño es lo importante, Bootstrap es una gran elección.

## 11.1. Pages app

- Hasta ahora se muestra la página de inicio incluyendo la lógica de la vista en el archivo `urls.py`. Aunque este enfoque funciona, es una triquiñuela y ciertamente no se escala a medida que un sitio web crece con el tiempo. También es probablemente algo confuso para los recién llegados a Django. En su lugar podemos y debemos crear una aplicación de páginas dedicadas para todas las páginas estáticas. Esto mantendrá el código bien organizado en el futuro. En la línea de comandos usar el comando `startapp` para crear la aplicación `pages`.

```bash
(news) $ python manage.py startapp pages
```

- Actualizar inmediatamente el archivo `settings.py`.

FICHERO: `newspaper_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'pages', # new
]
```
- Ahora se puede actualizar el archivo `urls.py` a nivel de proyecto. Eliminar el `import` de `TemplateView`. También se actualizará la ruta `''` para incluir las páginas de la aplicación.

FICHERO: `newspaper_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
```

- Es hora de añadir la página web, lo cual significa hacer el baile estándar de *urls/views/templates* de Django.

```bash
(news) $ touch pages/urls.py
```

- Luego importar las vistas aún no creadas, establecer las rutas y asegurarse de nombrar cada url, también.

FICHERO: `pages/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]
```

- El código de `views.py` debería resultar familiar a estas alturas. Se usa la vista genérica basada en clases `TemplateView` de Django, lo que significa que sólo habrá que especificar el `template_name` para usarlo.

FICHERO: `pages/views.py`
```python
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'
```

- Ya existe una plantilla `home.html`. Confirmar que sigue funcionando como se esperaba con nuestra la nueva url y vista.

## 11.2. Pruebas

- Hay dos momentos ideales para añadir pruebas
    - Antes de escribir cualquier código (test-driven-development)
    - Inmediatamente después de que hayas añadido una nueva funcionalidad y lo tengas claro en tu mente.
- Actualmente nuestro proyecto tiene cuatro páginas:
    - home
    - signup
    - login
    - logout
- Sólo se necesita probar las dos primeras. El login y logut son parte de Django y ya tienen cobertura de pruebas.

FICHERO: `pages/tests.py`
```python
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'

    def test_signup_page_status_code(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                         [0].username, self.username)
        self.assertEqual(get_user_model().objects.all()
                         [0].email, self.email)
```
- En la línea superior se usa `get_user_model()` para referirnos al modelo de usuario personalizado.
- Luego para ambas páginas se prueban tres cosas:
  - la página existe y devuelve un código de estado HTTP 200
  - la página utiliza el nombre de la url correcta en la vista
  - se está utilizando la plantilla adecuada
- La página de registro también tiene un formulario, así que se debería probar eso también.
- En el formulario `test_signup_form` se está verificando que cuando un nombre de usuario y una dirección de correo electrónico son POSTeados (enviados a la base de datos), coinciden con lo que se almacena en el modelo `CustomUser`.

- Ejecutar:
```bash
(news) $ python manage.py test
```

## 11.3. Bootstrap
- Hay dos maneras de añadir Bootstrap a un proyecto:
    - Se pueden descargar todos los archivos y servirlos localmente
    - Confiar en una Red de Entrega de Contenido (CDN)
- El segundo enfoque es más sencillo de implementar siempre que se tenga una conexión a Internet consistente, así que eso es lo que se usará aquí.
- Bootstrap viene con una plantilla inicial que incluye los archivos básicos necesarios. En particular, hay cuatro que se incorporarán:
    - `Bootstrap.css`
    - `jQuery.js`
    - `Popper.js`
    - `Bootstrap.js`

FICHERO: `templates/base.html`
```html
<!doctype html>
<html lang="en">
  <head>
  <!-- Required meta tags -->
  <meta charset="utf- ">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9KScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>
```
- Se añade ahora:
    - Una barra de navegación en la parte superior de la página que contiene los enlaces para:
        - la página de inicio
        - inicio de sesión
        - cierre de sesión
        - registro.
- En particular, se pueden usar las etiquetas `if/else` en el motor de plantillas de Django para añadir algo de lógica básica. Se quiere mostrar un botón de "login" y "signup" a los usuarios que han cerrado la sesión, pero un botón de "logout" y "cambiar contraseña" a los usuarios que han iniciado la sesión.

FICHERO: `templates/base.html`
```html
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf- ">
    <meta name="viewport" content="width=device-width, initial-scale= , shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>{% block title %}Newspaper App{% endblock title %}</title>
</head>
<body>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
    <a class="navbar-brand" href="{% url 'home' %}">Newspaper</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarCollapse">
      {% if user.is_authenticated %}
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link dropdown-toggle" href="#" id="userMenu" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              {{ user.username }}
            </a>
            <div class="dropdown-menu dropdown-menu-right" aria-labelledby="userMenu">
              <a class="dropdown-item" href="{% url 'password_change' %}">Change password</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="{% url 'logout' %}">Log out</a>
              </div>
            </li>
          </ul>
        {% else %}
          <form class="form-inline ml-auto">
            <a href="{% url 'login' %}" class="btn btn-outline-secondary">Log in</a>
            <a href="{% url 'signup' %}" class="btn btn-primary ml- ">Sign up</a>
          </form>
        {% endif %}
      </div>
    </nav>
    <div class="container">
      {% block content %}
      {% endblock %}
    </div>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9KScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>
```

- Lo único que se ve mal es el botón de "Login". Se puede usar Bootstrap para añadir un estilo agradable, como hacerlo verde y atractivo.


FICHERO: `templates/registration/login.html`
```html
...
  <button class="btn btn-success ml-2" type="submit">Login</button>
...
```

## 11.4. Formulario de inscripción

- ¿De dónde vino ese texto? Cuando algo se siente "mágico" en Django, seguro que no lo es.
El método más rápido para averiguar lo que ocurre bajo el capó de Django es simplemente ir al código fuente de Django en Github, usar la barra de búsqueda e intentar encontrar el trozo de texto específico.
- Por ejemplo, si se busca "150 characters or fewer" se encontrará en la página `django/contrib/auth/models.py` que se encuentra aquí en la línea 301. El texto viene como parte de la app `auth`, en el campo de nombre de usuario de `AbstractUser`.
- Ahora hat tres opciones:
  - anular el `help_text` existente
  - ocultar el `help_text`
  - reestilar el `help_text`
- Se escogerá la tercera opción ya que es una buena manera de introducir el excelente paquete de terceros `django-crispy-forms`. Trabajar con formularios es un reto y `django-crispy-forms` hace más fácil escribir código *ÁRIDO*.

```bash
(news) $ pipenv install django-crispy-forms
```

- Añadir la nueva aplicación a la lista `INSTALLED_APPS` en el archivo `settings.py`
- A medida que el número de aplicaciones comienza a crecer, es útil distinguir entre aplicaciones de terceros y aplicaciones locales que se han añadido. 

FICHERO: `newspaper_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #3rd Party
    'crispy_forms',

    # Local
    'users',
    'pages',
]
```
- Ya que se está usando `Bootstrap4` también se debería añadir esa configuración al archivo `settings.py`. Esto va en la parte inferior del archivo.

FICHERO: `newspaper_project/settings.py`
```
CRISPY_TEMPLATE_PACK = 'bootstrap '
```

- Ahora en la plantilla de `signup.html` se puede usar rápidamente formularios crujientes (*crispy forms*). Primero se cargan las etiquetas `crispy_forms_tags` en la parte superior y luego se intercambia `{{ form.as_p }}` por `{{ form|crispy }}`.

FICHERO: `templates/signup.html`
```html
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block title %}Sign Up{% endblock %}

{% block content %}
  <h2>Sign up</h2>
  <form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit">Sign up</button>
  </form>
{% endblock %}
```

- Mucho mejor. Aunque, ¿qué tal si nuestro botón de "Registrarse" fuera un poco más atractivo?¿Quizás hacerlo verde? Bootstrap tiene todo tipo de opciones de estilo de botones donde elegir. Se usará el "exitoso" fondo verde con texto blanco.

FICHERO: `templates/signup.html`
```html
...
<button class="btn btn-success" type="submit">Sign up</button>
...
```

## 11.5. Próximos pasos
- El último paso del flujo de autentificación de usuarios es configurar el cambio y el restablecimiento de la contraseña. Una vez más Django se ha encargado del trabajo pesado, así que solo se requiere una cantidad mínima de código adicional.