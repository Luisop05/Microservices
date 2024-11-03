Sistema de Gestión de Restaurante
Este proyecto implementa un sistema de gestión de restaurante con dos microservicios:

API de Pedidos (Puerto 8000): Gestiona los pedidos de los clientes
API de Inventario (Puerto 8001): Gestiona el inventario de productos

Requisitos

Docker
Docker Compose

Instalación y Ejecución

Clonar el repositorio:

Levantar los contenedores:

docker-compose up --build
Documentación de APIs
API de Pedidos (http://localhost:8000)
Endpoints Disponibles:

POST /pedidos/

Crea un nuevo pedido
Verifica el inventario disponible
Actualiza automáticamente el stock


GET /pedidos/{pedido_id}

Obtiene los detalles de un pedido específico


PUT /pedidos/{pedido_id}/estado

Actualiza el estado de un pedido
Estados disponibles: pendiente, en_preparacion, completado, cancelado



API de Inventario (http://localhost:8001)
Endpoints Disponibles:

GET /productos/

Lista todos los productos disponibles


GET /productos/{producto_id}

Obtiene detalles de un producto específico


POST /productos/{producto_id}/reducir

Reduce el stock de un producto



Ejemplos de Uso
1. Crear un nuevo pedido:
curl -X POST http://localhost:8000/pedidos/ \
-H "Content-Type: application/json" \
-d '{
  "items": [
    {
      "producto_id": 1,
      "cantidad": 2,
      "notas": "Sin cebolla"
    }
  ],
  "mesa": 5
}'
2. Consultar inventario:
curl http://localhost:8001/productos/
3. Actualizar estado de pedido:
curl -X PUT http://localhost:8000/pedidos/1/estado \
-H "Content-Type: application/json" \
-d '"en_preparacion"'

Documentación Swagger

API de Pedidos: http://localhost:8000/docs
API de Inventario: http://localhost:8001/docs

Estructura del Proyecto
Microservices/
├── pedidos_api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── inventario_api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── docker-compose.yml
└── README.md

Detener los servicios
Para detener los contenedores:
 docker-compose down