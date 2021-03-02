# 16. Comentarios

- Dos maneras:
   - Crear una aplicación de comentarios dedicada y enlazarla a los artículos (sobreingeniería en este momento).
   - Añadir un modelo adicional llamado `Comment` a la aplicación de artículos y enlazarlo al modelo de Artículo a través de una clave foránea.
- Los usuarios también tendrán la posibilidad de dejar comentarios en los artículos de cualquier otro usuario.

## 16.1. Modelo
- Añadir otra tabla a nuestra base de datos existente llamada `Comment`.
    - Tendrá una relación de muchos a uno con clave primaria  `Article`: un artículo puede tener muchos comentarios, pero no al revés. Tradicionalmente el nombre del campo de la clave foránea es simplemente el modelo con el que se vincula, por lo que este campo se llamará `article`. Los otros dos campos serán `comment` y `author`.

FICHERO: `articles/models.py`
```python
`...`

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Artículo')
    comment = models.CharField(max_length=140, verbose_name='Comentario')
    author = models.ForeignKey(
        get_user_model(),         # ó settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        verbose_name='Autor'
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('article_list')

```
- El modelo `Comment` tiene un método `__str__` y un método `get_absolute_url` que regresa a la página principal `articles/`.
- Ya que se han actualizado los modelos, es hora de hacer un nuevo archivo de migración y luego aplicarlo.
    - Al añadir `articles` al final de cada comando, lo cual es opcional, estamos especificando que queremos usar sólo la aplicación de artículos. Esto es un buen hábito.
    - Por ejemplo, ¿qué pasaría si se hicieran cambios en los modelos de dos aplicaciones diferentes? Si no especificamos una aplicación, entonces los cambios de ambas aplicaciones se incorporarán en el mismo archivo de migraciones, lo que hace más difícil, en el futuro, depurar los errores. Manténgase cada migración tan pequeña y contenida como sea posible.

```bash
(news) $ python manage.py makemigrations articles
(news) $ python manage.py migrate
```

## 16.4 Admin
- Después de crear un nuevo modelo es bueno jugar con él en la aplicación de administración antes de mostrarlo en el sitio web real. Añadir el `Comment` al archivo `admin.py` para que sea visible.

FICHERO: `articles/admin.py`
```python
# articles/admin.py
from django.contrib import admin
from .models import Article, Comment # new

admin.site.register(Article)
admin.site.register(Comment) # new
```
- En este punto podríamos añadir un campo de administración adicional para ver el comentario y el artículo en la página de administración de Django. ¿Pero no sería mejor ver todos los modelos de `Comment` relacionados con un solo modelo `Post`? Resulta que sí, con una función de administración de Django llamada **inlines** que muestra las relaciones de claves externas de una manera más visual y agradable.
- Hay dos vistas **inlines** principales: `TabularInline` y `StackedInline`. La única diferencia entre las dos es el modelo para mostrar la información. En una `TabularInline` todos los campos del modelo aparecen en una línea mientras que en una `StackedInline` cada campo tiene su propia línea.
- Se implementarán las dos para decidir cuál se prefiere

FICHERO: `articles/admin.py`
```python
from django.contrib import admin
from .models import Article, Comment

class CommentInline(admin.StackedInline):  # new
	model = Comment

class ArticleAdmin(admin.ModelAdmin):      # new
	inlines = [
		CommentInline,
	]

admin.site.register(Article, ArticleAdmin) # new
admin.site.register(Comment)
```

- Se pueden ver y modificar todos los artículos y comentarios relacionados en un solo lugar.

- Note
  that by default, the Django admin will display 3 empty rows here. You can change the default
  number that appear with the extra field. So if you wanted no fields by default, the code would
  look like this:

- FICHERO: `articles/admin.py`

```python
class CommentInline(admin.StackedInline):
   model = Comment
   extra = 0 # new
```

- En caso de usar  `TabularInline` se muestra más información en menos espacio, lo cual es preferible. Para cambiar a él sólo hay que cambiar `CommentInline` de `admin.StackedInline` a `admin.TabularInline`.

FICHERO: `articles/admin.py`
```python
from django.contrib import admin
from .models import Article, Comment

class CommentInline(admin.TabularInline): # new
    model = Comment

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
```
- Ver lo cambios en la página de administración de Django: todos los campos de cada modelo se muestran en la misma línea.

## 16.5. Plantilla

