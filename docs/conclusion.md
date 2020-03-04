# Conclusión
¡Felicidades por terminar Django para principiantes! Después de empezar desde cero, hemos construido cinco aplicaciones web diferentes desde cero. Y hemos cubierto todas las características principales de Django: plantillas, vistas, urls, usuarios, modelos, seguridad, pruebas y despliegue. Ahora tienes el conocimiento para salir y construir tus propios sitios web modernos con Django.
Como con cualquier habilidad nueva, es importante practicar y aplicar lo que acabas de aprender. La funcionalidad de CRUD en nuestros sitios de blog y periódicos es común en muchas, muchas otras aplicaciones web. Por ejemplo, ¿puedes hacer una aplicación web de Todo List? Ya tienes todas las herramientas que necesitas.
El desarrollo web es un campo muy profundo y todavía hay mucho más que aprender sobre lo que Django tiene que ofrecer. Por ejemplo, un proyecto Django más avanzado probablemente usaría múltiples archivos de configuración, variables de entorno y PostgreSQL localmente en lugar de SQLite. Incluso podría utilizar paquetes de terceros como django-allauth para la autenticación social, django-debug-toolbar para la depuración, y django-extensions para las ventajas adicionales.
La mejor manera de aprender más sobre Django y el desarrollo web en general es pensar en un proyecto que quieras construir y luego aprender paso a paso lo que necesitas para completarlo. Un recurso adicional que puede ayudarte es DjangoX, que es un proyecto de inicio en el mundo real que cuenta con autenticación social y más.
También puedes suscribirte al boletín de Django para principiantes para recibir actualizaciones periódicas sobre nuevos contenidos y descuentos en futuros libros.
Y un último recurso es mi propio sitio web personal, wsvincent.com, que se actualiza regularmente y ya presenta artículos sobre algunas de estas técnicas avanzadas:

- Autenticación social Django
- Mega-tutorial de acceso a Django
- Django, PostgreSQL y Docker
- Tutorial del marco de descanso de Django
- Marco de descanso de Django con React

Recursos de Django
Para continuar aprendiendo Django, recomiendo trabajar a través de los siguientes tutoriales gratuitos en línea:
- Tutorial de encuestas oficiales
- Tutorial de las chicas de Django
- MDN: Marco Web Django
- Una completa guía para principiantes de Django
También recomiendo encarecidamente Two Scoops of Django 1.11: Best Practices for the Django Web Framework, que es la actual biblia de mejores prácticas para los desarrolladores de Django.
Libros de Python
Si eres nuevo en Python, hay varios libros excelentes disponibles para principiantes y avanzados Pythonistas:
- Python Crash Course es una fantástica introducción a Python que también te lleva a través de tres proyectos del mundo real, incluyendo una aplicación de Django.
- Think Python introduce los fundamentos de Python y de la informática en el
al mismo tiempo.
- Automatizar las cosas aburridas es otra gran guía para aprender y usar Python en el mundo real.
- La Guía del autoestopista para Python cubre las mejores prácticas en la programación de Python.
- Python Tricks demuestra cómo escribir código python.
- Effective Python es una excelente guía no sólo para Python sino para la programación en general.
- Fluent Python es asombroso y proporciona un profundo entendimiento del lenguaje Python.
Blogs a seguir
Estos sitios proporcionan escritos regulares de alta calidad sobre Python y el desarrollo de la web.
- Real Python
- Dan Bader
- Trey Hunner
- Pila completa de pitón
- Ned Batchelder
- Armin Ronacher
- Kenneth Reitz
- Daniel Greenfeld
Comentarios
Si has conseguido terminar el libro entero, me encantaría escuchar tus pensamientos. ¿Qué te gustó o no te gustó? ¿Qué áreas fueron especialmente difíciles? ¿Y qué nuevo contenido te gustaría ver? Me pueden contactar en will@wsvincent.com.

# Conclusion 2
Building a “professional” website is no small task even with all the help that a batteries-
included web framework like Django provides. Docker provides a major advantage in
standardizing both local and production environments regardless of local machine–
and especially in a team context. However Docker is a complicated beast on its own.
While we have used it judiciously in this book there is much more that it can do
depending on the needs of a project.
Django itself is friendly to small projects because its defaults emphasize rapid local
development but these settings must be systematically updated for production, from
upgrading the database to PostgreSQL, using a custom user model, environment
variables, configuring user registration flow, static assets, email...on and on it goes.
The good news is that the steps needed for a production-level approach are quite
similar. Hence the first half of this book is deliberately agnostic about the eventual
project that is built: you’ll find these steps are standard on almost any new Django
project. The second half focused on building a real Bookstore site with modern
best practices, added Reviews, image uploads, set permissions, configured payments
with Stripe, added search, reviewed performance and security measures, and finally
deployed on Heroku with containers.
For all the content covered in this book we’ve really only scratched the surface of what
Django can do. This is the nature of modern web development: constant iteration.
Django is a magnificent partner in building out a professional website because so
many of the considerations required have already been thought of and included. But
knowledge is needed to know how to turn these production switches on to take
full advantage of the customization Django allows. Ultimately that is the goal of this
Conclusion
 362
book: to expose you, the reader, to the full spectrum of what Django and professional
websites require.
As you learn more about web development and Django I’d urge caution when it comes
to premature optimization. It is always tempting to features and optimizations to your
project that you think you’ll need later. The short list includes adding a CDN for static
and media assets, judiciously analyzing database queries, adding indexes to models,
and so on.
The truth is that in any given web project there will always be more to do than
time allows. This book has covered the fundamentals that are worthy of upfront
time to get right. Additional steps around security, performance, and features will
present themselves to you in real-time. Try to resist the urge to add complexity until
absolutely necessary.
If you have feedback on this book or examples of what you’ve built as a result, I
read and respond to every email I receive at will@wsvincent.com377. I look forward
to hearing from you!