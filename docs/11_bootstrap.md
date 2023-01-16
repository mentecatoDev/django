# 11. Bootstrap

El desarrollo de la web requiere de muchas habilidades. No sólo hay que programar un sitio web para que funcione correctamente, los usuarios también esperan que se vea bien. Cuando se está creando todo desde cero, puede ser abrumador añadir también todo el HTML/CSS necesario para un sitio atractivo.

Afortunadamente está **[Bootstrap](https://getbootstrap.com/)** , el framework más popular para construir proyectos *responsivos* y para móviles (aunque también podríamos contar con **[Tailwind CSS](https://tailwindcss.com/)**). En lugar de escribir nuestro propio CSS y JavaScript para las características comunes de diseño de sitios web, podemos confiar en Bootstrap para hacer el trabajo pesado. Esto significa que con sólo una pequeña cantidad de código de nuestra parte podemos tener rápidamente sitios web de gran apariencia. Y si queremos hacer cambios personalizados a medida que el proyecto avanza, también es fácil anular Bootstrap cuando sea necesario.

Cuando centrarse en la funcionalidad de un proyecto, y no en el diseño, es lo importante, Bootstrap es una gran elección.

## 11.1. Pages app

Hasta ahora se muestra la página de inicio incluyendo la lógica de la vista en el archivo `urls.py`. Aunque este enfoque funciona, es una triquiñuela y ciertamente no escala a medida que un sitio web crece con el tiempo. También es probablemente algo confuso para los recién llegados a Django. En su lugar se puede y debe crear una aplicación de páginas dedicadas para todas las **páginas estáticas**. Esto mantendrá el código bien organizado en el futuro. En la línea de comandos usar el comando `startapp` para crear la aplicación `pages`.

```bash
(news) $ python manage.py startapp pages
```

 Recordar actualizar inmediatamente el archivo `settings.py`.

FICHERO: `newspaper_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'pages.apps.PagesConfig',                             # new
]
```
Ahora se puede actualizar el archivo `urls.py` a nivel de proyecto. Eliminar el `import` de `TemplateView`. También se actualizará la ruta `''` para incluir las páginas de la aplicación.

FICHERO: `newspaper_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),                      # new
]
```

Es hora de añadir la página web, lo cual significa hacer el baile estándar de *urls/views/templates* de Django.

```bash
(news) $ touch pages/urls.py
```

Luego importar las vistas aún no creadas, establecer las rutas y asegurarse de nombrar cada url, también.

FICHERO: `pages/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]
```

El código de `views.py` debería resultar familiar a estas alturas. Se usa la vista genérica basada en clases `TemplateView` de Django, lo que significa que sólo habrá que especificar el `template_name` para usarlo.

FICHERO: `pages/views.py`
```python
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'
```

Ya existe una plantilla `home.html`. Confirmar que sigue funcionando como se esperaba con la nueva url y vista.

## 11.2. Tests

Hay dos momentos ideales para añadir pruebas
- Antes de escribir cualquier código (test-driven-development)
- Inmediatamente después de que se haya añadido una nueva funcionalidad y aún esté clara en la mente.

Actualmente el proyecto tiene cuatro páginas:

- `home`
- `signup`
- `login`
- `logout`

Sólo se necesita probar las dos primeras. `login` y `logut` que son parte de Django y ya tienen cobertura de tests.

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
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                         [0].username, self.username)
        self.assertEqual(get_user_model().objects.all()
                         [0].email, self.email)
```
- En la línea superior se usa `get_user_model()` para referirse al modelo de usuario personalizado.
- Luego para ambas páginas se prueban tres cosas:
  - Si la página existe y devuelve un código de estado HTTP 200
  - Si la página utiliza el nombre de la url correcta en la vista
  - Si se está utilizando la plantilla adecuada
- La página de registro también tiene un formulario, así que se debería probar eso también.
- En el formulario `test_signup_form` se está verificando que cuando un nombre de usuario y una dirección de correo electrónico son POSTeados (enviados a la base de datos), coinciden con lo que se almacena en el modelo `CustomUser`.
- Ten en cuenta que hay dos formas de especificar una página: o bien codificando como en `test_signup_page_-status_code` donde establecemos la respuesta a `/accounts/signup/` o a través del nombre de la URL de `signup` como se hace en `test_view_url_by_name` y `test_view_uses_correct_template`.
- Ejecutar:
```bash
(news) $ python manage.py test
```

## 11.3. Bootstrap
Si no has utilizado nunca Bootstrap, estás ante una auténtica maravilla. Al igual que Django, consigue
mucho con muy poco código.

Hay dos maneras de añadir *Bootstrap* a un proyecto:

- Se pueden descargar todos los archivos y servirlos localmente
- Confiar en una Red de Entrega de Contenido (CDN *Content Delivery Network*)

El segundo enfoque es más sencillo de implementar siempre que se tenga una conexión a Internet consistente, así que eso es lo que se usará aquí.

*Bootstrap* viene con una plantilla inicial que incluye los archivos básicos necesarios. En particular, hay cuatro que se incorporarán:

- `Bootstrap.css`
- `jQuery.js`
- `Popper.js`
- `Bootstrap.js`

FICHERO: `templates/base.html`
```html
<!doctype html>
<html lang="es">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>

    <!-- Option 2: jQuery, Popper.js, and Bootstrap JS
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
    -->
  </body>
