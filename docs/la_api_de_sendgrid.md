# La API de SendGrid

Existen varias formas empezar con la API de SendGrid:

## 1. Prerrequisitos para enviar el primer email con la API de SendGrid

Estas instrucciones describen cómo enviar un correo electrónico usando llamadas cURL. Esta es una de las muchas maneras de enviar un correo electrónico con la API de SendGrid - también existen bibliotecas [PHP](https://github.com/sendgrid/sendgrid-php), [Python](https://github.com/sendgrid/sendgrid-python), [Node.js](https://github.com/sendgrid/sendgrid-nodejs), [Java](https://github.com/sendgrid/sendgrid-java), [C#](https://github.com/sendgrid/sendgrid-csharp), [Go](https://github.com/sendgrid/sendgrid-go), y [Ruby](https://github.com/sendgrid/sendgrid-ruby).

Antes de empezar a usar la API, hay que hacer lo siguiente:

1. Crear una [cuenta](https://sendgrid.com/pricing/) de SendGrid.
2. Crear una [Clave API](https://app.sendgrid.com/settings/api_keys).
3. Asegúrarse de tener [curl](https://curl.haxx.se/) instalado en la máquina.

## 2. Cómo enviar un correo electrónico con la API

### 2.1. Crear la llamada a la API

La llamada a la API debe tener los siguientes componentes:

- Un *Host*. El host para las solicitudes de la API v3 de la Web siempre es `https://api.sendgrid.com/v3/`
- Un [Authorization Header](https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-authentication#authorization-header) (encabezado de autorización)
- Una [API Key](https://app.sendgrid.com/settings/api_keys) dentro del encabezado de autorización
- Una petición. Cuando se envían datos a un recurso a través de POST o PUT, debe enviar toda la carga en JSON.

> Nota.- Límite del tamaño del mensaje: El tamaño total del mensaje no debe exceder los 20MB.  Esto incluye el mensaje en sí mismo, los encabezados y el tamaño combinado de los archivos adjuntos.

### 2.2. Envío del correo electrónico usando la API

*Para enviar un correo electrónico usando el SendGrid API:*

```texto
curl --request POST \
--url https://api.sendgrid.com/v3/mail/send \
--header 'authorization: Bearer <<YOUR_API_KEY>>' \
--header 'content-type: application/json' \
--data '{"personalizations":[{"to":[{"email":"john.doe@example.com","name":"John Doe"}],"subject":"Hello, World!"}],"content": [{"type": "text/plain", "value": "Heya!"}],"from":{"email":"sam.smith@example.com","name":"Sam Smith"},"reply_to":{"email":"sam.smith@example.com","name":"Sam Smith"}}'
```

1. Copiar el ejemplo de arriba de *curl*
2. Pegar la llamada *curl*  en un editor de texto.
3. Copiar la API key y pegarla en el encabezado de la autorización.
4. En la sección de datos, especificar los nombres y las direcciones de correo electrónico de "destino", "procedencia" y "respuesta" e introducir un asunto.
5. Copiar el código y pegarlo en el terminal.
6. Presionar **Enter**.
7. Revisar la bandeja de entrada de la dirección que se especificó como "to" el correo electrónico para ver el mensaje

Si aún no se ha configurado la [autenticación del remitente](https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/) en la cuenta, es posible que se tenga que comprobar en la carpeta de correo basura el correo electrónico que acaba de enviar.

### 2.3. Mensajes de respuesta de la API

Todas las respuestas se devuelven en formato JSON. Se especifica enviando el encabezado `Content-Type`. La Web API v3 proporciona una selección de [códigos de respuesta](https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-responses#status-codes), [content-type headers](https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-responses#content-type-header), y opciones de  [paginación](https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-responses#pagination) para ayudar a interpretar las respuestas a las solicitudes de API.

## 3. A continuación...

Para más información sobre SendGrid y dónde se puede ir desde aquí, revisar las páginas:

- [Referencia API](https://sendgrid.com/docs/api-reference/)

- [Autenticación del remitente](https://sendgrid.com/docs/ui/account-and-settings/how-to-set-up-domain-authentication/)

- [Automatización de subusuarios](https://sendgrid.com/docs/for-developers/sending-email/automating-subusers/)

- [Crear una app django para enviar email con SendGrid](https://github.com/sendgrid/sendgrid-python/blob/master/use_cases/django.md)