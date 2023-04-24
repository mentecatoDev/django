:: DJ041 ::
¿Para qué se utiliza la función include() en el archivo urls.py de una aplicación Django?
{
  ~%-25% Para incluir una plantilla HTML en una vista
  ~%-25% Define la interfaz de usuario de la aplicación.
  = Para incluir las URL de otra aplicación Django en el archivo urls.py de una aplicación
  ~%-25% Para incluir un archivo CSS en una plantilla
}

:: DJ042 ::
¿Qué significa el error "There are unapplied migrations" en Django?
{
  ~%-25% Significa que se ha producido un error en el archivo settings.py y que se deben corregir las variables de configuración.
  ~%-25% Significa que se ha producido un error en la base de datos y que se deben eliminar las migraciones no aplicadas.
  ~%-25% Significa que se han realizado cambios en la base de datos manualmente y que las migraciones no están sincronizadas con la base de datos.
  = Significa que se han realizado cambios en el modelo de datos pero que las migraciones correspondientes aún no se han aplicado a la base de datos.
}

:: DJ043 ::
¿Cómo se pueden aplicar las migraciones pendientes en Django?
{
  = Ejecutando el comando "python manage.py migrate" en la terminal.
  ~%-25% Ejecutando el comando "python manage.py makemigrations" en la terminal.
  ~%-25% Eliminando todas las migraciones no aplicadas y creando una nueva migración desde cero.
  ~%-25% Actualizando el archivo settings.py con las nuevas configuraciones de migración.
}

:: DJ044 ::
¿Cómo se configura el directorio de templates en Django?
{
  ~%-25% Creando una nueva aplicación Django y definiendo el directorio de templates en el archivo urls.py.
  ~%-25% Creando una variable de entorno "TEMPLATES_DIR" y asignándole la ruta del directorio de templates en el archivo settings.py.
  ~%-25% Creando una nueva carpeta "templates" dentro de la aplicación y definiéndola en el archivo views.py.
  = Creando una nueva carpeta "templates" en el proyecto y definiéndo su ruta en el archivo settings.py, en el objeto "TEMPLATES", en la propiedad "DIRS".
}
