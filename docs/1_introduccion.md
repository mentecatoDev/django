# 1 Introducción

- Aprendizaje basado en proyectos 
    - 5 Proyectos progresivos
- Libre y Open Source
- Lo que hace que Django sea impresionante es su filosofía de "viene en la caja" ó "pilas incluidas" (*"comes with the box"* ó *"batteries-included"*). Permite una rápida implementación porque las partes más importantes ya están allí.
- Robusto 
    - Instagram, Pinterest (Flask; más personalizable y adecuado para  API's), Bitbucker, Disqus, Nasa, Mozilla Firefox, Onion, Mahalo, The  Washington Post, Eventbrite
- Se usará `pipenv`

## 1.1 Por qué Django *"comes with the box"* ó *"batteries-included"*

- La mayoría de los sites usan las mismas funcionalidades básicas 
    - Autenticación de usuarios
    - Conexión a bases de datos
    - Rutas
    - Contenidos de una página
    - Gestión de la seguridad
    - Interfaz de administración
    - etc.
- Hay que centrarse en **nuevas** funcionalidades: no reinventar la rueda.
- Django abraza el "batteries-included" frente a la aproximación "microframework" (Flask). 
    - Menos flexible pero también menos tendente al error (Django) frente a más personalizable y simple (Flask).
- Es un entorno muy maduro (2005).
- Aprendamos de las mejores prácticas.

## 1.2 Por qué unos apuntes

- Django está bien [documentado](https://docs.djangoproject.com/es/2.2/) pero es difícil de abordar para el principiante
- Incluso el [tutorial básico](https://docs.djangoproject.com/es/2.2/intro/tutorial01/) es notablemente arduo
- El problema viene de que está orientado a la **profundidad** y no a la **facilidad de uso**
- Aunque no es estrictamente necesario, se recomienda tener conocimientos sobre Python, HTML y CSS

## 1.3 Estructura

 1.Configuración inicial 

- Django 2.2 (3.0.2?)
- Python 3.8
- Pipenv
- Visual Studio Codium
- Terminal

 2.Aplicación "Hello World" 

- Configuración de un proyecto Django
- Git/GitLab (BitBucker?)

 3.Aplicación "Pages" 

- Don't Repeat Yourserlf (DRY)
- Platform as a service (PaaS): Heroku?

 4.Aplicación "Message Board" 

- Bases de datos: ORM
- Test
- Bitbucker?
- Heroku?

 5-7.Aplicación "Blog" 

- CRUD (Create-Read-Update-Delete)
- log in, log out, sign up

 8.Aplicación "Newspaper" 

- Concepto de "Custom user models"

 9.Autenticación de usuarios 

 10.Bootstrap 

 11-12.Reseteo y cambio de contraseñas vía email 

 13-15.Artículos y comentarios para "Newspaper" 

 16.Conclusión 

 Estamos preparados para empezar a aprender programación 