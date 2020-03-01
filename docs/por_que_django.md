# ¿Por qué Django?

Esta es la primera pregunta que los no iniciados casi siempre se hace cuando se les presenta Django:

- "¿Por qué debo aprender Django?"

- "¿Qué tiene Django que lo hace mejor que el Marco X o el lenguaje Y para construir aplicaciones web?"

Buena pregunta.

La programación, como la mayoría de las actividades creativas, tiene a mucha gente dedicada que lleva sus pasiones al extremo.

Es por esta razón que se debe desconfiar de las comparaciones entre este software y aquel.

El resultado final es que **todos los lenguajes de programación y las herramientas y marcos construidos sobre ellos tienen puntos buenos y malos**.

Cuando se trata de comparar Django con otros frameworks web,  la única comparación que vale la pena considerar es el **pragmatismo** vs. la perfección.

O para decirlo de otra manera, ¿quieres código estable y mantenible que puedas entregar en un plazo determinado? ¿O quieres una caja de magia arcana y una plantilla que haga que los profesores de la universidad te quieran y los que la mantienen te odien al mismo tiempo?

Django tiene sus asperezas, pero su enfoque pragmático para hacer las cosas es lo que realmente le destaca de la multitud. Django tiene muchos partidarios y unos cuantos enemigos, así que no dudar en sacar conclusiones propias.

## Las 10 mejores razones de Django

### 1. Python

Se puede decir que Python es el lenguaje de programación más fácil de aprender.

Con su uso de construcciones de lenguaje natural (por ejemplo, disposición y sangría parecida a la de un párrafo) y una sintaxis fácil de aprender, Python hace que la comprensión de la estructura y el flujo de los programas sea significativamente más fácil de aprender que otros lenguajes populares.

Esto se pone de manifiesto en el hecho de que la mayor proporción de cursos de programación introductoria en universidades e institutos de enseñanza superior utilizan ahora Python como el lenguaje elegido.

**Python es versátil**. Ejecuta sitios web y se utiliza en muchas aplicaciones de escritorio populares en PC y Mac. También se puede encontrar en aplicaciones móviles e incorporado en muchos dispositivos. Python también es un lenguaje de programación popular para otras aplicaciones.

Aprender Python casi seguro que servirá, sin importar la carrera que se elija.

**Python es popular**. Google, una de las empresas más grandes del mundo, utiliza Python en muchas de sus aplicaciones. También es usado ampliamente por programadores profesionales.

Algunos datos interesantes de la encuesta de desarrolladores de Stack Overflow de 2017:

