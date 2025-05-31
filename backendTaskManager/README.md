## Proyecto de gestión de Tareas
Para la prueba técnica, se deberá crear un sistema de tareas. 
Este sistema deberá permitirte crear nuevas tareas, actualizarlas y consultarlas.

## Estructura del Proyecto de gestión de Tareas
backendTaskManager/
├── manage.py
├── backendTaskManager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── ...
└── requirements.txt

## Nota: Se utiliza BD Sqlite para dar facilidad de uso y despliegue.

## Instrucciones para ejecución de Proyecto de gestión de Tareas sin Docker
1. Clona el repositorio del proyecto.
2. Instala las dependencias del proyecto con `pip install -r requirements.txt`.
3. Realiza las migraciones de la base de datos con `python manage.py migrate`.


## Instrucciones para ejecución de Proyecto de gestión de Tareas con Docker
1. Clona el repositorio del proyecto.
2. Construye la imagen de Docker con el comando `docker build -t backend-task-manager .`.
3. Inicia el contenedor de Docker con el comando `docker run -p 8000:8000 backend-task-manager`.

Pasos comunes para ambas ejecuciones:
* Inicia el servidor de desarrollo con `python manage.py runserver`.
* Accede a la  en tu navegador en `http://localhost:8000`.