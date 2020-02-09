## 8. Cuentas de Usuarios
- La mayoría de las aplicaciones web cuentan con una importante pieza: la **autenticación del usuario**.
- La implementación de una autenticación de usuario adecuada es conocida por su dificultad
- Afortunadamente Django viene con un poderoso sistema de autenticación de usuarios incorporado.
- Cada vez que se crea un nuevo proyecto, Django instala por defecto la aplicación de autenticación, que proporciona un objeto de usuario que contiene:

  + Nombre de Usuario
  + Contraseña
  + Correo Electrónico
  + Nombre
  + Apellidos
  
## 8.1. Login

- Se usará este objeto usuario para implementar:

  + El inicio de sesión
  + El cierre de sesión
  + El registro en la aplicación del blog

- Django proporciona una vista predeterminada para una página de inicio de sesión a través de `LoginView`.
  + Todo lo que se necesita es:
    - Añadir un patrón de url a nivel de proyecto para el sistema de autorización
    - Una plantilla de inicio de sesión
    - Una pequeña actualización del fichero `settings.py`

- Actualizar el archivo `urls.py` a nivel de proyecto
  + Se colocaran las páginas de *login* y *logout* en la URL `accounts/`.

FICHERO: `blog_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
]
```
Como se indica en la documentación de `LoginView`, por defecto Django buscará dentro de una carpeta de plantillas llamada `registration` un archivo llamado `login.html` para un formulario de inicio de sesión. Así que tenemos que crear un nuevo directorio llamado `registration` y el archivo requerido dentro de él.
```bash
(blog) $ mkdir templates/registration
(blog) $ touch templates/registration/login.html
```
FICHERO: `templates/registration/login.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>
{% endblock content %}
```
Se usan las etiquetas HTML <form></form> y se especifica el método POST ya que se están enviando datos al servidor (se usa GET si se están solicitando datos, como en un formulario de un motor de búsqueda). Se añade `{% csrf_token %}` por motivos de seguridad, es decir, para evitar un ataque XSS. El contenido del formulario se muestra entre las etiquetas de los párrafos gracias a `{{ form.as_p }}` y luego se añade un botón de "enviar".
En el paso final hay que especificar dónde redirigir al usuario cuando el acceso es exitoso. Podemos establecer esto con la configuración `LOGIN_REDIRECT_URL`. En la parte inferior del archivo `settings.py` agregar:
FICHERO: `settings.py`
```
LOGIN_REDIRECT_URL = 'home'
```
Ahora el usuario será redirigido a la plantilla `home` que es la página de inicio.
Navegar ahora a: http://127.0.0.1:8000/accounts/login/

Al introducir la información de acceso de la cuenta de superusuario, seremos redirigidos a la página de inicio.
Nótese no se  ha añadido ninguna lógica de visualización ni se ha creados un modelo de base de datos porque el sistema de autentificación de Django los proporcionó automáticamente.
## 8.2. Actualizado de la homepage

- Actualizar la plantilla base.html para mostrar un mensaje a los usuarios tanto si están conectados como si no.
  + Se puede usar el atributo `is_authenticated` para esto.
- Por ahora, se pondrá este código en una posición prominente. Más adelante se le pordrá dar un estilo más apropiado.

FICHERO: `templates/base.html`
```
...
</header>
{% if user.is_authenticated %}
  <p>Hi {{ user.username }}!</p>
{% else %}
  <p>You are not logged in.</p>
  <a href="{% url 'login' %}">login</a>
{% endif %}
{% block content %}
{% endblock content %}
```
- Si el usuario está conectado, se le saludará por su nombre, si no,  se le dará un enlace a la recién creada página de acceso.

## 8.3. Enlace para Logout
- Se añade un enlace de cierre de sesión que redirija a la página de inicio.
  + Gracias al sistema de autentificación de Django, esto es muy sencillo de conseguir.
- En el archivo `base.html` se agrega un enlace de una línea `{% url 'desconexión' %}` para desconectarse.

