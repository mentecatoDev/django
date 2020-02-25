 

# 10. Autenticación de usuarios

## 10.1. Plantillas
- Por defecto, el cargador de plantillas de Django busca plantillas en una estructura anidada dentro de cada aplicación. Así que una plantilla `home.html` en usuarios tendría que estar ubicada en `users/templates/users/home.html`.
- Pero un enfoque de carpeta de plantillas a nivel de proyecto es más limpio y se escala mejor, así que eso es lo que se usará.

```bash
(news) $ mkdir templates
(news) $ mkdir templates/registration
```

FICHERO: `newspaper_project/settings.py`
```python
TEMPLATES = [
    {
    ...
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    ...
    }
]
```
- Si se piensa en lo que sucede cuando se inicia o cierra sesión en un sitio, se es redirigido inmediatamente a una página subsiguiente. Por tanto, habrá que decirle a Django dónde enviar a los usuarios en cada caso. Las configuraciones `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL` hacen eso. Se configurará ambos para redirigirlos a la página de inicio, que tendrá el nombre de URL `home`.
- Recordar que cuando se crean las rutas URL se tiene la opción de añadir un nombre a cada una. Así que cuando se construya la URL de la página de inicio habrá que asegurarse de llamarla `home`.
- Añadir estas dos líneas en la parte inferior del archivo settings.py.

FICHERO: `newspaper_project/settings.py`
```python
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```
Ahora se pueden crear cuatro nuevas plantillas:

```bash
(news) $ touch templates/registration/login.html
(news) $ touch templates/base.html
(news) $ touch templates/home.html
(news) $ touch templates/signup.html
```
- Este es el código HTML para cada archivo a utilizar. `base.html` será heredada por cada una de las otras plantillas del proyecto. Usando un bloque como `{% block contente %}` se puede más tarde sobreescribir el contenido sólo en este lugar desde otras plantillas.

FICHERO: `templates/base.html`
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Newspaper App</title>
  </head>
  <body>
    <main>
      {% block content %}
      {% endblock %}
    </main>
  </body>
</html>
```
FICHERO: `templates/home.html`
```html
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
  {% if user.is_authenticated %}
    Hi {{ user.username }}!
    <p><a href="{% url 'logout' %}">logout</a></p>
  {% else %}
    <p>You are not logged in</p>
    <a href="{% url 'login' %}">login</a> |
    <a href="{% url 'signup' %}">signup</a>
  {% endif %}
{% endblock %}
```
FICHERO: `templates/registration/login.html`
```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<h2>Login</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Login</button>
</form>
{% endblock %}
```
FICHERO: `templates/signup.html`
```html
{% extends 'base.html' %}

{% block title %}Sign Up{% endblock %}

{% block content %}
<h2>Sign up</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign up</button>
</form>
{% endblock %}
```

## 10.2. URLs

- En el archivo `urls.py`, a nivel de proyecto, se quiere que la plantilla `home.html` aparezca como página de inicio. Pero no se quiere construir una app `pages` dedicada todavía, así que se puede usar el atajo de importar `TemplateView` y establecer el `template_name` justo en el patrón url.
- A continuación se quiere "incluir" tanto la app `users` como la app `auth` incorporada. La razón es que la app `auth` incorporada ya proporciona vistas y urls para el inicio y el cierre de sesión. Pero para el registro hay que crear una vista y una url propias. Para asegurar que las rutas URL sean consistentes se colocarán ambas en `users/` para que las URLs eventuales sean `/users/login`, `/users/logout` y `/users/signup`.

FICHERO: `newspaper_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
```

- Ahora se crea un archivo `urls.py` en la app `users`.

```bash
(news) $ touch users/urls.py
```

- Actualizar a los `users/urls.py` con el siguiente código:

FICHERO: `users/urls.py`
```python
from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
```
- El último paso es el archivo `views.py` que contendrá la lógica del formulario de inscripción. Se usará el `CreateView` genérico de Django diciéndole que use `CustomUserCreationForm`, para redirigirse a `login` una vez que el usuario se registre con éxito, y que la plantilla se llama `signup.html`.

FICHERO: `users/views.py`
```python
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
```

- Arrancar el servidor con python `manage.py runserver` e ir a la página principal en http://127.0.0.1:8000/. Probar todo y crear un nuevo usuario `testuser`.



## 10.3. Admin
- Entrar también en el administrador para ver las dos cuentas de usuario. No se podrá entrar con una cuenta de superusuario.
- Todo está funcionando pero no hay un campo `email` para el usuario `testuser`.
    - En  la página de registro users/signup/ se puede ver que sólo se pide un nombre de usuario y una contraseña, ¡no un correo electrónico!
    - Así es como funciona la configuración predeterminada de Django pero se puede cambiar fácilmente en `users/forms.py`.
- En principio tiene este aspecto:

FICHERO: `users/forms.py`
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
```
- Como campos se usan `Meta.fields` que sólo muestran la configuración por defecto de nombre_de_usuario/contraseña. Pero también se puede establecer explícitamente qué campos se quieren mostrar, así que se actualizará para pedir un nombre_de_usuario/correo_electrónico/contraseña configurándolo como `('username', 'email',)` . ¡No se necesita incluir el campo `password` porque es obligatorio! Pero todos los demás campos pueden ser configurados como se quiera.

FICHERO: `users/forms.py`
```python
...
class CustomUserCreationForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', ) # new


    class CustomUserChangeForm(UserChangeForm):
        class Meta:
            model = CustomUser
            fields = ('username', 'email', ) # new
```
- El flujo de autenticación de usuarios de Django requiere un poco de configuración, pero puede verse que también proporciona una increíble flexibilidad para configurar el registro e iniciar la sesión exactamente como se requiera.

## 10.4. Conclusión

- Hasta ahora nuestra aplicación `Newspaper` tiene un modelo de usuario personalizado y funciona con páginas de *registro*, *login* y *logout* aunque no tiene muy buen aspecto. Próximamente se añadirá **Bootstrap** para mejorar para el estilo además de una app de páginas dedicadas.