# Sistema de Gestión de Restaurante

prueba jenkins

Este proyecto implementa un sistema de gestión de restaurante distribuido en dos microservicios. Cada microservicio es responsable de una función específica: gestión de pedidos e inventario.

- **API de Pedidos** (Puerto 8000): Maneja los pedidos realizados por los clientes.
- **API de Inventario** (Puerto 8001): Administra el inventario de productos disponibles.
## Estructura del Proyecto

La estructura del proyecto es la siguiente:

```plaintext
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
└── Jenkinsfile

Comunicación entre servicios:
## Cuando se crea un pedido:
1. La api de pedidos consulta el inventario
2. Verifica la disponibilidad
3. Reduce el stock
4. Calcula el total basado en precios de inventario

## La comunicación se realiza a través de la red Docker restaurant-net

## Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Instalación y Ejecución

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/Luisop05/Microservices.git
   cd nombre_del_repositorio

2. **Levantar los contenedores:**

    ```bash
    docker-compose up --build

Este comando construirá y levantará los contenedores necesarios para ejecutar los microservicios.


## Documentación de APIs

Cada microservicio tiene su propia API documentada con Swagger para una interacción más sencilla y para facilitar las pruebas.

### API de Pedidos

- **URL Base**: [http://localhost:8000](http://localhost:8000)
- **Documentación Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Endpoints Disponibles

- **`POST /pedidos/`**  
  Crea un nuevo pedido, verifica el inventario disponible y actualiza automáticamente el stock.

- **`GET /pedidos/{pedido_id}`**  
  Obtiene los detalles de un pedido específico.

- **`PUT /pedidos/{pedido_id}/estado`**  
  Actualiza el estado de un pedido. Los estados disponibles incluyen:
  - `pendiente`
  - `en_preparacion`
  - `completado`
  - `cancelado`

### API de Inventario

- **URL Base**: [http://localhost:8001](http://localhost:8001)
- **Documentación Swagger**: [http://localhost:8001/docs](http://localhost:8001/docs)

#### Endpoints Disponibles

- **`GET /productos/`**  
  Lista todos los productos disponibles en el inventario.

- **`GET /productos/{producto_id}`**  
  Obtiene los detalles de un producto específico.

- **`POST /productos/{producto_id}/reducir`**  
  Reduce el stock de un producto en función de la cantidad indicada.


## Ejemplos de Uso

A continuación, se muestran ejemplos de uso para cada endpoint principal:

1. **Crear un nuevo pedido**:

   ```bash
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


2. **Consultar el inventario:**

    ```bash
    curl http://localhost:8001/productos/
    
3. **Actualizar estado de un pedido:**

    ```bash
    curl -X PUT http://localhost:8000/pedidos/1/estado \
    -H "Content-Type: application/json" \
    -d '"en_preparacion"'



## Detener los Servicios

1. **Para detener y eliminar los contenedores, usa el siguiente comando::**

   ```bash
   docker-compose down

