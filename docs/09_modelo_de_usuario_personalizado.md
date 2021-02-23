# 9. Modelo de usuario personalizado
La documentación oficial de Django recomienda encarecidamente utilizar un **modelo de usuario personalizado** para los nuevos proyectos. La razón es que si se quiere hacer cualquier cambio en el modelo de usuario en el futuro -por ejemplo, añadir un campo edad- utilizar un modelo de usuario personalizado desde el principio lo convierte en algo sencillo. Pero si **no** se crea, **actualizar el modelo de usuario** por defecto en un proyecto Django existente es muy, **muy difícil**.

Sin embargo, el ejemplo de la documentación oficial no es realmente lo que muchos expertos en Django recomiendan. Utilizar el complejo `AbstractBaseUser` cuando si sólo se utiliza `AbstractUser` las cosas son mucho más sencillas y aún así personalizables es mucho mejor práctica.

Y ahora, **hagamos un periódico** (homenaje a las raíces de Django como un framework construido para editores y periodistas en el [Lawrence Journal-World](https://en.wikipedia.org/wiki/Lawrence_Journal-World)).

## 9.1. Setup
```bash
$ cd ~/Desktop
$ mkdir news
$ cd news
$ pipenv install django
$ pipenv shell
(news) $ django-admin startproject newspaper_project .
(news) $ python manage.py startapp accounts
(news) $ python manage.py runserver
```
Tener en cuenta que aún **no se ha ejecutado la migración** para configurar la base de datos.

> Nota
>
> Es importante **esperar hasta después** de que se haya creado el nuevo modelo de usuario personalizado, dado lo **estrechamente conectado que está el modelo de usuario con el resto de Django**.

## 9.2 Modelo de usuario personalizado
La creación del modelo de usuario personalizado requiere cuatro pasos:

- Actualizar `settings.py`
- Crear un nuevo modelo `CustomUser` añadiendo un nuevo campo `age`
- Crear nuevos formularios para `UserCreation` y `UserChangeForm`
- Actualizar la app `admin`


 FICHERO: `newspaper_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountsConfig',                          # new
]
...
# Authentication                                          # new
AUTH_USER_MODEL = 'accounts.CustomUser'                   # new
```

FICHERO: `accounts/models.py`
```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad")
```
Si leemos la documentación oficial sobre modelos de usuario personalizados, ésta recomienda usar `AbstractBaseUser` en lugar de `AbstractUser` lo cual trae consigo complicaciones innecesarias; sobre todo para los novatos.

> #### `AbstractBaseUser` vs `AbstractUser`
>
> `AbstractBaseUser` requiere un nivel muy fino de control y personalización. Esencialmente reescribimos Django. Esto puede ser útil, pero si sólo queremos un modelo de usuario personalizado que se pueda actualizar con algunos campos adicionales, la mejor opción es `AbstractUser`, que es una subclase de `AbstractBaseUser`.
> En otras palabras, escribimos mucho menos código y tenemos menos oportunidades de estropear las cosas. Es la mejor opción a menos que realmente sepas lo que estás haciendo con Django.

Tenga en cuenta que utilizamos tanto `null` como `blank` con nuestro campo `age`. Estos dos términos son fáciles de confundir pero son bastante distintos:
- `null` está relacionado con la **base de datos**. Cuando un campo tiene `null=True` puede almacenar una entrada de la base de datos como NULL, es decir, sin valor.
- `blank` está relacionado con **la validación**, si `blank=True` un formulario permitirá un valor vacío, mientras que si `blank=False` se requiere un valor.

En la práctica, `null` y `blank` se utilizan comúnmente juntos de esta manera para que un formulario permita un valor vacío y la base de datos almacene ese valor como `NULL`.

Un problema común que hay que tener en cuenta es que el tipo de campo dicta cómo utilizar estos valores. Siempre que el campo esté basado en cadenas de caracteres, como `CharField` o `TextField`, si se establece tanto `null` como `blank`, como hemos hecho, resultará en dos valores posibles para "sin datos" en la base de datos. Lo cual es una mala idea. La convención de Django es usar la cadena vacía `''`, no NULL.

## 9.3. Formularios
Hay **dos formas** de interactuar con el **nuevo modelo** de usuario personalizado

- Cuando un usuario se **registra** para una nueva cuenta en el sitio web
- Dentro de la **aplicación de administración** que permite, como superusuarios, modificar los usuarios existentes.

Así que hay que actualizar los dos formularios incorporados para esta funcionalidad: `UserCreationForm` y `UserChangeForm`.

```bash
(noticias) $ touch accounts/forms.py
```

FICHERO: `accounts/forms.py`
```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
```
Para ambos formularios se usa el modelo `CustomUser` con los campos por defecto de `Meta.fields`.

El modelo de `CustomUser` contiene todos los campos del modelo de usuario por defecto y el campo `age` adicional que se ha definido.

Para los nuevos formularios usamos la clase `Meta` para anular los campos por defecto estableciendo el
modelo a nuestro `CustomUser` y utilizando los campos por defecto a través de `Meta.fields` que incluye todos los campos por defecto. Para añadir nuestro campo `age` personalizado simplemente lo añadimos al final y se mostrará automáticamente en nuestra futura página de registro. Bastante ingenioso, ¿no?.
El concepto de campos en un formulario puede ser confuso al principio, así que vamos a dedicar un momento a explorarlo más a fondo. Nuestro modelo `CustomUser` contiene todos los campos del modelo `User` por defecto y el campo adicional que hemos establecido.

¿Pero cuáles son estos campos por defecto?

Resulta que hay muchos, incluyendo ``username``, ``first_name``, ``last_name``, ``email``, ``password``, ``groups`` y más.

Sin embargo, cuando un usuario se registra en una nueva cuenta en Django, el formulario predeterminado sólo pide un nombre de usuario, un correo electrónico y una contraseña.

Esto nos dice que la configuración predeterminada para los campos en `UserCreationForm` son sólo el `username`,  `email` y `password` aunque hay muchos más campos disponibles.

Por tanto, entender los formularios y los modelos correctamente lleva algún tiempo.



El paso final es actualizar el archivo `admin.py` ya que *Admin* está estrechamente unido al modelo de usuario por defecto. Se extenderá la clase existente `UserAdmin` para usar el nuevo modelo de `CustomUser` y los dos nuevos formularios.

FICHERO: `accounts/admin.py`
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
```
Ejecutar `makemigrations` y `migrate` por primera vez para crear una nueva base de datos que utilice el modelo de usuario personalizado.

```bash
(news) $ python manage.py makemigrations
(news) $ python manage.py migrate
```
## 9.4. Superusuario
Vamos a crear una cuenta de superusuario para confirmar que todo funciona como se espera. En la línea de comandos, escribir el siguiente comando y cumplir con las indicaciones.

```bash
(news) $ python manage.py createsuperuser
```
El hecho de que esto funcione es la primera prueba de que el modelo de usuario personalizado funciona como se esperaba.

- Navegar a http://127.0.0.1:8000/admin, logear y probar. Si haces clic en el enlace para "Usuarios", se debería ver la cuenta de superusuario, así como los campos predeterminados de Nombre de usuario
  Dirección de correo electrónico, Nombre, Apellido y Estado del personal.

Para controlar los campos listados aquí se utiliza `list_display`. Sin embargo, para editar y añadir nuevos campos personalizados, como la edad, debemos añadir también `fieldsets`.

FICHERO: `accounts/admin.py`
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'age', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('age',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields':('age',)}),)


admin.site.register(CustomUser, CustomUserAdmin)
```
- Actualizar la página y ver el resultado

## 9.5. Conclusión
Con el modelo de usuario personalizado completo, ahora podemos centrarnos en construir el resto de la aplicación *Newspaper*.



|\/| [- |\| ~|~ [- ( /\ ~|~ () ^/_ '|