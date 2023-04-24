:: DJ092 ::
La creación del modelo de usuario personalizado requiere cuatro pasos:
{
~%-25% No se pueden crear.
~%-25% Crear un nuevo modelo CustomUser añadiendo un nuevo campo age, Actualizar settings.py.
~%-25%  Crear un nuevo modelo CustomUser añadiendo un nuevo campo age.
= Actualizar settings.py , Crear un nuevo modelo CustomUser añadiendo un nuevo campo age , Crear nuevos formularios para UserCreation y UserChangeForm , Actualizar la app admin.
}

:: DJ094 ::
¿Cómo crearemos un super usuario?
{
= (news) $ python manage.py createsuperuser
~%-25% No se puede crear
~%-25% (news) $ python manage.py migrate
~%-25% Todas las opciones son correctas.
}

:: DJ091 ::
 Modelo de usuario personalizado como haer el set up
{
~%-25% Todas son correctas
~%-25% $
= $ cd ~/Desktop ,$ mkdir news ,$ cd news ,$ pipenv install django ,$ pipenv shell , (news) $ django-admin startproject newspaper_project .,(news) $ python manage.py startapp accounts ,(news) $ python manage.py runserver
~%-25% django.contrib.admin
}

:: DJ093 ::
¿Pero cuáles son estos campos por defecto vistos en los apuntes entre otros?
{
~%-25% username, first_name, email,.
=  username, first_name, last_name, email, password, groups .
~%-25% No tiene nunguno por defecto.
~%-25% Todas son correctas.
}