- Python es el segundo en crecimiento en los últimos cinco años, después de node.js. PHP, Java y Ruby han disminuido en popularidad.
- Python es ahora más común que PHP.
- Python es el lenguaje más buscado entre todos los desarrolladores, saltando cuatro lugares desde 2016 y superando a JavaScript en el primer lugar.
- Los trabajos en Python pagan mejor que los tradicionales trabajos de Microsoft (C#, C++, VBA y .NET).

### 2. Baterías incluidas

Django hereda su filosofía de "pilas incluidas" de Python.

Esto se interpreta a menudo como que Django incluye muchas cosas extra que probablemente no se necesiten, sin embargo, la mejor analogía es que, en lugar de tener que abrir el lenguaje para insertar energía propia (baterías), sólo hay que pulsar el interruptor y Django hace el resto.

En términos prácticos esto significa que Django implementa algunos procesos comunes, pero complejos, proporcionando herramientas y envoltorios simples para ocultar la complejidad sin comprometer la potencia.

Las "baterías" de Django se encuentran en los *contrib packages* que son:

`admin`.- La aplicación de administración de Django
`auth`.- El marco de autenticación de Django
`contenttypes`.- Un marco para enganchar con los modelos Django
`flatpages`.-  Un marco para la gestión de las páginas de casos especiales, como las políticas del sitio y los términos y condiciones de uso
`gis`.- Añade capacidades geoespaciales a Django
`humanize`.- Añade filtros de plantilla para mejorar la legibilidad de los datos
`messages`.- Un marco para la gestión de los mensajes basados en sesiones y cookies
`postgres`.- Características específicas de la base de datos postgreSQL
`redirects`.- Gestión de redirecciones
`sessions`.- Un marco para la gestión de sesiones anónimas
`sites`.- Permite operar varios sitios web desde una sola instalación
`sitemaps`.- Implementa archivos *sitemap XML*
`syndication`.- Un marco para generar *feeds* para la sindicación

Los *contrib packages* pueden ser un poco complejos, sin embargo, Django proporciona una sólida lista de poderosos módulos incorporados para que no haya que crearlos.

### 3. No se interpone en tu camino

Cuando creas una aplicación Django, Django no agrega ningún tipo de funciones innecesarias. No hay importaciones obligatorias, no se requieren bibliotecas de terceros ni archivos de configuración XML.

Esto puede ser un poco aterrador cuando se crea un proyecto Django por primera vez, ya que las herramientas automáticas de Django (`startproject` y `startapp`) sólo crean un archivo de configuración básico, unas cuantas carpetas y algunos archivos de inicio casi vacíos.

Aunque esto pueda parecer algo malo, en realidad es un gran beneficio ya que Django proporciona una base sólida sobre la que se puede construir de la forma que se quiera.

El resultado es una mayor confianza en el código ya que se sabe que lo que sea que esté en la aplicación, se ha puesto ahí.

### 4. Administración incorporada

Desde el principio, Django proporciona una interfaz de administración (`admin`) para trabajar con los modelos y gestionar los usuarios, los permisos de usuario y los grupos.

La interfaz del modelo reemplaza inmediatamente la necesidad de un programa de administración de base de datos separado para todas las funciones de la base de datos, excepto las avanzadas.

Con cambios muy simples en la configuración de la administración, se puede organizar los campos del modelo, mostrar y ocultar campos, clasificar, filtrar y organizar los datos para maximizar la eficiencia.

El administrador también tiene una función opcional de documentación de modelos que proporciona una documentación automática de los mismos.

La administración de usuarios siempre es importante en un sitio Web moderno y Django proporciona todo lo que se espera: añadir y modificar usuarios, cambiar contraseñas, crear grupos de usuarios, asignar permisos y comunicarse con los usuarios.

Al igual que el resto de Django, el administrador también es personalizable y ampliable.

Por ejemplo, se pueden anular las plantillas de visualización del administrador y añadir nuevas funciones para tareas como la exportación de los datos del modelo a un archivo delimitado por comas (CSV).

### 5. Escalable
Django se basa en el patrón de diseño Modelo-Vista-Controlador (MVC). Esto significa que la base de datos, el código de programa (back-end) y el código de visualización (front-end) están separados.

Django lleva esta separación un paso más allá al separar el código de los medios estáticos -imágenes, archivos, CSS y JavaScript- que conforman tu sitio.

Estas filosofías de diseño permiten:

- Ejecutar servidores separados para la base de datos, las aplicaciones y los medios
- Tener fácilmente los medios servidos desde una Red de Entrega de Contenido (CDN)
- Cachear el contenido en múltiples niveles y alcances
- Para sitios realmente grandes, se puede emplear la agrupación y el equilibrio de carga para distribuir el sitio web entre varios servidores

Django es compatible con una serie de proveedores externos populares para servidores web, administración del rendimiento, almacenamiento en caché, agrupación en clústeres y balanceo.

También es compatible con las principales aplicaciones y servicios de correo electrónico y mensajería como OAuth y ReST.

### 6. Probado en el campo de batalla

Una buena forma de saber si un marco de trabajo en la web es robusto y fiable es averiguar cuánto tiempo ha estado en funcionamiento, si está creciendo y qué sitios de alto perfil lo están utilizando.

Django fue de fuentes abiertas por primera vez en 2005, después de haber funcionado durante varios años en el entorno de alta demanda de una organización de noticias.

Después de crecer desde el 2005, Django ahora no sólo corre en empresas de publicación de noticias como el Washington Post, sino que también dirige todas o parte de las principales empresas globales como Pinterest, Instagram, Disqus, Bitbucket, EventBrite y Zapier.

Django continúa creciendo en popularidad. [Djangosites](https://www.djangosites.org/) enumera más de 5200 sitios que usan Django, y eso es sólo para los sitios que se registran en Djangosites.

Sería imposible adivinar cuántas páginas sirve Django cada día en comparación con otras tecnologías de Internet, pero eso es en gran medida irrelevante: Django ha demostrado su valía en los últimos años gestionando algunos de los sitios de mayor tráfico de la Internet, y sigue aumentando su base de usuarios en la actualidad.

### 7. Paquetes, paquetes y más paquetes!

Casi todo lo que se quiera hacer con Django ya se ha hecho antes.

Muchos de la gran comunidad internacional de desarrolladores de Django lo devuelven liberando sus proyectos como paquetes de código abierto.

El mayor repositorio de estos proyectos se puede encontrar en el sitio [Django Packages](https://djangopackages.org/). A día de hoy, Django Packages enumera más de 3400 aplicaciones, sitios y herramientas reutilizables de Django para usar en proyectos propios. Un rápido recorrido por los paquetes más populares incluye:

+ **Wagtail, Mezzanine y django CMS**.- Sistemas de gestión de contenidos
+ **Cookiecutter**.- Configuración rápida y sencilla del proyecto Django y de las estructuras de las aplicaciones para aplicaciones más avanzadas
+ **Django ReST Framework**.-Implementa una API de ReST en Django
+ **Django allauth**.-Apps de autenticación de Facebook, GitHub, Google y Twitter
+ **Debug toolbar**.- Barra de herramientas de depuración que muestra la información de depuración a medida que el proyecto se ejecuta.
+ **Django Celery**.- Proporciona la integración con Celery para Django
+ **Oscar, Django Shop y Cartridge**.- eCommerce frameworks para Django (Cartridge es una extensión para Mezzanine CMS)

Con miles de paquetes más como estos, es muy probable que se encuentre un paquete que se adapte a unas necesidades específicas, sin tener que reinventar la rueda.

### 8. Desarrollado activamente

Uno de los mayores riesgos del código abierto es si hay suficiente interés en el proyecto para que atraiga el apoyo de los desarrolladores a largo plazo.

No existe tal riesgo con Django; no sólo el proyecto tiene más de 15 años de antigüedad, sino que tiene un largo historial de liberaciones constantes y sigue contando con el apoyo de una comunidad activa y un gran equipo básico de contribuyentes voluntarios que mantienen y mejoran la base del código todos los días.

Django tuvo su primera versión de producción en 2008 (versión 1.0) y ha tenido tres versiones de soporte a largo plazo (LTS): 1.4, 1.8, 1.11 y 2.2. La versión 2.2 LTS (la actual) tiene soporte completo hasta mediados de 2022.

El equipo de desarrollo de Django mantiene una [hoja de ruta de desarrollo](https://www.djangoproject.com/download/#supported-versions) en el sitio web del Proyecto Django y tiene un sólido historial de cumplimiento de los hitos de la hoja de ruta.

El Proyecto Django también cuenta con el apoyo de una fundación independiente, la Django Software Foundation, que es una organización sin ánimo de lucro registrada en los Estados Unidos.

### 9. Lanzamientos estables

Los proyectos de software de código abierto son, en muchos casos, desarrollados más activamente y más seguros que el software propietario de la competencia.

El inconveniente del desarrollo en constante evolución de un proyecto de software de código abierto es la falta de una base de código estable en la que basar el desarrollo comercial.

Django aborda este problema con versiones de apoyo a largo plazo (LTS) del software y un proceso de lanzamiento definido.

Las versiones LTS se lanzan con un período de soporte garantizado (normalmente de tres años). En este periodo se garantiza que la base del código permanezca estable; con parches para errores, seguridad y pérdida de datos 100% compatibles con la versión de la característica.

El proceso de lanzamiento de Django asegura que las versiones oficiales sean tan estables como sea posible. Tras una fase de desarrollo, cada versión entra en una fase Alfa en la que se aplica una congelación de características.

La nueva versión pasa entonces por las fases Beta y Candidata a la Liberación (RC Release Candidate), donde se trabajan los errores de la versión. Si no se encuentran errores importantes durante un período después de la versión candidata, se lanzará la versión final (feature release).

Después de que la versión final ha sido liberada, sólo se aplican correcciones de errores y parches de seguridad. Estos parches, como las versiones LTS, son 100% compatibles con la *feature release*.

### 10. Documentación de primera clase

Incluso en las primeras versiones, los desarrolladores de Django se aseguraron de que la documentación fuera completa y que los tutoriales fueran fáciles de seguir.

La documentación debería ser la razón número uno de esta lista porque fue la calidad de la documentación lo que en muchos casos prevalezca la elección de Django sobre otras opciones.

Django también cuenta con un fuerte apoyo de los miembros de la comunidad que producen materiales de aprendizaje gratuitos, libros, cursos pagados y gratuitos y muchos consejos, trucos y asistencia en sus sitios web.

Hay muchos grupos. Algunos de los más relevantes son:

+ [Tango con Django](https://www.tangowithdjango.com/)
+ Cualquier cosa de Danny y Audrey en [TwoScoops Press](https://www.roygreenfeld.com/)
+ [Django Girls](https://djangogirls.org/)

Por supuesto, también se van a descubrir cosas sobre Django que parezcan frustrantes pero, dado que todos los lenguajes de programación y los frameworks construidos sobre ellos tienen sus idiosincrasias, seguro que se descubrirá que cuando se trata de construir rápidamente sitios web seguros y escalables, los beneficios de Django superan con creces a sus desafíos.
