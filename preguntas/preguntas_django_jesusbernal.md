:: DJ031 ::
Si incluimos esta línea de código ‘from django.urls import path, include’ en nuestro archivo ‘urls.py’ de nuestro proyecto
{
~%-25% Nos permite devolver respuestas HTTP desde vistas en Django.
~%-25% Nos permite crear patrones de URL personalizados en nuestra aplicación y asociarlos con vistas específicas.
~%-25% Nos permite incluir patrones de URL personalizados de aplicaciones externas en nuestro proyecto.
= Nos permite crear patrones de URL personalizados y también incluir los de otras aplicaciones en nuestro proyecto.
}

:: DJ032 ::
¿Cómo crearemos una aplicación de nombre blog?
{
= python manage.py startapp blog
~%-25% python startapp __init__.py blog
~%-25% python startapp blog manage.py 
~%-25% Todas las opciones son correctas.
}

:: DJ033 ::
¿Qué archivo de tu proyecto Django se utiliza para ejecutar comandos?
{
~%-25% asgi.py
~%-25% wsgi
= manage.py
~%-25% settings.py
}

:: DJ034 ::
¿Para qué sirven las etiquetas ‘{% block %} {% endblock %}’?
{
~%-25% Es una etiqueta utilizada para heredar el contenido de una plantilla base y extenderla con contenido adicional en una nueva.
= Es una etiqueta utilizada en plantillas para definir una sección específica del contenido de una página, siendo reutilizada en otras páginas.
~%-25% Es una etiqueta utilizada para recorrer un objeto iterable y mostrar su contenido en la plantilla.
~%-25% Es una etiqueta utilizada para la protección de falsificación entre sitios de Django.
}