- Dado que `Comment` vive dentro de la app `articles` existente, sólo necesitamos actualizar las plantillas existentes para `article_list.html` y `article_detail.html` para mostrar el nuevo contenido. No hay que crear nuevas plantillas y jugar con las urls y las vistas.
- Lo que se quiere hacer es mostrar **todos** los comentarios relacionados con un artículo específico. Esto se llama "query" ya que estamos pidiendo a la base de datos una información específica. En este caso, al trabajar con una clave rofánea, se busca seguir una relación hacia atrás: para cada `Article` buscar modelos de `Comment` relacionados.
- Django tiene una sintaxis incorporada que se puede usar conocida como `FOO_set` donde `FOO` es el nombre del modelo fuente en minúsculas. Así que para el modelo de `Article` se puede usar `article_set` para acceder a todas las instancias del modelo.
- Esta sintaxis es un poco confusa y no intuitiva. Un mejor enfoque es añadir un atributo `related_name` al modelo que permita establecer explícitamente el nombre de esta relación inversa en su lugar. Hagámoslo.
- Para empezar, agregar un atributo `related_name` al modelo de comentarios. Un buen valor por defecto es nombrarlo en el plural del modelo que contiene la clave foránea.

FICHERO: `articles/models.py`
```python
`...`
class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments', # new
    )
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def__str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('article_list')
```
- Como se acaba de hacer un cambio en el modelo de base de datos, se necesita crear un archivo de migraciones y actualizar la base de datos.

```bash
(news) $ python manage.py makemigrations articles
(news) $ python manage.py migrate
(news) $ python manage.py runserver
```
- Entender las consultas lleva algún tiempo, así que no preocuparse si la idea de las relaciones inversas es confusa. Y una vez que se dominen estos casos básicos, se puede explorar cómo filtrar  consultas con gran detalle para que devuelvan exactamente la información que se desea.
- En el archivo `article_list.html` se pueden añadir los comentarios a `card-footer`. Notar que se han movido los enlaces de edición y borrado a `card-body`. Para acceder a cada comentario se llama a `article.comments.all` lo que significa que primero se mira el modelo `article`, luego `comment` que es el nombre relacionado a todo el modelo `Comment`, y se selecciona `all included`. ¡Puede llevar un poco de tiempo acostumbrarse a esta sintaxis para referenciar datos de claves foráneas en una plantilla!

FICHERO: `template/article_list.html`
```html
{% extends 'base.html' %}

{% block title %}Articles{% endblock title %}

{% block content %}
  {% for article in object_list %}
    <div class="card">
      <div class="card-header">
        <span class="font-weight-bold">{{ article.title }}</span> &middot;
        <span class="text-muted">by {{ article.author }} | {{ article.date }}</span>
      </div>
      <div class="card-body">
        <p>{{ article.body }}</p>
        <a href="{% url 'article_edit' article.pk %}">Edit</a> |
        <a href="{% url 'article_delete' article.pk %}">Delete</a>
      </div>
      <div class="card-footer">
        {% for comment in article.comments.all %}
          <p>
            <span class="font-weight-bold">{{ comment.author }} &middot;</span>
            {{ comment }}
          </p>
        {% endfor %}
      </div>
    </div>
    <br />
  {% endfor %}
{% endblock content %}



{% extends 'base.html' %}

{% block title %}Articles{% endblock title %}

{% block content %}
  {% for article in object_list %}
    <div class="card">
      <div class="card-header">
        <span class="font-weight-bold">{{ article.title }}</span> &middot;
        <span class="text-muted">by {{ article.author }} | {{ article.date }}</span>
      </div>
      <div class="card-body">
        <!-- Los cambios empiezan aquí -->
        <p>{{ article.body }}</p>
        <a href="{% url 'article_edit' article.pk %}">Editar</a> |
        <a href="{% url 'article_delete' article.pk %}">Borrar</a>
      </div>
      <div class="card-footer">
        {% for comment in article.comments.all %}
          <p>
            <span class="font-weight-bold">
              {{ comment.author }} &middot;
            </span>
            {{ comment }}
          </p>
        {% endfor %}
      </div>
      <!-- Los cambios terminan aquí -->
    </div>
    <br>
  {% endfor %}
{% endblock content %}
```

## Conclusión
- Con más tiempo habría que centrarse en los formularios para que un usuario pueda escribir un nuevo artículo directamente en la página de artículos, así como añadir también comentarios. Pero el principal objetivo de este capítulo es demostrar cómo funcionan las relaciones de clave foránea en Django.
- La aplicación para el periódico ya está completa.
    - Tiene un flujo de autenticación de usuario robusto, incluyendo el uso del correo electrónico para el restablecimiento de la contraseña.
    - También se utiliza un modelo de usuario personalizado, por lo que si se quiere añadir campos adicionales al modelo de usuario personalizado es tan sencillo como añadir un campo adicional. Ya tenemos un campo de edad para todos los usuarios que está siendo configurado por defecto. 
    - Se podría añadir un desplegable de edad al formulario de registro y restringir el acceso de los usuarios sólo a los mayores de 13 años. O se podría ofrecer descuentos a los usuarios mayores de 65 años. Lo que se quiera hacer con el modelo de usuario personalizado es una opción.
- La mayor parte del desarrollo web sigue los mismos patrones y al utilizar un framework como Django el 99% de lo que se quiera en términos de funcionalidad ya está incluido o sólo falta una pequeña personalización de alguna función existente.