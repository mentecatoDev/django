:: DJ011 ::
En el fichero `settings.py` se pueden añadir aplicaciones ...
{
= Incluyendo la aplicación en la lista `INSTALLED_APPS`
~%-25% Incluyendo la aplicación en la lista `MIDDLEWARE`
~%-25% Incluyendo la aplicación en la lista `TEMPLATES`
~%-25% Incluyendo la aplicación en el diccionario `DATABASES`
}

:: DJ012 ::
Cuando se crea un apliación de Django dentro de un proyecto utilizando la línea de comandos se crean los ficheros:
{
= `admin.py`, `apps.py`, `migrations/`, `models.py`, `tests.py`, `views.py`
~%-25% `admin.py`, `migrations/`, `settings.py`, `models.py`, `tests.py`, `views.py`
~%-25% `admin.py`, `apps.py`, `models.py`, `tests.py`, `views.py`
~%-25% `admin.py`, `apps.py`, `models.py`, `views.py`
}

:: DJ013 ::
Las vistas de Django ...
{
= Se pueden crear usando funciones o clases
~%-25% Solo se pueden crear utilizando funciones
~%-25% Solo se pueden crear utilizando clases
~%-25% Son un fichero de HTML
}

:: DJ014 ::
En Django, cuando usamos `{% csrf_token %}`
{
= Lo hacemos en un formulario, así se evitan ataques de `cross-site scripting`
~%-25% Se utiliza antes de poner un enlace
~%-25% Solo hay que incluirlo en formularios con información sensible
~%-25% Se debe incluir en todos los formularios para evitar ataques basados en `SQL injection`
}
