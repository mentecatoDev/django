# 13. Correo electrónico

Ahora se quiere que los correos electrónicos se envíen realmente a los usuarios, no sólo a la consola de línea de comandos.

Se precisa de una *SendGrid* y actualizar los archivos `settings.py`. Django se encargará del resto.

## 13.1. SendGrid

[*SendGrid*](https://sendgrid.com/) es un servicio popular para el envío de e-mails transaccionales. A Django no le importa el servicio que se elija; se puede usar también [*MailGun*](https://www.mailgun.com/) o cualquier otro servicio con la misma facilidad.

- En la página de inicio de *SendGrid*, hacer clic en "[Start for Free](https://signup.sendgrid.com/)".
- Registrarse para obtener su cuenta gratuita en la siguiente página.
- Asegurarse de que la cuenta de correo electrónico que se utiliza para *SendGrid* **no sea la misma cuenta de correo electrónico que se tiene para la cuenta de superusuario** en el proyecto de Newspaper o pueden suceder errores extraños.
- Luego de confirmar la nueva cuenta a través de un correo electrónico, se pedirá que se ingrese y nos llevará a la página del panel de control de *SendGrid*.
- Ahora podemos configurar el código Django en el archivo `settings.py`. Primero se actualizará el backend de correo electrónico para usar SMTP.

FICHERO: `newspaper_project/settings.py`
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
- Luego, justo debajo, agregar las siguientes cinco líneas de configuración de correo electrónico. Tener en cuenta que lo ideal sería almacenar información segura como la contraseña en variables de entorno, pero no estamos aquí para mantener las cosas simples.


FICHERO: `newspaper_project/settings.py`
```python
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'sendgrid_username'
EMAIL_HOST_PASSWORD = 'sendgrid_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
- Asegúrarse de usar el nombre de usuario SendGrid para EMAIL_HOST_USER y
la contraseña de EMAIL_HOST_PASSWORD.
- Eso es todo.

## 13.2. Correos electrónicos personalizados

- Utilizar la barra de búsqueda de [Github](https://github.com/django/django) e introducir algunas palabras del texto del correo electrónico. Si se escribe "*You're receiving this email because*" se terminará en una página muy concreta de Github.
- El primer resultado es el que se desea. Muestra que el código se encuentra en `django/contrib/admin/templates/registration/password_reset_email.html`. Eso significa que en la app `contrib` el archivo que queremos se llama `password_reset_email.html`.

Aquí está el texto por defecto del código fuente de Django.
```html
{% load i18n %}{% autoescape off %}
{% blocktrans %}You're receiving this email because you requested a password reset for your user account at {{ site_name }}.{% endblocktrans %}

{% trans "Please go to the following page and choose a new password:" %}
{% block reset_link %}
{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
{% endblock %}
{% trans "Your username, in case you've forgotten:" %} {{ user.get_username }}

{% trans "Thanks for using our site!" %}

{% blocktrans %}The {{ site_name }} team{% endblocktrans %}

{% endautoescape %}
```
- Para cambiarlo, se necesita crear un nuevo archivo `password_reset_email.html` en la carpeta `registration`.

```bash
(news) $ touch templates/registration/password_reset_email.html
```
- Usar el siguiente código que ajusta lo que Django proporcionó por defecto.

FICHERO: `templates/registration/password_reset_email.html`
```html
{% load i18n %}{% autoescape off %}
{% trans "Hi" %} {{ user.get_username }},

{% trans "We've received a request to reset your password. If you didn't make this request, you can safely ignore this email. Otherwise, click the button below to reset your password." %}

{% block reset_link %}
{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
{% endblock %}
{% endautoescape %}
```
- Arriba se carga la etiqueta de la plantilla i18n lo que significa que este texto puede ser traducido a varios idiomas. Django tiene un sólido soporte de internacionalización aunque cubrirlo está fuera de nuestro alcance, por ahora.
- Se saluda al usuario por su nombre gracias a `user.get_username`. Luego se usa el bloque `reset_link` incorporado para incluir el enlace URL personalizado.
- También se actualiza el título del asunto del correo electrónico. Para ello, se crea un nuevo archivo `templates/registration/password_reset_subject.txt`.
```bash
(news) $ touch templates/registration/password_reset_subject.txt
```
- Luego agregar la siguiente línea de código al archivo `password_reset_subject.txt`.

```text
Please reset your password
```

## 13.3. Conclusión

Se ha terminado de implementar un flujo de autenticación de usuario completo. Los usuarios pueden ingresar una nueva cuenta, iniciar sesión, cerrar sesión, cambiar contraseña y restablecerla.

