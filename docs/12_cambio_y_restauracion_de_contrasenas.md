# 12. Cambio y Restauración de Contraseñas

Así como Django viene con vistas y urls incorporadas para el inicio y cierre de sesión, también viene con vistas/urls para el cambio y el restablecimiento de la contraseña.

## 12.1. Cambio de contraseña
Django proporciona una implementación predeterminada que ya funciona para este cometido.

Para probarlo:

- Hacer clic en el botón "Login" para asegurar que se ha iniciado sesión.
- Luego navegar a la página "Password change" en http://127.0.0.1:8000/users/password_change/
- Introducir la antigua contraseña y luego una nueva. Luego hacer clic en el botón "Change My Password".
- Se será redirigido a la página "Password change successful" ubicada en:
http://127.0.0.1:8000/users/password_change/done/.

## 12.2. Personalizar el cambio de contraseña
Se van a personalizar estas dos páginas de cambio de contraseña para que coincidan con el aspecto y la sensación del sitio del periódico.

Dado que Django ya ha creado las vistas y las URL, sólo hay que añadir nuevas plantillas.

Crear dos nuevos archivos de plantillas en la carpeta de registro.

```bash
(news) $ touch templates/registration/password_change_form.html
(news) $ touch templates/registration/password_change_done.html
```
Actualiza password_change_form.html con el siguiente código.

FICHERO: `templates/registration/password_change_form.html`
```html
{% extends 'base.html' %}

{% block title %}Password Change{% endblock %}

{% block content %}
  <h1>Password change</h1>
  <p>Please enter your old password, for security's sake, and then enter your new password twice so we can verify you typed it in correctly.</p>
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input class="btn btn-success" type="submit" value="Change my password">
  </form>
{% endblock %}
```
En la parte superior se extiende `base.html` y se fija el título de la página. Debido a que se usan títulos "blocks" en el archivo `base.html` se puede prescindir de ellos aquí. El formulario usa POST ya que se están enviando datos y un `csrf_token` por razones de seguridad. Usando `form.as_p` estamos simplemente mostrando en párrafos el contenido del formulario de restablecimiento de contraseña por defecto. Y finalmente incluimos un botón de envío que usa el estilo `btn btn-success` de Bootstrap para que sea verde.

Lo siguiente es la plantilla `password_change_done`.

FICHERO: `templates/registration/password_change_done.html`
```html
{% extends 'base.html' %}

{% block title %}Password Change Successful{% endblock %}

{% block content %}
  <h1>Password change successful</h1>
  <p>Your password was changed.</p>
{% endblock content %}
```

También se extiende `base.html` y se incluye un nuevo título. Sin embargo, no hay ningún formulario en la página, sólo texto nuevo.

La nueva página está en http://127.0.0.1:8000/users/password_change/done/.

## 12.3. Restablecer la contraseña

La única configuración que se requiere es decirle a Django cómo enviar los correos electrónicos. Después de todo, un usuario sólo puede restablecer una contraseña si se tiene acceso al correo electrónico vinculado a la cuenta. En la producción se usará el servicio de correo electrónico `SendGrid` para enviar realmente los correos electrónicos, pero para fines de prueba se puede confiar en la configuración del backend de la consola de Django que envía el texto del correo electrónico a la consola de línea de comandos en su lugar.

En la parte inferior del archivo `settings.py` hacer el siguiente cambio de una línea.

FICHERO: `newspaper_project/settings.py`
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Listo. Django se encargará del resto. Probar desde http://127.0.0.1:8000/users/password_reset/.

Asegurar que la dirección de correo electrónico coincida con una de las cuentas de usuario. Una vez enviado, se será redirigido a la página de restablecimiento de contraseña en http://127.0.0.1:8000/users/password_reset/done/ que informa de que se revise el correo electrónico. Ya que se le ha dicho a Django que envíe correos electrónicos a la consola de la línea de comando, el texto del correo electrónico estará ahora allí. Esto es lo que se muestra por consola:

``` text
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Password reset on 127.0.0.1:8000
From: webmaster@localhost
To: will@wsvincent.com
Date: Thu,22 Mar 2018 20:31:48 -0000
Message-ID: <152175070807.39206.18266082938043731152@1.0.0.127.in-addr.arpa>


You're receiving this email because you requested a password reset for your user account at 127.0.0.1:8000.

Please go to the following page and choose a new password:

http://127.0.0.1:8000/user/reset/MQ/4up-678712c114db2ead7780/

Your username, in case you've forgotten: wsv

Thanks for using our site!

The 127.0.0.1:8000 team
```
El texto del correo electrónico debe ser idéntico excepto por tres líneas:
- El "To:" en la sexta línea contiene la dirección de correo electrónico del usuario
- El enlace URL contiene una señal segura que Django genera aleatoriamente y puede ser usada sólo una vez
- Django recuerda amablemente el nombre de usuario

- El enlace proporcionado: http://127.0.0.1:8000/users/reset/MQ/4up-678712c114db2ead7780/, conduce a la "change password page".
- Introducir una nueva contraseña y hacer clic en el botón "Change my password". El paso final es ser redirigido a la página de "Password reset complete". 

Comprobar que todo ha funcionado, hacer clic en el enlace "Login" y usar la nueva contraseña.

## 12.4. Plantillas personalizadas

Sólo hay que crear nuevas plantillas para personalizar el aspecto y la sensación del restablecimiento de la contraseña.

Crear cuatro nuevos archivos de plantilla:

```bash
(news) $ touch templates/registration/password_reset_form.html
(news) $ touch templates/registration/password_reset_done.html
(news) $ touch templates/registration/password_reset_confirm.html
(news) $ touch templates/registration/password_reset_complete.html
```
Se empieza con el formulario de restablecimiento de contraseña que es `password_reset_form.html`.

FICHERO: `templates/registration/password_reset_form.html`
```html
{% extends 'base.html' %}

{% block title %}Forgot Your Password?{% endblock %}

{% block content %}
<h1>Forgot your password?</h1>
<p>Enter your email address below, and we'll email instructions for setting a new one.</p>
<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input class="btn btn-success" type="submit" value="Send me instructions!">
</form>
{% endblock %}
```
En la parte superior se extiende `base.html` y se fija el título de la página. Debido a que usamos títulos "block" en el `base.html` se pueden anular aquí.

- El formulario usa POST ya que se están enviando datos y un `csrf_token` por razones de seguridad.
- Al usar `form.as_p` simplemente se está mostrando en párrafos el contenido del formulario de restablecimiento de la contraseña predeterminada.
- Finalmente se incluye un enviar el botón y se usa el estilo de Bootstrap `btn btn-success` para hacerlo verde.

- Ahora se puede actualizar las otras tres páginas. Cada una tiene la misma forma de extender
`base.html`, un nuevo título, un nuevo texto de contenido, y para "password reset confirm" una actualización también.

FICHERO: `templates/registration/password_reset_done.html`
```html
{% extends 'base.html' %}

{% block title %}Email Sent{% endblock %}

{% block content %}
  <h1>Check your inbox.</h1>
  <p>We've emailed you instructions for setting your password. You should receive the email shortly!</p>
{% endblock %}
```
Confirmar los cambios en http://127.0.0.1:8000/users/password_reset/done/

A continuación, la página de confirmación del restablecimiento de la contraseña.

FICHERO: `templates/registration/password_reset_confirm.html`

```html
{% extends 'base.html' %}

{% block title %}Enter new password{% endblock %}

{% block content %}
<h1>Set a new password!</h1>
<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input class="btn btn-success" type="submit" value="Change my password">
</form>
{% endblock %}
```
Abrir la linea de comandos y tomar el enlace URL del correo electrónico enviado a la consola.

Finalmente aquí está el código completo para reestablecer el password.

FICHERO: `templates/registration/password_reset_complete.html`
```html
{% extends 'base.html' %}

{% block title %}Password reset complete{% endblock %}

{% block content %}
<h1>Password reset complete</h1>
<p>Your new password has been set. You can log in now on the <a href="{% url 'login' %}">log in page</a>.</p>
{% endblock %}
```
## 12.5. Conclusión
En el próximo capítulo se conectará *Newspaper* con el servicio de correo electrónico *SendGrid* para enviar realmente los correos electrónicos automatizados a los usuarios, en lugar de emitirlos en la consola de línea de comandos.