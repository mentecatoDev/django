# 15. Permisos y Autorización

- Si se quiere que el periódico sea financieramente sostenible se podría añadir una app de *pagos* para cobrar por el acceso, para lo que se requiere un **proceso de autorización**, diferente al **proceso de autenticación**. La autorización restringe el acceso; la autenticación permite el flujo de registro e inicio de sesión de un usuario.
- Django incorpora una funcionalidad de autorización que se puede utilizar rápidamente. 

## 15.1. `CreateView` mejorado
- Se van a establecer permisos de edición/borrado para que sólo el autor de un artículo pueda hacer tales cambios.
- Se va a eliminar el autor de los campos y en su lugar se establecerá automáticamente a través del método `form_valid`.

FICHERO: `articles/views.py`
```python
`...`
class ArticleCreateView(CreateView):
    model = models.Article
    template_name = 'article_new.html'
    fields = ('title', 'body')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
`...`
```
> Las vistas genéricas basadas en clases son increíbles para empezar nuevos proyectos, pero cuando se quieren personalizar, es necesario remangarse y empezar a entender lo que pasa bajo el capó. Lo más probable es que lo que estás intentando hacer ya haya sido resuelto en algún lugar, ya sea dentro de Django mismo o en un foro como Stack Overflow. No tengas miedo de pedir ayuda!

- Ahora el autor ya no es un campo a rellenar si se crea un nuevo artículo sino que se establece automáticamente según el usuario actual conectado.

## 15.2. Autorizaciones

- Hay múltiples problemas en torno a la falta de autorizaciones en nuestro proyecto actual.
    - Nos gustaría restringir el acceso sólo a los usuarios para tener la opción de cobrar un día a los lectores de nuestro periódico.
    
    - Cualquier usuario desconectado al azar que conozca la URL correcta puede acceder a cualquier parte del sitio.
    
      - ¿Qué pasaría si un usuario que ha cerrado la sesión intentara crear un nuevo artículo? Para probarlo haga clic en su nombre de usuario en la esquina superior derecha de la barra de navegación y seleccione "Cerrar sesión" en las opciones desplegables. El enlace "+ Nuevo" desaparece de la barra de navegación, pero ¿qué ocurre si vas directamente a: http://127.0.0.1:8000/articles/new/?: La página sigue ahí.
      - Intenta crear un nuevo artículo y pulsar el botón "Grabar".
      - ERROR: El modelo espera un campo `author` que está enlazado al usuario logeado, pero, como no hay ninguno, no hay autor tampoco y por tanto el envío falla. ¿Qué hacer?

## 15.3. Mixins
- Hay que establecer algunas autorizaciones para que sólo los usuarios registrados puedan acceder al sitio. Para ello se puede utilizar un **mixin**, que es un *tipo especial de herencia múltiple que Django utiliza para evitar la duplicación de código y permitir la personalización*.
    - Por ejemplo, el `ListView` genérico incorporado necesita una forma de devolver una plantilla. Pero también lo hace `DetailView` y, de hecho, casi todas las demás vistas. En lugar de repetir el mismo código en cada gran vista genérica, Django descompone esta funcionalidad en una "mezcla" conocida como `TemplateResponseMixin`. Tanto la `ListView` como la `DetailView` usan esta mezcla para mostrar la plantilla adecuada.
    - Para restringir el acceso a la vista a sólo los usuarios conectados, Django tiene un mixin `LoginRequired` que se puede utilizar.

FICHERO: `articles/views.py`
```python
from django.contrib.auth.mixins import LoginRequiredMixin # new
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Article

`...`
class ArticleCreateView(LoginRequiredMixin, CreateView): # new

```
- Regresar a la URL para crear nuevos mensajes en http://127.0.0.1:8000/articles/new/ y se verá un error:
    - Django se ha redirigido automáticamente a la ubicación por defecto de la página de inicio de sesión que está en `/accounts/login`, sin embargo, en los URLs a nivel de proyecto se usa usando `users/` como ruta. Por eso la página de acceso está en `users/login`. Entonces, ¿cómo se informa a `ArticleCreateView` sobre esto?
    - La respuesta está en la documentación para `LoginRequiredMixin`. Se puede agregar una ruta `login_url` para anular el parámetro por defecto. Se usa la URL con nombre de la ruta `login`.

FICHERO: `articles/views.py`
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Article


class ArticleListView(LoginRequiredMixin, ListView): # new
	model = Article
	template_name = 'article_list.html'

    
class ArticleDetailView(LoginRequiredMixin, DetailView): # new
	model = Article
	template_name = 'article_detail.html'


class ArticleUpdateView(LoginRequiredMixin, UpdateView): # new
    model = Article
    fields = ('title', 'body',)
	template_name = 'article_edit.html'

    
class ArticleDeleteView(LoginRequiredMixin, DeleteView): # new
	model = Article
	template_name = 'article_delete.html'
	success_url = reverse_lazy('article_list')
    
class ArticleCreateView(LoginRequiredMixin, CreateView):
	model = Article
	template_name = 'article_new.html'
	fields = ('title', 'body',)

    def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

```

- Probar el enlace para crear nuevos mensajes de nuevo: http://127.0.0.1:8000/articles/new/.
    - Ahora redirige a los usuarios a la página de acceso. Tal como se deseaba.

## 15.4 Actualizando las vistas
Estamos progresando, pero todavía existe el problema de nuestras vistas de edición y borrado. Cualquier usuario conectado puede hacer cambios en cualquier artículo. Lo que queremos es restringir este acceso para que sólo el autor de un artículo tenga este permiso.
Podríamos añadir lógica de permisos a cada vista para esto, pero una solución más elegante es crear un mixin dedicado, una clase con una característica particular que queremos reutilizar en nuestro código Django. Y mejor aún, Django viene con un mixin incorporado, `UserPassesTestMixin`, ¡sólo para este propósito!

- Restringir el acceso a las vistas es sólo cuestión de añadir `LoginRequiredMixin` al principio de todas las vistas existentes y especificar el `login_url` correcto.
- Actualizar el resto de las vistas de los artículos ya que no se desea que un usuario pueda crear, leer, actualizar o borrar un mensaje si no está conectado.
- El archivo completo `views.py` debería tener ahora este aspecto:

FICHERO: `articles/views.py`
```python
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin # new
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .models import Article

`...`

class ArticleUpdateView(
	LoginRequiredMixin, UserPassesTestMixin, UpdateView): # new
	model = Article
	fields = ('title', 'body',)
	template_name = 'article_edit.html'

	def test_func(self): # new
		obj = self.get_object()
	return obj.author == self.request.user

class ArticleDeleteView(
	LoginRequiredMixin, UserPassesTestMixin, DeleteView): # new
	model = Article
	template_name = 'article_delete.html'
	success_url = reverse_lazy('article_list')

	def test_func(self): # new
		obj = self.get_object()
		return obj.author == self.request.user

```

- Jugar con el sitio para confirmar que las redirecciones de acceso ahora funcionan como se esperaba.

## Conclusión
- La aplicación para el periódico está casi terminada. 
    - Artículos correctamente configurados
    - Establecidos permisos y autorizaciones
    - La autentificación de los usuarios está en buen estado.
- Queda:
    - Añadir la posibilidad de que otros usuarios conectados dejen comentarios