# 3 Hello World app

- Objetivo: Crear la típica aplicación "Hello World"

## 3.1 Configuración inicial

```
$ cd ~/Escritorio
$ mkdir helloworld
$ cd helloworld
$ pipenv install django
$ pipenv shell
(helloworld) $ django-admin startproject helloworld_project .
(helloworld) $ sudo apt install tree
(helloworld) $ tree
.
├── Pipfile
├── Pipfile.lock
├── helloworld_project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py

1 directory, 7 files
```

- `settings.py`: Controla la configuración del proyecto
- `urls.py`: Indica a Django qué páginas construir en respuesta a una petición de URL
- `wsgi.py`: (*Web Server Gateway Interface*) Punto de entrada para servidores web compatibles con WSGI para servir el proyecto.
- `asgi.py`: (*Asynchronous Server Gateway Interface*) Punto de entrada para servidores web compatibles con ASGI para servir el proyecto (nuevo en la versión 3.0).
- `manage.py`: Ejecuta varios comandos Django, como correr el servidor web local o crear una nueva **app**

```
(helloworld) $ python manage.py runserver
```

 Visitar: `http://localhost:8000`

## 3.2 Crear una **app**

- Un **proyecto** Django consta de una o más **apps**
- Cada **app** resuelve una funcionalidad concreta
- Crear la **app** `pages`

```
(helloworld) $ python manage.py startapp pages
(helloworld) $ tree
├── pages
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
```

- Nuevos FICHEROS 
  - `admin.py`: Es un fichero de configuración para la **app** incorporada al Admin de Django
  - `apps.py`: Es una fichero de configuración para la propia **app**
  - `migrations/`: Manteniene el seguimiento de cualquier cambio en el fichero `models.py` para que la *base de datos* y el fichero `models.py` estén sincronizados
  - `models.py`: Es donde se define el modelo de la base de datos que Django traduce en tablas dentro de la base de datos automáticamente.
  - `tests.py`: Es para los tests específicos de la **app**
  - `views.py`: Es donde se gestiona la lógica petición/respuesta (*request/response*) de la **app**
- Aunque la **app** existe, Django no sabe nada de ella hasta que explícitamente se la añadimos.
- Para incluir la app en el proyecto se necesita a;adir una referencia a su clase de configuración en la lista [`INSTALLED_APPS`](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-INSTALLED_APPS). La clase `PagesConfig` class está en el archivo `pages/apps.py` , por eso su *path* con puntos es `'pages.apps.PagesConfig'`.

 FICHERO: `settings.py` 

```
...
    # helloworld_project/settings.py
    INSTALLED_APPS = [
ç       'pages.apps.PagesConfig',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
...
```

- _Ojo, el **orden** importa; si varias aplicaciones intentan acceder al mismo recurso, la **app** que aparece primero tiene preferencia._

## 3.3 Vistas (Views) y configurariones de URL's (URLConfs)

- En *Django*, las vistas determinan qué contenido se muestra mientras que *URLConfs* indica dónde va ese contendio.

- URLConf utiliza una expresión regular para mapear las peticiones a la función apropiada de la vista que devuelve los datos correctos. 

    - La vista saca el texto `Hello, World` mientras que la url se asegurará de que cuando el usuario visita la página sea redireccionado a la vista correcta.

    - Cuando se escribe una URL, lo primero que ocurre dentro del proyecto *Django* es que se encuentra un patrón que coincide con la página de inicio (*homepage*). El `urlpattern` especifica una **vista**, que determinará el contenido de la página (normalmente desde una base de datos), y una **plantilla** (*template*) para darle estilo. El resultado final se devuelve al usuario como una respuesta HTTP.
<div class=text-center>
 URL -> View -> Model (típicamente) -> Template 
</div>

- Se empieza actualizando el fichero `views.py`

 FICHERO: `pages/views.py` 

```
    from django.shortcuts import render
ç   from django.http import HttpResponse

    # Create your views here.
ç   def homePageView(request):
ç       return HttpResponse("Hello, World!")
```

- Básicamente se indica que siempre que se llame a la función de la vista `homePageView` se devolverá el texto `“Hello, World!”` . 

  - Más específicamente se ha importado el método `HttpResponse` para poder devolver un objeto respuesta al usuario.

- Ahora a configurar *urls*. Crear un nuevo archivo `urls.py` dentro del directorio `pages`.

```
(helloworld) $ touch pages/urls.py
```

- Añadir el código

 FICHERO: `pages/urls.py` 

```python
ç # pages/urls.py
ç from django.urls import path

ç from .views import homePageView

ç urlpatterns = [
ç     path('', homePageView, name='home')
ç ]
```

- Importamos `path`
- `.views` utiliza "." para indicar el directorio actual
- El patrón `urlpattern` tiene tres partes:
    - Un expresión regular Python para la cadena vacía ''
    - Especifica la vista que se llamará: `homePageView`
    - Añade un nombre de URL opcional `home`
- Es decir, si el usuario requiere la pagina de inicio, representada por la cadena vacía, entonces utilizar la vista llamada `homePageView`
- El último paso es configurar el fichero `urls.py` a nivel de proyecto donde se recogen todas las **apps** dentro de un proyecto Django, dado que **cada una precisa de su propia ruta**.

 FICHERO: `helloworld_project/urls.py` 

```python
    from django.contrib import admin
ç   from django.urls import path, include
    urlpatterns = [
        path('admin/', admin.site.urls),
ç       path('', include('pages.urls')),
]
```

- Puede confundir un poco que no se necesite importar la app `pages` pero ya se hace referencia en `urlpatterns` como `pages.urls`.
    - La razón de hacerlo así es que el método `django.urls.include()` ya recibe un módulo, o **app**, como primer argumento. Así que, sin usar `include`, habría que importar la **app** `pages` pero, como sí que se usa, no se necesita a nivel de proyecto.

## 3.4 Resumen

### 1.- CREAR APP 

```bash
(helloworld) $ python manage.py startapp pages
```

### 2.- INFORMAR DE LA NUEVA APP 

 FICHERO: `settings.py` 

```python
...
    INSTALLED_APPS = [
ç       'pages.apps.PagesConfig',
...
```

### 3.- CREAR LA VISTA 

 FICHERO: `pages/views.py` 

```python
    from django.shortcuts import render
ç   from django.http import HttpResponse

    # Create your views here.
ç   def homePageView(request):
ç       return HttpResponse("Hello, World!")
```

### 4.- CREAR EL FICHERO DE RUTAS DE LA APP 

 FICHERO: `pages/urls.py` 

```python
ç from django.urls import path
ç from .views import homePageView
ç urlpatterns = [
ç     path('', homePageView, name='home')
ç ]
```

### 5.- INCLUIR EL FICHERO DE RUTAS DE LA APP EN EL PRINCIPAL 

 FICHERO: `helloworld_project/urls.py` 

```python
    from django.contrib import admin
ç   from django.urls import path, include
    urlpatterns = [
        path('admin/', admin.site.urls),
ç       path('', include('pages.urls')),
]
```
