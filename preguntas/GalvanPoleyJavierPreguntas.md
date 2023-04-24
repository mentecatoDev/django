::DJ061::
El comando para iniciar una app en django es: { 
= python .\manage.py startapp HelloWorld 
~%-25% python .\manage.py appstart HelloWorld 
~%-25% python .\manage.py startapplication HelloWorld 
~%-25% python .\manage.py newApp HelloWorld } 

::DJ062::
Para arrancar el servidor con un puerto distinto al que establece por defecto django, en este caso el puerto 4000, utilizaremos el siguiente comando: { 
= python .\manage.py runserver 4000 
~%-25% python .\manage.py runserver:4000 
~%-25% python .\manage.py runserver port 4000 
~%-25% python .\manage.py startserver 4000 } 

::DJ063::
Para iniciar el shell de Django usaremos el siguiente comando: { 
~%-25% python .\manage.py start shell = python .\manage.py shell 
~%-25% python .\manage.py shellstart 
~%-25% python .\manage.py runshell } 

::DJ064::
El comando para crear un usuario administrador para Django es: { 
~%-25% python .\manage.py createadminuser 
~%-25% python .\manage.py createadmin 
~%-25% python .\manage.py createuser 
= python .\manage.py createsuperuser }