</html>
```
Este fragmento de código incluye los enlaces completos de Bootstrap CSS y JavaScript. Está actualizado a 23/02/2021 pero se puede encontrar la última versión en los [documentos de inicio rápido](https://getbootstrap.com/docs/4.5/getting-started/introduction/#quick-start).

Se añade ahora:

- Una barra de navegación en la parte superior de la página que contiene los enlaces para:
    - la página de inicio
    - inicio de sesión
    - cierre de sesión
    - registro.

- En particular, se pueden usar las etiquetas `if/else` en el motor de plantillas de Django para añadir algo de lógica básica. Se quiere mostrar un botón de "login" y "signup" a los usuarios que han cerrado la sesión, pero un botón de "logout" y "cambiar contraseña" a los usuarios que han iniciado la sesión.

FICHERO: `templates/base.html`
```html
<html lang="es">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">

    <title>{% block title %}Newspaper App{% endblock title %}</title>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="{% url 'home' %}">Newspaper</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        {% if user.is_authenticated %}
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                {{ user.username }}
              </a>
              <div class="dropdown-menu dropdown-menu-lg-right" aria-labelledby="navbarDropdown">
                <a class="dropdown-item" href="{% url 'password_change'%}">Cambiar contraseña</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item" href="{% url 'logout' %}">Logout</a>
              </div>
            </li>
          </ul>
        {% else %}
          <form class="form-inline ml-auto">
            <a href="{% url 'login' %}" class="btn btn-outline-secondary">Login</a>
            <a href="{% url 'signup' %}" class="btn btn-primary ml-2">Registrar</a>
          </form>
        {% endif %}
      </div>
    </nav>

    <main>
      <div class="container">
        {% block content %}
        {% endblock content %}
      </div>
    </main>


    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper)
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
    -->

    <!-- Option 2: jQuery, Popper.js, and Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
  </body>
</html>
```

Lo único a mejorar es el botón de "Login". Se puede usar Bootstrap para añadir un estilo agradable, como hacerlo verde y atractivo.


FICHERO: `templates/registration/login.html`
```html
...
  <button class="btn btn-success ml-2" type="submit">Login</button>
...
```

## 11.4. Formulario de inscripción

¿De dónde vino ese texto? Cuando algo se siente "mágico" en Django, seguro que no lo es.

El método más rápido para averiguar lo que ocurre bajo el capó de Django es simplemente ir al código fuente de Django en Github, usar la barra de búsqueda e intentar encontrar el trozo de texto específico.

Por ejemplo, si se busca "150 characters or fewer" se encontrará en la página `django/contrib/auth/models.py` que se encuentra ahí en la línea 334. El texto viene como parte de la app `auth`, en el campo de nombre de usuario de `AbstractUser`.

Ahora hay tres opciones:
- anular el `help_text` existente
- ocultar el `help_text`
- reestilar el `help_text`

Se escogerá la tercera opción ya que es una buena manera de introducir el excelente paquete de terceros `django-crispy-forms`. Trabajar con formularios es un reto y `django-crispy-forms` hace más fácil escribir código *DRY* (Don't Repeat Yourself).

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

    # 3rd Party
    'crispy_forms',

    # Local
    'accounts.apps.AccountsConfig',
    'pages.apps.PagesConfig',
]
```
Ya que se está usando `Bootstrap4` también se debería añadir esa configuración al archivo `settings.py`. Esto va en la parte inferior del archivo.

FICHERO: `newspaper_project/settings.py`
```python
CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

Ahora en la plantilla de `signup.html` se puede usar rápidamente formularios crujientes (*crispy forms*). Primero se cargan las etiquetas `crispy_forms_tags` en la parte superior y luego se intercambia `{{ form.as_p }}` por `{{ form|crispy }}`.

FICHERO: `templates/signup.html`
```html
{% extends 'base.html' %}

{% load crispy_forms_tags %}

{% block title %}Registro{% endblock %}

{% block content %}
  <h2>Registro</h2>
  <form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit">Registrarse</button>
  </form>
{% endblock content %}
```

Mucho mejor. Aunque, ¿qué tal si el botón de "Registrarse" fuera un poco más atractivo?¿Quizás hacerlo verde? Bootstrap tiene todo tipo de opciones de estilo de botones donde elegir. Se usará el "exitoso" fondo verde con texto blanco.

FICHERO: `templates/signup.html`
```html
...
<button class="btn btn-success" type="submit">Registrarse</button>
...
```

## 11.5. Próximos pasos
El último paso del flujo de autentificación de usuarios es configurar el cambio y el restablecimiento de la contraseña. Una vez más Django se ha encargado del trabajo pesado, así que solo se requiere una cantidad mínima de código adicional.