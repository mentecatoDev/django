# 2 Configuración inicial

- Objetivos 
  - Configurar el entorno para programar en proyectos Django
  - Uso de la línea de comandos para instalar: 
    - Django 3.0
    - Python 3.8
  - Git
  - Editor de texto

## 2.1 La línea de comandos

- Konsole, Tmux, zsh
- cd, cd .., ls, pwd, mkdir, touch
- Práctica: 
  - Recorrer los directorios del sistema, hacer una lista de ellos
  - Mostrar el directorio de trabajo
  - Crear un nuevo directorio y crear un fichero `index.html` en él
  - Listar el fichero: formato largo, ficheros ocultos
- Dónde aprender 
  - OpenWebinars
  - [Command Line Crash Course](https://learnpythonthehardway.org/book/appendixa.html)
  - [CodeAcademy's Course on the Command Line](https://www.codecademy.com/learn/learn-the-command-line)

## 2.2 Instalar Python 3

- [Entornos Virtuales](https://mentecatodev.github.io/intermezzo/entornos_virtuales/)

- [Instrucciones de instalación desde los ficheros fuentes](https://solarianprogrammer.com/2017/06/30/building-python-ubuntu-wsl-debian/)

- Python Path
  
  - **Python path** es la lista de directorios del sistema en donde Python buscará cuando se use la sentencia `import` de Python.
  
  - Por ejemplo, supongamos que el Python path tiene el valor 
    
```python
['', '/usr/lib/python2.4/site-packages', '/home/username/djcode/']
```

  - Si se ejecuta el código Python `from foo import bar`, Python, en primer lugar, se va a buscar el módulo `foo.py` en el directorio actual (la primera entrada en el Python path, una cadena de caracteres vacía, significa "el directorio actual"). Si ese archivo no existe, Python va a buscar el módulo en `/usr/lib/python2.4/site-packages/foo.py`. Si ese archivo no existe, entonces se probará en `/home/username/djcode/foo.py`. Finalmente, si ese archivo no existe, Python lanzará un `ImportError`.
  
  - Si se quiere ver el valor del Python path, abrir un intérprete interactivo de Python y escribir:
```python
>>> from sys import path
>>> print(path)`
```
  - Generalmente no hay que preocuparse de asigarle valores a "Python Path" — Python y Django se encargan automáticamente de hacer esas cosas entre bastidores. (Si se quiere curiosear, establecer el Python path es una de las cosas que hace el archivo `manage.py`).

## 2.3 Entornos Virtuales

- Ver: [Entornos Virtuales](https://mentecatodev.github.io/intermezzo/entornos_virtuales/)

## 2.4 Instalación de Django

```bash
$ cd ~/Escritorio
$ mkdir django
$ cd django
$ pipenv install django
$ pipenv shell
```

- Crear nuevo proyecto `test`. No olvidar el "." al final.

```bash
$ django-admin startproject test_project .
```

- Si no se usa el "." aparecerá la siguiente estructura de directorios que es molesta por, como se puede ver, lo redundante del directorio `test_project`:

```bash
└──test_project
   ├── manage.py
   └── test_project
       ├── __init__.py
       ├── settings.py
       ├── urls.py
       └── wsgi.py
```

- Arrancando el servidor

```bash
$ python manage.py runserver
```

- Escribir en el navegador la url `http://127.0.0.1:8000/` ó `http://localhost:8000`
- `<Ctrl>-c` para parar
- `exit` para salir del entorno virtual

### 2.5.1. Cambiando la IP de escucha y el puerto

De manera predeterminada, el comando `runserver` inicia el servidor de desarrollo en el puerto 8000 de la IP local.

Si se desea cambiar el puerto del servidor, hay que pasarlo como un argumento de línea de comandos. Por ejemplo, este comando inicia el servidor en el puerto 8080:

```bash
$ python manage.py runserver 8080
```

Si se desea cambiar la IP del servidor, ejecutar el comando con la IP seguida del puerto. Por ejemplo, para escuchar todas las IP públicas disponibles (lo cual es útil si se está ejecutando Vagrant o se desea mostrar la web en otras computadoras en la red), usar:

```bash
$ python manage.py runserver 0:8000
```

`0` es un atajo para `0.0.0.0`. Los documentos completos para el servidor de desarrollo se pueden encontrar en la [referencia del servidor de ejecución](https://docs.djangoproject.com/en/3.0/ref/django-admin/#runserver).

> Si se ejecuta este script como un usuario sin privilegios (recomendado), es posible que no se tenga acceso para iniciar en un puerto con un número bajo (puerto 80). Los números de puerto bajos están reservados para el superusuario (root).

## 2.5. Instalar Git

```bash
$ sudo apt install git
$ git config --global user.name "<Nombre>"
$ git config --globar user.email "<Correo electrónico>"
```

## 2.6. Editores de texto

- Emacs
- Vim ó Neovim
- Code-OSS ó VSCodium
- PyCharm

## 2.7. Borrar el proyecto

El proyecto no es más que una colección de ficheros bajo el directorio que hemos creado más el correspondiente entorno virtual que se ubicará, a menos que se especifique lo contrario, en el directorio `~/.local/share/virtualenvs/<directorio-código>`. Si se borra el proyecto, aún quedará pendiente borrar el entorno virtual que, si bien se puede hacer igualmente a mano, dispone del comando `pipenv --rm` para hacerlo desde el directorio del proyecto.

```bash
$ pipenv --rm
```

Una vez elminado el entorno virtual podemos proceder a borrar el proyecto, desde su directorio padre, usando el málefico comando: 

```bash
$ rm -rf <directorio del proyecto>
```

Las advertencias nunca serán suficientes para poner de manifiesto que ejecutar este comando de forma inadecuada (con derechos de administrador, utilizarndo wildcards, ubicado en el directorio incorrecto...) se podría acabar con el sistema al completo.
