# 9. Modelo de usuario personalizado
- La documentación oficial de Django recomienda encarecidamente utilizar un **modelo de usuario personalizado** para los nuevos proyectos. La razón es que si se quiere hacer cualquier cambio en el modelo de usuario en el futuro -por ejemplo, añadiendo un campo de edad- utilizar un modelo de usuario personalizado desde el principio lo convierte en algo sencillo. Pero si no se crea un modelo de usuario personalizado, actualizar el modelo de usuario por defecto en un proyecto Django existente es muy, **muy difícil**.
- Sin embargo, el ejemplo de la documentación oficial no es realmente lo que muchos expertos de Django recomiendan. Utiliza el complejo `AbstractBaseUser` cuando si sólo se utiliza `AbstractUser` las cosas son mucho más sencillas y aún así personalizables.
- Hagamos un periódico (homenaje a las raíces de Django como un framework construido para editores y periodistas en el [Lawrence Journal-World](https://en.wikipedia.org/wiki/Lawrence_Journal-World)).
## 9.1. Setup
```bash
$ cd ~/Desktop
$ mkdir news
$ cd news
$ pipenv install django
$ pipenv shell
(news) $ django-admin startproject newspaper_project .
(news) $ python manage.py startapp users
(news) $ python manage.py runserver
```
- Tener en cuenta que aún **no se ha ejecutado la migración** para configurar la base de datos.
    - Es importante **esperar hasta después** de que se haya creado el nuevo modelo de usuario personalizado antes de hacerlo, dado lo estrechamente conectado que está el modelo de usuario con el resto de Django.

## 9.2 Modelo de usuario personalizado
- La creación de nuestro modelo de usuario personalizado requiere cuatro pasos:
    - Actualizar `settings.py`
    - Crear un nuevo modelo `CustomUser` añadiendo un nuevo campo `age`
    - Crear nuevos formularios para `UserCreation` y `UserChangeForm`
    - Actualizar el admin


 FICHERO: `newspaper_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users', # new
]
...
AUTH_USER_MODEL = 'users.CustomUser' # new
```

FICHERO: `users/models.py`
```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=0)
```

## 9.3. Formularios
- Hay dos formas de interactuar con el nuevo modelo de Usuario Personalizado
    - Cuando un usuario se registra para una nueva cuenta en el sitio web
    - Dentro de la aplicación de administración que permite, como superusuarios, modificar los usuarios existentes.
- Así que hay que actualizar los dos formularios incorporados para esta funcionalidad: `UserCreationForm` y `UserChangeForm`.

```bash
(noticias) $ touch users/forms.py
```
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
- Para ambos formularios se usa el modelo `CustomUser` con los campos por defecto de `Meta.fields`.
- El modelo de `CustomUser` contiene todos los campos del modelo de usuario por defecto y el campo `age` adicional que se ha definido.
- ¿Pero cuáles son estos campos por defecto?
    - Resulta que hay muchos, incluyendo ``username``, ``first_name``, ``last_name``, ``email``, ``password``, ``groups`` y más.
    - Sin embargo, cuando un usuario se registra en una nueva cuenta en Django, el formulario predeterminado sólo pide un nombre de usuario, un correo electrónico y una contraseña.
    - Esto nos dice que la configuración predeterminada para los campos en `UserCreationForm` son sólo el ``username``,  ``email`` y ``password``aunque hay muchos más campos disponibles.
    - Por tanto, entender los formularios y los modelos correctamente lleva algún tiempo.
- El paso final es actualizar el archivo `admin.py` ya que *Admin* está estrechamente unido al modelo de Usuario por defecto. Se extenderá la clase existente `UserAdmin` para usar el nuevo modelo de `CustomUser` y los dos nuevos formularios.
FICHERO: `users/admin.py`
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age']
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
```
- Obsérvese que `CustomUserAdmin` también tiene un ajuste de `list_display` de manera que sólo muestra los campos de `email` , `username` y `age` aunque de hecho hay muchos más en el modelo de `CustomUser`
- Ejecutar `makemigrations` y `migrate` por primera vez para crear una nueva base de datos que utilice el modelo de usuario personalizado.

```bash
(news) $ python manage.py makemigrations
(news) $ python manage.py migrate
```
## 9.4. Superusuario
Vamos a crear una cuenta de superusuario para confirmar que todo funciona como se espera. En la línea de comandos, escriba el siguiente comando y pase a través de las indicaciones.

```bash
(news) $ python manage.py createsuperuser
```
- El hecho de que esto funcione es la primera prueba de que el modelo de usuario personalizado funciona como se esperaba.
- Navegar a http://127.0.0.1:8000/admin, logear y probar.

## 9.5. Conclusión
Con el modelo de usuario personalizado completo, ahora podemos centrarnos en construir el resto de la aplicación *Periódico*.