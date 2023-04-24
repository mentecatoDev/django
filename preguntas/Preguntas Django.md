
```gift
:: DJ051 ::
¿Cómo se cambia el puerto en el que se conecta Django por defecto cuando ejecutamos runserver (por ejemplo al 4000) {
~%-25% python manage.py runserver -p 4000 
=      python manage.py runserver 4000
~%-25% python manage.py runserver:4000
~%-25% python manage.py runserver --port 4000
}

:: DJ052 ::
¿Qué fichero nos permite crear tablas para posteriormente agregarlas a nuestra base de datos {
=      models.py
~%-25% forms.py
~%-25% views.py
~%-25% sql.py
}

:: DJ053 ::
Si queremos añadir en la URL una variable que sea un tipo entero con el nombre id, ¿cómo lo pondríamos?{
~%25-25% path('example/id_as_variable')
~%25-25% path('example/id/int')
=        path('example/<int:id>')
~%25-25% path('<int:id>/example')
}

:: DJ054 ::
Como recorremos los datos con un bucle for dentro de Django {
~%25-25% for project in projects
~%25-25% {{for project in projects}}
~%25-25% {%for% project in %projects%}
=        {% for project in projects %}
}
```


