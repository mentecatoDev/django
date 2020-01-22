# 2 Configuración inicial

- Objetivos 
    - Configurar el entorno para programar en proyectos Django
    - Uso de la línea de comandos para instalar: 
        - Django 2.2 (3.0.2)
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

- Entornos Virtuales
- [Instrucciones de instalación desde los ficheros fuentes](https://solarianprogrammer.com/2017/06/30/building-python-ubuntu-wsl-debian/)

## 2.3 Entornos Virtuales

- Ver: https://mentecatodev.github.io/intermezzo/entornos_virtuales/

## 2.4 Instalación de Django

```
$ cd ~/Escritorio
$ mkdir django
$ cd django
$ pipenv install django
$ pipenv shell
```

- Crear nuevo proyecto `test`. No olvidar el "." al final.

```
django-admin startproject test_project .
```

- Si no se usa el "." aparecerá la siguiente estructura

```
└──test_project
   ├── manage.py
   └── test_project
       ├── __init__.py
       ├── settings.py
       ├── urls.py
       └── wsgi.py
```

- Arrancando el servidor

```
$ python manage.py runserver
```

- Escribir en el navegador la url `http://127.0.0.1:8000/` o `http://localhost:8000`
- `<Ctrl>-c` para parar
- `exit` para salir del entorno virtual

## 2.5 Instalar Git

```
$ sudo apt install git
$ git config --global user.name "<Nombre>"
$ git config --globar user.email "<Correo electrónico>"
```

## 2.6 Editores de texto

- Emacs ó Vim
- Code-OSS ó Visual Studio Codium
- PyCharm

## 2.7 Conclusión