FICHERO: `templates/base.html`
```
...
{% if user.is_authenticated %}
  <p>Hi {{ user.username }}!</p>
  <p><a href="{% url 'logout' %}">logout</a></p>
{% else %}
...
```
- Eso es todo lo que se necesita hacer ya que la `view` necesaria proporciona aplicación de autentificación `auth`. Aún se necesita especificar dónde redirigir al usuario al cerrar la sesión.
- Actualizar `settings.py` para proporcionar un enlace de redireccionamiento que se llama, apropiadamente, `LOGOUT_REDIRECT_URL`. Podemos añadirlo justo al lado de nuestra redirección de inicio de sesión, de manera que la parte inferior del archivo tenga el siguiente aspecto:

FICHERO: `blog_project/settings.py`
```
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

## 8.4. Inscripción
- Se necesita escribir una vista propia para la página de registro de nuevos usuarios, pero Django  proporciona una clase formulario, `UserCreationForm`, para facilitar las cosas. 
  + Por defecto viene con tres campos: nombre de usuario, contraseña y contraseña.
- Hay muchas maneras de organizar el código y la estructura de urls para un sistema de autenticación de usuario robusto. Aquí se creará una nueva aplicación dedicada, `accounts`, para la página de registro.

```bash
(blog) $ python manage.py startapp accounts
```
- Añadir la nueva app a INSTALLED_APPS del fichero `settings.py`.
FICHERO: `blog_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'accounts',
]
```
- A continuación añadimos una url a nivel de proyecto que apunta a esta nueva aplicación directamente debajo de donde incluimos la aplicación de autorización incorporada.
FICHERO: `blog_project/urls.py`
```
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('blog.urls')),
]
```
- El orden de las `urls` importa porque Django lee este archivo de arriba a abajo. Por lo tanto, cuando se solicite la url `/accounts/signup`, Django buscará primero en el archivo `auth`, no lo encontrará, y luego procederá a la aplicación `accounts` de cuentas.
```bash
(blog) $ touch accounts/urls.py
```
And add the following code:
FICHERO: `acounts/urls.py`
```python
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
```
- Se éstá usando una vista que aún no se ha creado llamada  `SignupView` que está basada en clases, ya que está en mayúsculas, y tiene el sufijo `as_view()`. Su ruta es sólo `signup/` por lo que la ruta general será `accounts/signup/`.
- Ahora para la vista que usa el `UserCreationForm` incorporado y el CreateView genérico .
FICHERO: `accounts/views.py`
```python
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
```
- Se está heredando de la vista genérica basada en clases `CreateView` la clase `SignUpView`. Se especifica el uso de `UserCreationForm` incorporado y la plantilla aún no creada en `signup.html`. Y se usa `reverse_lazy` para redirigir al usuario a la página de inicio de sesión cuando se registra con éxito.
- ¿Por qué usar aquí `reverse_lazy` en lugar de `reverse`? La razón es que para todas las vistas genéricas basadas en clases las urls no se cargan cuando se importa el archivo, por lo que tenemos que usar la forma perezosa de `reverse` para cargarlas más tarde cuando estén disponibles.
- Añadir `signup.html` a la carpeta de plantillas a nivel de proyecto:
```bash
(blog) $ touch templates/signup.html
```
TEMPLATE: `templates/signup.html`
```html
{% extends 'base.html' %}

