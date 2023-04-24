:: yy05xxx1 ::
¿Por qué utilizamos el "." en el comando "django-admin startproject test_project ."?
{
~%-25% Si no se usa, el comando no funciona
= Si no se usa el "." aparecerá una redundante y molesta estructura de directorios
~%-25% Es parte de la sintaxis del comando
~%-25% No se utiliza, es mentira
}

:: yy05xxx2 ::
¿Cómo instalamos django?
{
~%-25% poetry django
~%-25% poetry install django
~%-25% Django viene instalado con poetry de serie, no hace falta
= poetry add django
}

:: yy05xxx3 ::
¿Qué se usa para arrancar el servidor?
{
~%-25% poetry manage.py runserver
~%-25% poetry manage
~%-25% poetry runserver
= python manage.py runserver
}

:: yy05xxx4 ::
¿Como se inicia una aplicación?
{
~%-25% poetry manage.py startapp
~%-25% poetry new app
~%-25% poetry manage.py startapp pages
= python manage.py startapp lol
}
