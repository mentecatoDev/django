# 19. PostgreSQL
Una de las diferencias más inmediatas entre trabajar en una "aplicación de juguete" en Django y una aplicación lista para producción es la base de datos. Django se suministra con [SQLite](https://sqlite.org/index.html) como opción predeterminada para el desarrollo local porque es pequeña, rápida y basada en archivos, lo que la hace fácil de usar. No se requiere ninguna instalación o configuración adicional.
Sin embargo, esta comodidad tiene un coste. En general, SQLite no es una buena elección de base de datos para sitios web profesionales. Por lo tanto, aunque está bien usar SQLite localmente mientras se hace un prototipo de una idea, es raro usar realmente SQLite como la base de datos en un proyecto de producción.
Django se suministra con soporte incorporado para [cuatro bases de datos](https://docs.djangoproject.com/es/3.0/ref/databases/): SQLite, PostgreSQL, MySQL y Oracle. Utilizaremos [PostgreSQL](https://www.postgresql.org/) en este libro ya que es la opción más popular para los desarrolladores de Django, sin embargo, la belleza del **ORM** de Django es que incluso si quisiéramos utilizar MySQL u Oracle, el código real de Django que escribamos será casi idéntico. El ORM de Django se encarga de la traducción del código Python a las bases de datos por uno, lo cual es bastante sorprendente si se piensa.
El reto de utilizar estas tres bases de datos es que cada una de ellas debe estar instalada y funcionar localmente si se quiere imitar fielmente un entorno de producción en la computadora local. ¡Y eso es lo que se quiere! Aunque Django se encarga de los detalles del cambio entre bases de datos, inevitablemente hay pequeños errores difíciles de detectar que pueden surgir si se utiliza SQLite para el desarrollo local, pero una base de datos diferente en producción.
Por lo tanto, la mejor práctica es usar la misma base de datos localmente y en producción.
Se comenzará un nuevo proyecto Django con una base de datos SQLite y luego se pasará a Docker y PostgreSQL.

## 19.1. Empezando

Crear un nuevo directorio `postgresql` para el nuevo código.

```bash
$ cd ..
$ mkdir postgresql && cd postgresql
```

Ahora instalar Django, iniciar el shell y crear un proyecto básico de Django llamado `postgresql_-project`. No olvidar el punto... ¡al final del comando!

```bash
$ pipenv install django
$ pipenv shell
(postgresql) $ django-admin startproject postgresql_project .
```

Hasta ahora todo bien. Ahora se puede migrar la base de datos para inicializarla y usar el servidor de ejecución para iniciar el servidor local.
> **NOTA**
>
> Normalmente no se recomienda ejecutar la migración en nuevos proyectos hasta que se haya configurado un **modelo de usuario personalizado**. De lo contrario, Django vinculará la base de datos al modelo de usuario incorporado, que es difícil de modificar más adelante en el proyecto. Se cubrirá esto adecuadamente más adelante, pero se está aquí principalmente con fines de demostración, usar el modelo de usuario por defecto aquí es una excepción por una vez.

```
(postgresql) $ python manage.py migrate
(postgresql) $ python manage.py runserver
```
Confirmar que todo funciona navegando a http://127.0.0.1:8000 en el navegador. Puede que se necesite refrescar la página, pero se debería ver la conocida página de bienvenida de Django.
Detener el servidor local con `<Control>+C` y luego usar el comando `ls` para listar todos los archivos y directorios.

```bash
(postresql) $ ls
Pipfile   Pipfile.lock   db.sqlite3   manage.py   postgresql_project
```
## 19.2. Docker

Para pasar a Docker, primero hay que salir del entorno virtual y luego crear un `Dockerfile`
y los archivos `docker-compose.yml` que controlarán la imagen y el contenedor Docker
respectivamente.

```bash
(postgresql) $ exit
$ touch Dockerfile
$ touch docker-compose.yml
```
El `Dockerfile` es el mismo del capítulo anterior.

```Dockerfile
# Pull base image
FROM python:3.8
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system
# Copy project
COPY . /code/
```
Go ahead and build the initial image now using the docker build . command.
Did you notice that the Dockerfile built an image much faster this time around? That’s
because Docker looks locally on your computer first for a specific image. If it doesn’t
find an image locally it will then download it. And since many of these images were
Chapter 2: PostgreSQL
 33
already on the computer from the previous chapter, Docker didn’t need to download
them all again!
Time now for the docker-compose.yml file which also matches what we saw previously
in Chapter 1.
```yml
docker-compose.yml
version: '3.8'
services:
web:
build: .
command: python /code/manage.py runserver 0.0.0.0:8000
volumes:
- .:/code
ports:
- 8000:8000
```
## 19.3. Modo Independiente

Ahora se pondrá en marcha el contenedor, pero esta vez en modo 'detached', lo que requiere la bandera `-d` o `-detach`.

```bash
$ docker-compose up -d
```

El modo independiente ejecuta los contenedores en [*background*](https://docs.docker.com/compose/reference/up/), lo que significa que se puede usar una unica consola de línea de comandos sin necesidad de abrir una separada. Esto ahorra tener que cambiar constantemente entre dos pestañas de línea de comandos. La desventaja es que si/cuando hay un error, la salida no siempre será visible. Así que si pantalla no coincide con lo descrito aquí, probar a escribir los logs de `docker-compose` para ver la salida actual y depurar cualquier problema.

Es probable que se vea una "Warning: Image for service web was built because it did not already exists" (Advertencia: La imagen para el servicio web se construyó porque no existía) al final del comando. Docker creó automáticamente una nueva imagen dentro del contenedor. Como se verá más adelante, es necesario añadir la bandera `--build` para forzar la construcción de una imagen cuando se actualizan los paquetes de software porque, de forma predeterminada, Docker buscará una copia local en la caché del software y utilizará la que mejore el rendimiento.

Para confirmar que las cosas funcionan correctamente, volver a http://127.0.0.1:8000/ en el navegador web.

Como ahora se está trabajando dentro de Docker en lugar de hacerlo localmente, se debe preceder los comandos tradicionales con `docker-compose exec [servicio]` donde se especifica el nombre del servicio. Por ejemplo, para crear una cuenta de superusuario en lugar de escribir `python manage.py createsuperuser`, el comando actualizado se vería ahora como la línea de abajo, usando el servicio web.

```bash
$ docker-compose exec web python manage.py createsuperuser
```
Como nombre de usuario elegir `sqliteadmin`, `sqliteadmin@email.com` como dirección de correo electrónico, y seleccionar una contraseña a discreción. navegue directamente al administrador en http://127.0.0.1:8000/admin e inicie sesión.

Será redirigido a la página principal del administrador. Notar en la esquina superior derecha que `sqliteadmin` es el nombre de usuario.

Si se hace clic en el botón `Users` se llega a la página de Usuarios donde se puede confirmar que sólo se ha creado un usuario.

Es importante destacar otro aspecto de Docker en este punto: hasta ahora se ha estado actualizando la base de datos, representada actualmente por el archivo `db.sqlite3`, dentro de Docker.
Eso significa que el archivo actual `db.sqlite3` está cambiando cada vez. Y gracias a los volúmenes montados en la configuración `docker-compose.yml` cada cambio en el archivo ha sido copiado en un archivo `db.sqlite3` en el ordenador local también. Se podría salir de Docker, iniciar el shell, iniciar el servidor con `python manage.py runserver`, y ver exactamente el mismo inicio de sesión de administrador en este punto porque la base de datos subyacente  SQLite es la misma.

## 19.4. PostgreSQL

Ahora es el momento de cambiar a PostgreSQL, que requiere tres pasos adicionales:

1.- Instalar un adaptador de base de datos, `psycopg2`, para que Python pueda hablar con PostgreSQL
2.- Actualizar la configuración de la BASE DE DATOS en nuestro archivo `settings.py`
3.- Instalar y ejecutar PostgreSQL localmente

¿Listo? Aquí vamos. Detener el contenedor Docker en marcha con `docker-compose down`.

```bash
$ docker-compose down
Stopping postgresql_web_1 ... done
Removing postgresql_web_1 ... done
Removing network postgresql_default
```

Entonces dentro del  archivo `docker-compose.yml` agregar un nuevo servicio llamado `db`. Esto significa que habrá dos servicios separados, cada uno un contenedor, corriendo dentro del  host Docker: `web` para el servidor local de Django y `db` para la base de datos PostgreSQL.
La versión PostgreSQL será fijada a la última versión, la 11. Si no se hubiera especificado un número de versión y en su lugar se hubiera usado sólo `postgres`, entonces seria descargada la última versión de PostgreSQL aunque, en una fecha posterior, sea Postgres 12, que probablemente tenga requerimientos diferentes.
Finalmente agregamos una línea de dependencias al servicio web ya que literalmente depende de la base de datos a ejecutar. Esto significa que `db` se iniciará antes que `web`.

FICHERO: `docker-compose.yml`
```yml
version: '3.7'
38
services:
web:
build: .
command: python /code/manage.py runserver 0.0.0.0:8000
volumes:
- .:/code
ports:
- 8000:8000
depends_on:
- db
db:
image: postgres:11
```
Ahora ejecutar `docker-compose up -d` que reconstruirá la imagen y hará ponerse en marcha a dos contenedores, uno ejecutando PostgreSQL dentro de `db` y el otro el servidor web Django.

```
$ docker-compose up -d
Creating network "postgresql_default" with the default driver
...
Creating postgresql_db_1 ... done
Creating postgresql_web_1 ... done
```

Es importante señalar en este punto que una base de datos de producción como PostgreSQL no está basada en archivos. Se ejecuta completamente dentro del servicio `db` y es efímero; cuando se ejecuta `docker-compose down` todos los datos dentro de ella se perderán. Esto contrasta con el código en el contenedor web que tiene un montaje de volúmenes para sincronizar el código local y el de Docker.
Próximamente se aprenderá cómo añadir un montaje de volúmenes para que en el servicio `db` persista la información de la base de datos.

## 19.5. Ajustes

Con el editor de texto, abrir el archivo `posgresql_project/settings.py` y bajar hasta la configuración de Bases de Datos. La configuración actual es esta:
```python
Code
# postgresql_project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Por defecto, Django especifica sqlite3 como motor de la base de datos, le da el nombre de `db.sqlite3`, y lo coloca en `BASE_DIR` que implica al directorio de nivel de proyecto.  Dado que la estructura del directorio es a menudo un punto de confusión, "nivel de proyecto" significa el directorio superior del proyecto que contiene a `postgresql_project`, `manage.py`, `Pipfile`, `Pipfile.lock`, y el archivo `db.slite3`.


```bash
(postgresql) $ ls
Dockerfile Pipfile.lock docker-compose.yml postgresql_project
Pipfile db.sqlite3 manage.py
```
Para cambiar a PostgreSQL actualizaremos la configuración de [ENGINE](https://docs.djangoproject.com/es/3.0/ref/settings/#engine). PostgreSQL requiere un NOMBRE, USUARIO, CONTRASEÑA, HOST y PUERTO.
Para mayor comodidad, configuraremos los tres primeros a postgres, el `HOST` a db que es el nombre de nuestro servicio establecido en `docker-compose.yml`, y el `PORT` a `5432` que es el predeterminado Puerto PostgreSQL.

```python
Code
# postgresql_project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}
```
Se verá un error si se refresca la página

¿Qué es lo que está pasando? Dado que se está ejecutando Docker en modo *detach* con la bandera `-d` no está claro inmediatamente. Es hora de revisar los *logs*.

```
$ docker-componer registros
...
web_1 | django.core.exceptions.ImproperlyConfigured: Error loading psycopg2
module: No module named 'psycopg2'
```
Habrá mucha salida pero en la parte inferior de la sección `web_1` se verán las líneas de arriba que indican que aún no se ha instalado el driver `psycopg2`.

## 19.5.Psycopg

PostgreSQL es una base de datos que puede ser utilizada por casi cualquier lenguaje de programación. Pero si se piensa, ¿cómo un lenguaje de programación, y todos ellos varían de alguna u otra menera, se conecta a la base de datos?
¡La respuesta es a través de un adaptador de base de datos! Y eso es lo que es [Psycopg](https://www.psycopg.org/), el adaptador de base de datos más popular para Python. Si quieres saber más sobre el funcionamiento de Psycopg, aquí tienes un [enlace a una descripción más completa en la página oficial](https://www.psycopg.org/docs/index.html).
Se puede instalar Pyscopg con Pipenv. En la línea de comandos, introducir el siguiente comando para que se instale en nuestro host Docker.

```bash
$ docker-compose exec web pipenv install psycopg2-binary==2.8.3
```
¿Por qué instalarse dentro de Docker en vez de localmente, nos preguntamos? La respuesta corta es que instalar consistentemente nuevos paquetes de software dentro de Docker y luego reconstruir la imagen desde cero nos salvará de potenciales conflictos de `Pipfile.lock`.
La generación de `Pipfile.lock` depende en gran medida del sistema operativo que se utilice. Se ha especificado todo el sistema operativo en Docker, incluyendo el uso de Python 3.8. Pero si se instala `psycopg2` localmente en el ordenador, que tiene un entorno diferente, el archivo `Pipfile.lock` resultante también será diferente. Pero entonces el montaje de los volúmenes en el archivo `docker-compose.yml`, que sincroniza automáticamente los sistemas de archivos locales y Docker, hará que el `Pipfile.lock` local sobreescriba la versión dentro de Docker. Así que ahora nuestro contenedor Docker intenta ejecutar un archivo `Pipfile.lock` incorrecto. Una forma de evitar estos problemas es instalar sistemáticamente nuevos paquetes de software en Docker en lugar de hacerlo localmente.
Si ahora  se actualiza la página web..... se seguirá viendo un error. Se revisan de nuevo los logs.

```bash
$ docker-compose logs
```
¡Es lo mismo que antes! ¿Por qué sucede esto? Docker almacena automáticamente las imágenes a menos que algo cambie por razones de rendimiento. Se quiere que reconstruya automáticamente la imagen con el nuevo `Pipfile` y `Pipfile.lock` pero porque la última línea del  `Dockerfile` es `COPY . /code/` sólo se copiarán los archivos; la imagen subyacente no se reconstruirá a sí misma a menos que la forcemos también. Esto puede hacerse añadiendo la bandera `--build`.

> Reconsiderar: siempre que se agregue un nuevo paquete primero instalarlo dentro de Docker, detener los contenedores, forzar una reconstrucción de la imagen, y luego iniciar los contenedores de nuevo.

```bash
$ docker-compose down
$ docker-compose up -d --build
```
Si se actualiza la página principal de nuevo la página de bienvenida de Django en http://127.0.0.1:8000/ ¡ahora funciona! Eso es porque Django se ha conectado con éxito a PostgreSQL a través de Docker.

## 19.6. Nueva base de datos

Sin embargo, ya que se está usando PostgreSQL ahora, no SQLite, la base de datos está vacía. Si se miran los registros actuales de nuevo escribiendo `docker-compose logs` se verán quejas como *"Tienes 15 migraciones no aplicadas"*.
Para reforzar este punto visitar *Admin* en http://127.0.0.1:8000/admin/ e iniciar sesión.
¿Funcionará nuestra anterior cuenta de superusuario de sqliteadmin?
¡No! Vemos *ProgrammingError at /admin* que se queja de que `auth_user` ni siquiera existe porque aún no se ha hecho la migración! Además, tampoco se tiene un superusuario en la base de datos PostgreSQL.
Para arreglar esta situación se puede tanto migrar como crear un superusuario dentro de Docker que acceda a la base de datos PostgreSQL.

```bash
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
```

¿Cómo se debería llamar al superusuario? Usemos `postgresadmin` y para propósitos de prueba poner el correo electrónico a `postgresadmin@email.com` y la contraseña.
En el navegador web navegar a la página de administración en http://127.0.0.1:8000/admin/  y entrar la información de acceso del nuevo superusuario.

En la esquina superior derecha se muestra que estamos conectados con postgresadmin ahora no sqliteadmin. También puede hacer clic en la pestaña de Usuarios en la página de inicio y visitar la sección de Usuarios para ver nuestro único usuario es la nueva cuenta de superusuario.

Recordar detener el contenedor en marcha con el `docker-compose down`.

```bash
$ docker-compose down
```
## 19.7. Git

Guardar los cambios de nuevo inicializando Git para este nuevo proyecto, añadir los cambios, e incluir un mensaje de confirmación.

```bash
$ git init
$ git status
$ git add .
$ git commit -m 'ch2'
```

## 19.8. Conclusión

El objetivo de este capítulo era demostrar cómo Docker y PostgreSQL trabajan juntos en un proyecto de Django. Cambiar entre una base de datos SQLite y un PostgreSQL es un salto mental para muchos desarrolladores inicialmente.
El punto clave es que con Docker ya no se necesita estar en un entorno virtual local. Docker es el nuevo entorno virtual... y la base de datos y más si se desea.
El host de Docker esencialmente reemplaza al sistema operativo local y dentro de él se pueden ejecutar múltiples contenedores, como para la aplicación web y para la base de datos, que pueden ser aislados y ejecutados por separado.