{% block content %}
<h2>Sign up</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign up</button>
</form>
{% endblock %}
```
- Al principio se extiende la plantilla base, se coloca la lógica entre las etiquetas `<form></form>`, y se usa `csrf_token` por seguridad. El contenido del formulario se muestra en etiquetas de párrafo con `form.as_p` y se incluye un botón de envío.
- Navegar en: http://127.0.0.1:8000/accounts/signup/
- Observar que hay mucho texto extra que Django incluye por defecto. Se puede personalizar usando el *marco de mensajes* incorporado, pero por ahora probar el formulario.
- Crear un nuevo usuario llamado "William" y comprobar como al enviarlo se redirige a la página de acceso y de como, después de ingresar exitosamente, se redirige a la página de inicio con el saludo personalizado `Hi <nombre de usuario>`.
- El último flujo es, por lo tanto:

<center>Inscripción (Signup) -> Inicio de sesión (Login) -> Página de inicio (Homepage)</center>
- Y por supuesto podemos modificar esto como queramos. La `SignupView` se redirige a la entrada al sistema (login) porque se establece `success_url = reverse_lazy('login')`. La página de *login* se redirige a la *homepage* porque en el archivo `settings.py` se establece `LOGIN_REDIRECT_URL = 'home'`.
- Al principio puede parecer abrumador llevar la cuenta de todas las partes de un proyecto Django. Eso es normal. Pero prometo que con el tiempo empezarán a tener más sentido.

## 8.5. Git
```bash
(blog) $ git commit -m 'Añade formulario y cuentas de usuario'
```
Crear un nuevo repo en GitHub al que puedes llamar como quieras.
```bash
(blog) $ git remote add origin git@bitbucket.org:wsvincent/blog-app.git
(blog) $ git push -u origin master
```
## 8.6. Configuración de Heroku
- Hay cuatro cambios que hacer para el despliegue en Heroku.
  + actualizar `Pipfile.lock`
  + nuevo `Procfile`
  + instalar `gunicorn`
  + actualizar `settings.py`

FICHERO: `Pipfile`
```pipfile
[requires]
python_version = "3.8"
```

```bash
(blog) $ pipenv lock
```

```bash
(blog) $ touch Procfile
```
FICHERO: `procfile`
```
web: gunicorn blog_project.wsgi --log-file -
```
```bash
(blog) $ pipenv install gunicorn
```
FICHERO: `blog_project/settings.py`
```python
ALLOWED_HOSTS = ['*']
```
```bash
(blog) $ git status
(blog) $ git add -A
(blog) $ git commit -m 'Añade ficheros de configuración Heroku'
(blog) $ git push -u origin master
```
## 8.7. Despliegue en Heroku
```bash
(blog) $ heroku login
```
- "Create" indica a Heroku que haga un nuevo contenedor para la aplicación. Si sólo se ejecuta `heroku create`, Heroku asignará un nombre al azar, aunque se puede especificar un nombre personalizado, que debe ser único en Heroku.

```bash
(blog) $ heroku create dfb-blog
```
- Ahora configurar git de manera que cuando se suba a Heroku (push), vaya al nombre de la nueva aplicación (reemplazar `dfb-blog` con el nombre elegido).

```bash
(blog) $ heroku git:remote -a dfb-blog
```
- Hay un paso más que debemos dar ahora que tenemos archivos estáticos, en este caso CSS. Django no soporta servir archivos estáticos en producción, sin embargo el proyecto `WhiteNoise` sí lo hace. Así que vamos a instalarlo.

```bash
(blog) $ pipenv install whitenoise
```
- Hay que actualizar la configuración estática para que se use en producción. En su editor de texto abra settings.py . Añade whitenoise al INSTALLED_APPS encima de la aplicación de archivos estáticos incorporada y también al MIDDLEWARE en la tercera línea. El orden importa tanto para INSTALLED_APPS como para MIDDLEWARE .
  En la parte inferior del archivo añade nuevas líneas tanto para STATIC_ROOT como para STATICFILES_STORAGE . Debería verse como lo siguiente.

FICHERO: `blog_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # new!
    'django.contrib.staticfiles',
    'blog',
    'accounts',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # new!
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
...
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # new!
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # new!
```
```bash
(blog) $ git add -A
(blog) $ git commit -m 'Heroku config'
(blog) $ git push origin master
```
Finalmente podemos subir el código a Heroku y añadir un proceso web para que el banco de pruebas se ponga en marcha.
```
(blog) $ git push heroku master
(blog) $ heroku ps:scale web=1
```

## 8.8. Conclusión
Con una mínima cantidad de código, el framework de Django nos ha permitido crear un flujo de autenticación de usuario de inicio de sesión, cierre de sesión y registro. Bajo el capó, se ha ocupado de los muchos problemas de seguridad que pueden surgir si se intenta crear un flujo de autenticación de usuario propio desde cero.