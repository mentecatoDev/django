 

# 10. Autenticación de usuarios

## 10.1. Plantillas
Por defecto, el cargador de plantillas de Django las busca en una estructura anidada dentro de cada aplicación. Así que una plantilla `home.html` de `accounts` tendría que estar ubicada en `accounts/templates/accounts/home.html`.

Pero el enfoque de carpeta de plantillas a nivel de proyecto es más limpio y se escala mejor, así que se usará éste.

```bash
(news) $ mkdir templates
(news) $ mkdir templates/registration
```

FICHERO: `newspaper_project/settings.py`
```python
TEMPLATES = [
    {
    ...
    'DIRS': [str(BASE_DIR.joinpath('templates'))],
    ...
    }
]
```
Tras iniciar o cerrar sesión en un sitio se es redirigido inmediatamente a una página subsiguiente. Por tanto, habrá que decirle a Django dónde enviar al usuario en cada caso. Las configuraciones `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL` hacen eso. Se configurará ambos para redirigirlos a la página de inicio, que tendrá el nombre de URL `home`.

> Recordar que cuando se crean las rutas URL se tiene la opción de añadir un nombre a cada una. Así que cuando se construya la URL de la página de inicio habrá que asegurarse de llamarla `home`.

Añadir estas dos líneas en la parte inferior del archivo settings.py.

FICHERO: `newspaper_project/settings.py`
```python
# Redirect
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```
Ahora se pueden crear cuatro nuevas plantillas:

```bash
(news) $ touch templates/registration/login.html
(news) $ touch templates/registration/signup.html
(news) $ touch templates/base.html
(news) $ touch templates/home.html
```
Veamos el código HTML para cada archivo.

`base.html` será heredada por cada una de las otras plantillas del proyecto. Usando un bloque como `{% block content %}` se puede más tarde sobreescribir el contenido sólo en este lugar desde otras plantillas.

FICHERO: `templates/base.html`
```html
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{% block title %}Newspaper App{% endblock title %}</title>
</head>
<body>
  <main>
    {% block content %}
    {% endblock content %}
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
    ¡Hola {{ user.username }}!
    <p><a href="{% url 'logout' %}">Logout</a></p>
  {% else %}
    <p>No estás logueado</p>
    <a href="{% url 'login' %}">Login</a> |
    <a href="{% url 'signup' %}">Registro</a>
  {% endif %}
{% endblock content %}
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
{% endblock content%}
```
FICHERO: `templates/registration/signup.html`
```html
{% extends 'base.html' %}

{% block title %}Registro{% endblock %}

{% block content %}
<h2>Registro</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Registrar</button>
</form>
{% endblock content%}
```


## 10.2. URLs

En el archivo `urls.py`, a nivel de proyecto, se quiere que la plantilla `home.html` aparezca como página de inicio. Pero no se quiere construir una app `pages` dedicada todavía, así que se puede usar el atajo de importar `TemplateView` y establecer el `template_name` justo en el patrón url.

A continuación se quiere "incluir" tanto la app `accounts` como la app `auth` que incorpora django. La razón es que la app `auth`  ya proporciona vistas y urls para el inicio y el cierre de sesión. Pero **para el registro hay que crear una vista y una url propias**.

Para asegurar que las rutas URL sean consistentes se colocarán ambas en `accounts/` para que las URLs sean `/accounts/login`, `/accounts/logout` y `/accounts/signup`.

FICHERO: `newspaper_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include										# new
from django.views.generic.base import TemplateView							# new


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),							# new
    path('accounts/', include('django.contrib.auth.urls')),					# new
    path('', TemplateView.as_view(template_name='home.html'), name='home'),	# new
]
```

Ahora se crea un archivo `urls.py` en la app `accounts`.

```bash
(news) $ touch accounts/urls.py
```

Actualizar `accounts/urls.py` con el siguiente código:

FICHERO: `accounts/urls.py`
```python
from django.urls import path
from .views import SignUp



urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
]
```
El último paso es el archivo `views.py` que contendrá la lógica del formulario de inscripción. Se usará el `CreateView` genérico de Django diciéndole que use `CustomUserCreationForm`, para redirigirse a `login` una vez que el usuario se registre con éxito, y que la plantilla se llama `signup.html`.

FICHERO: `accounts/views.py`
```python
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
```

Arrancar el servidor con python `manage.py runserver` e ir a la página principal en http://127.0.0.1:8000/. Probar todo y crear un nuevo usuario `testuser`.

> Recuerda establecer el idioma en el fichero `settings.py`.
>
> ```python
> LANGUAGE_CODE = 'es'
> 
> TIME_ZONE = 'Europe/Madrid'
> ```

Como tenemos un nuevo campo `age` añadámoslo al template `home.html`. Es un campo del modelo de usuario por lo que para mostrarlo sólo tenemos que usar `{{ user.age }}` pero comprobando previamente que su contenido no es `null`.

FICHERO: `templates/home.html`

```html
{% extends 'base.html' %}

{% block title %}Home{% endblock title %}

{% block content %}
{% if user.is_authenticated %}
  ¡Hola {{ user.username }}! 
  {% if user.age %}
    Tienes {{ user.age }} años.
  {% endif %}
  <p><a href="{% url 'logout' %}">Logout</a></p>
{% else %}
  <p>No estás logueado</p>
  <a href="{% url 'login' %}">Login</a> |
  <a href="{% url 'signup' %}">Registro</a>
{% endif %}
{% endblock content %}
```

## 10.3. Admin
Entrar también en el administrador para ver las dos cuentas de usuario. No se podrá entrar con una cuenta que no sea de superusuario.

Todo está funcionando pero **no** hay un campo `email` para el usuario `testuser` porque no fue incluido en `accounts/form.py`.

Este es un punto importante: sólo porque el modelo de usuario tenga un campo no implica que se incluirá en nuestro formulario de registro personalizado a menos que se añada explícitamente. Hagámoslo ahora.

En principio `accounts/forms.py` tiene el siguiente aspecto:

FICHERO: `accounts/forms.py`
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
Como campos se usan `Meta.fields` que sólo muestran la configuración por defecto de nombre_de_usuario/contraseña. Pero también se puede establecer explícitamente qué campos se quieren mostrar, así que se actualizará para pedir un nombre_de_usuario/correo_electrónico/contraseña configurándolo como `('username', 'email','age')` . ¡No se necesita incluir el campo `password` porque es **obligatorio**! Pero todos los demás campos pueden ser configurados como se quiera.

FICHERO: `accounts/forms.py`
```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'age') # new


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age') # new
```
El flujo de autenticación de usuarios de Django requiere un poco de configuración, pero puede verse que también proporciona una increíble flexibilidad para configurar el registro e iniciar la sesión exactamente como se requiera.

## 10.4. Conclusión

Hasta ahora la aplicación `Newspaper` tiene un modelo de usuario personalizado y funciona con páginas de *registro*, *login* y *logout* aunque no tiene muy buen aspecto. Próximamente se añadirá **Bootstrap** para mejorar el estilo además de una *app* dedicada `pages` .



|\/| [- |\| ~|~ [- ( /\ ~|~ () ^/_ '|

