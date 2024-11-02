Microservicios Docker
Este proyecto consiste en dos microservicios dockerizados que se comunican entre sí:

API Principal (Puerto 8000)
API Secundaria (Puerto 8001)

Requisitos

Docker
Docker Compose

Instalación y Ejecución

Clonar el repositorio:

Levantar los contenedores:

bashCopydocker-compose up --build

Endpoints Disponibles
API Principal (http://localhost:8000)

/: Mensaje de bienvenida
/obtener-datos: Obtiene datos de la API secundaria

API Secundaria (http://localhost:8001)

/: Mensaje de bienvenida
/datos: Retorna datos de ejemplo con la fecha actual

Estructura del Proyecto
Copy/
├── api_principal/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── api_secundaria/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── docker-compose.yml
└── README.md

Pruebas
Para verificar que todo funciona correctamente:

Acceder a http://localhost:8000/docs para ver la documentación de la API principal
Acceder a http://localhost:8001/docs para ver la documentación de la API secundaria
Probar el endpoint http://localhost:8000/obtener-datos para verificar la comunicación entre servicios

Detener los servicios

Para detener los contenedores:
bashCopydocker-compose down