## Proyecto de gestión de Tareas
Para la prueba técnica, se deberá crear un sistema de tareas. 
Este sistema deberá permitirte crear nuevas tareas, actualizarlas y consultarlas.

## Estructura del Proyecto de gestión de Tareas
## Estructura del Proyecto de Gestión de Tareas

```bash
backendTaskManager/
├── manage.py                          # Script principal para ejecutar comandos de Django (migraciones, servidor, etc.)
├── pytest.ini                         # Configuración de pytest para pruebas automatizadas
├── core/                              # Módulo central de configuraciones compartidas
│   ├── injection.py                   # Configuración de inyección de dependencias (DI) para toda la aplicación
├── backendTaskManager/                # Configuración principal del proyecto Django
│   ├── settings.py                    # Archivo principal de configuración del proyecto (DB, apps, middleware, etc.)
│   ├── urls.py                        # Rutas globales del proyecto
│   └── wsgi.py                        # Interfaz WSGI para despliegue en servidores (como Gunicorn)
├── tasks/                             # Aplicación principal encargada de la gestión de tareas y categorías
│   ├── migrations/                    # Migraciones de base de datos para el modelo `tasks`
│   ├── services/                      # Lógica de negocio (services) y definición de interfaces
│   │   ├── di.py                      # Módulo que configura los bindings para la inyección de dependencias
│   │   ├── interfaces.py              # Definición de interfaces (abstracciones) para servicios
│   │   ├── auth_service.py            # Lógica de autenticación personalizada (si aplica)
│   │   ├── task_service.py            # Lógica relacionada a las tareas (crear, completar, listar, etc.)
│   │   └── category_service.py        # Lógica relacionada a las categorías de tareas
│   ├── views/                         # Vistas (ViewSets de DRF) separadas por funcionalidad
│   │   ├── auth_views.py              # Vistas relacionadas con autenticación (login, logout, etc.)
│   │   ├── category_views.py          # Vistas que manejan las categorías
│   │   └── task_views.py              # Vistas que manejan las tareas
│   ├── admin.py                       # Registro de modelos en el panel de administración de Django
│   ├── apps.py                        # Configuración de la app `tasks` (nombre, etc.)
│   ├── factories.py                   # Generadores de datos falsos para pruebas o desarrollo
│   ├── models.py                      # Definición de modelos de base de datos (Task, Category, etc.)
│   ├── serializers.py                 # Serializadores para convertir modelos a JSON y viceversa
│   ├── tests/                         # Pruebas automatizadas de la aplicación 
│   │   ├── conftest.py                # Configuración de pruebas
│   │   ├── unit/                      # Pruebas unitarias (sin base de datos real)
│   │   │   └── test_task_service_integration.py  # Aquí irían las pruebas unitarias de TaskService
│   ├── integration/                   # Pruebas de integración (con base de datos real)
│   │   │   └── test_task_service_integration.py # Aquí irían las pruebas de integración de TaskService
│   └── urls.py                        # Rutas específicas de la app `tasks`
└── requirements.txt                   # Lista de dependencias del proyecto para instalar con pip
```

## Nota: Se utiliza BD Sqlite para dar facilidad de uso y despliegue.

## Instrucciones para ejecución de Proyecto de gestión de Tareas sin Docker
1. Clona el repositorio del proyecto.
2. Instala las dependencias del proyecto con `pip install -r requirements.txt`.
3. Realiza las migraciones de la base de datos con `python manage.py migrate`.
4. Inicia el servidor de desarrollo con `python manage.py runserver`.

## Instrucciones para ejecución de Proyecto de gestión de Tareas con Docker
1. Clona el repositorio del proyecto.
2. Construye la imagen de Docker con el comando `docker build -t backend-task-manager .`.
3. Inicia el contenedor de Docker con el comando `docker run -p 8000:8000 backend-task-manager`.

## Instrucciones para ejecución de Proyecto de gestión de Tareas con Docker Compose
1. Clona el repositorio del proyecto.
2. Ejecutar  `docker compose up --build`
   - Este comando construirá la imagen y levantará el contenedor de Docker.
   - Si deseas ejecutar en segundo plano, puedes usar `docker compose up --build -d`.

Pasos comunes para ambas ejecuciones:

* Accede a la  en tu navegador en `http://localhost:8000/api`.