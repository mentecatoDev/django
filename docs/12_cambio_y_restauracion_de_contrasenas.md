# 12. Cambio y Restauración de Contraseñas

Así como Django viene con vistas y urls incorporadas para el inicio y cierre de sesión, también viene con vistas/urls para el cambio y el restablecimiento de la contraseña.

Inicialmente implementaremos las vistas y URLs integradas en Django tanto para el cambio de contraseña como para el cambio de contraseña antes de personalizarlas con nuestras propias plantillas y servicios de correo electrónico basados en Bootstrap.

## 12.1. Cambio de contraseña
Django proporciona una implementación predeterminada que ya funciona para este cometido.

Para probarlo:

- Hacer clic en el botón "Login" para asegurar que se ha iniciado sesión.
- Luego navegar a la página "Password change" en http://127.0.0.1:8000/accounts/password_change/
- Introducir la antigua contraseña y luego una nueva. Luego hacer clic en el botón "Change My Password".
- Se será redirigido a la página "Password change successful" ubicada en:
http://127.0.0.1:8000/accounts/password_change/done/.

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

{% block title %}Cambio de Contraseña{% endblock %}

{% block content %}
  <h1>Cambio de Contraseña</h1>
  <p>Introduzca su antigua contraseña, por seguridad, y luego la nueva dos veces para verificar que se ha escrito correctamente.</p>
  <form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input class="btn btn-success" type="submit" value="Cambiar Contraseña">
  </form>
{% endblock %}
```
En la parte superior se extiende `base.html` y se fija el título de la página. Debido a que se usan títulos "blocks" en el archivo `base.html` se puede prescindir de ellos aquí. El formulario usa POST ya que se están enviando datos y un `csrf_token` por razones de seguridad. Usando `form.as_p` estamos simplemente mostrando en párrafos el contenido del formulario de restablecimiento de contraseña por defecto. Y finalmente incluimos un botón de envío que usa el estilo `btn btn-success` de Bootstrap para que sea verde.

Lo siguiente es la plantilla `password_change_done`.

FICHERO: `templates/registration/password_change_done.html`
```html
{% extends 'base.html' %}

{% block title %}Cambio de Contraseña Exitoso{% endblock %}

{% block content %}
  <h1>Cambio de Contraseña exitoso</h1>
  <p>Su contraseña ha cambiado.</p>
{% endblock content %}
```

También se extiende `base.html` y se incluye un nuevo título. Sin embargo, no hay ningún formulario en la página, sólo texto nuevo.

La nueva página está en http://127.0.0.1:8000/accounts/password_change/done/.

## 12.3. Restablecer la contraseña

La única configuración que se requiere es decirle a Django cómo enviar los correos electrónicos. Después de todo, un usuario sólo puede restablecer una contraseña si se tiene acceso al correo electrónico vinculado a la cuenta. En producción se usará el servicio de correo electrónico `SendGrid` para enviar realmente los correos electrónicos, pero para fines de prueba se puede confiar en la configuración del backend de la consola de Django que envía el texto del correo electrónico a la consola de línea de comandos en su lugar.

En la parte inferior del archivo `settings.py` hacer el siguiente cambio de una línea.

FICHERO: `newspaper_project/settings.py`
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Listo. Django se encargará del resto. Probar desde http://127.0.0.1:8000/accounts/password_reset/.

Asegurar que la dirección de correo electrónico coincida con una de las cuentas de usuario. Una vez enviado, se será redirigido a la página de restablecimiento de contraseña en http://127.0.0.1:8000/accounts/password_reset/done/ que informa de que se revise el correo electrónico. Ya que se le ha dicho a Django que envíe correos electrónicos a la consola de la línea de comando, el texto del correo electrónico estará ahora allí. Esto es lo que se muestra por consola:

``` tex
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Subject: =?utf-8?q?Contrase=C3=B1a_restablecida_en_127=2E0=2E0=2E1=3A8000?=
From: webmaster@localhost
To: testuser2@gmail.com
Date: Wed, 24 Feb 2021 19:08:41 -0000
Message-ID: <161419372146.227460.6264007619116440451@padre>


Ha recibido este correo electrónico porque ha solicitado restablecer la contraseña para su cuenta en 127.0.0.1:8000.

Por favor, vaya a la página siguiente y escoja una nueva contraseña.

http://127.0.0.1:8000/accounts/reset/NA/ail96h-fc019327b99befed62950c6dc526e12b/

Su nombre de usuario, en caso de que lo haya olvidado: testuser2

¡Gracias por usar nuestro sitio!

El equipo de 127.0.0.1:8000
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

{% block title %}¿Olvidó su contraseña?{% endblock %}

{% block content %}
<h1>¿Olvidó su contraseña?</h1>
<p>Introduzca su dirección de correo electrónico y recibirá instrucciones para establecer una nueva.</p>
<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input class="btn btn-success" type="submit" value="¡Envíenme instrucciones!">
</form>
{% endblock content %}
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

{% block title %}Correo electrónico enviado{% endblock %}

{% block content %}
  <h1>Compruebe su buzón de correo electrónico</h1>
  <p>Se le ha enviado instrucciones para establecer su nueva contraseña.<br>
     ¡Debería recibir el correo electrónico en breve!.</p>
{% endblock content %}
```
Confirmar los cambios en http://127.0.0.1:8000/accounts/password_reset/done/

A continuación, la página de confirmación del restablecimiento de la contraseña.

FICHERO: `templates/registration/password_reset_confirm.html`

```html
{% extends 'base.html' %}

{% block title %}Introducir nueva contraseña{% endblock %}

{% block content %}
<h1>¡Establezca una nueva contraseña!</h1>
<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input class="btn btn-success" type="submit" value="Cambiar Contraseña">
</form>
{% endblock content %}
```
Abrir la linea de comandos y tomar el enlace URL del correo electrónico enviado a la consola.

Finalmente aquí está el código completo para restablecer el password.

FICHERO: `templates/registration/password_reset_complete.html`
```html
{% extends 'base.html' %}

{% block title %}Restablecimiento de la contraseña completo{% endblock %}

{% block content %}
<h1>Restablecimiento de la contraseña completo</h1>
<p>Su nueva contraseña se ha restablecido. Puede logarse ahora en la página de <a href="{% url 'login' %}">login</a>.</p>
{% endblock content %}
```
## 12.5. Conclusión
En el próximo capítulo se conectará *Newspaper* con el servicio de correo electrónico *SendGrid* para enviar realmente los correos electrónicos automatizados a los usuarios, en lugar de emitirlos en la consola de línea de comandos.