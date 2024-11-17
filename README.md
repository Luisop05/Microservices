# 🍽️ Sistema de Gestión de Restaurante

Este proyecto implementa un sistema de gestión de restaurante distribuido en dos microservicios. Cada microservicio es responsable de una función específica: gestión de pedidos e inventario.

## 📁 Estructura del Proyecto

```plaintext
Microservices/
├── inventario_api/
│   ├── tests/
│   │   ├── __pycache__/
│   │   └── test_app.py
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── pedidos_api/
│   ├── tests/
│   │   ├── __pycache__/
│   │   ├── pytest.cache/
│   │   └── test_app.py
│   ├── get-pip.py
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── docker-entrypoint.sh
├── Dockerfile
├── Jenkinsfile
└── README.md
```

## 🚀 Microservicios

- **🛍️ API de Pedidos** (Puerto 8000): Maneja los pedidos realizados por los clientes.
- **📦 API de Inventario** (Puerto 8001): Administra el inventario de productos disponibles.

## 🔄 Flujo de Comunicación

### Cuando se crea un pedido:
1. 📤 La API de pedidos consulta el inventario
2. ✅ Verifica la disponibilidad
3. 📉 Reduce el stock
4. 💰 Calcula el total basado en precios de inventario

> La comunicación se realiza a través de la red Docker `restaurant-net`

## 📋 Requisitos Previos

- 🐳 [Docker](https://www.docker.com/)
- 🔧 [Docker Compose](https://docs.docker.com/compose/)
- 🏗️ [Jenkins](https://jenkins.io/) (para CI/CD)

## ⚙️ Configuración del Entorno

### Componentes Principales

1. **🐳 Dockerfile Principal**
   - Base: jenkins/jenkins:lts
   - Incluye: Python3, pip, Docker, Docker Compose
   - Configuración para integración con Docker host

2. **📄 docker-compose.yml**
   - Jenkins: Puerto 8080 (UI), 50000 (Agentes)
   - Pedidos API: Puerto 8000
   - Inventario API: Puerto 8001
   - Red compartida: restaurant-net

3. **🔄 Pipeline de Jenkins**
   - Definido en Jenkinsfile
   - Etapas: Clonación, Construcción, Pruebas, Despliegue

## 🛠️ Instalación y Ejecución

### 1. **Configuración Inicial**

```bash
# Clonar el repositorio
git clone https://github.com/Luisop05/Microservices.git
cd Microservices
```

### 2. **Levantar Jenkins**

```bash
# Iniciar el contenedor de Jenkins y la red
docker-compose -f docker-compose.yml up -d jenkins
```

- Acceder a Jenkins: http://localhost:8080
- Seguir el proceso inicial de configuración de Jenkins:
  1. Obtener la contraseña inicial del log de Jenkins
  2. Instalar los plugins recomendados
  3. Crear el primer usuario administrador
  4. Configurar la URL de Jenkins

### 3. **Ejecutar el Pipeline**

1. En Jenkins, crear un nuevo Pipeline:
   - Click en "Nueva Tarea"
   - Seleccionar "Pipeline"
   - En la configuración del pipeline, seleccionar "Pipeline from SCM"
   - Configurar el repositorio Git y la rama

2. Ejecutar el pipeline:
   - El pipeline clonará el repositorio
   - Construirá los microservicios
   - Ejecutará las pruebas
   - Desplegará los servicios

### 4. **Ejecutar Pruebas Localmente**

Para ejecutar las pruebas manualmente, navegar a la carpeta de tests de cada aplicación:

```bash
# Para pedidos_api
cd pedidos_api/tests
PYTHONPATH=.. python3 -m pytest test_app.py

# Para inventario_api
cd inventario_api/tests
PYTHONPATH=.. python3 -m pytest test_app.py
```

## 📚 Documentación de APIs

### 🛍️ API de Pedidos

- **🌐 URL Base**: [http://localhost:8000](http://localhost:8000)
- **📖 Documentación Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Endpoints Disponibles

- **📤 `POST /pedidos/`**
  - Crea un nuevo pedido
- **📥 `GET /pedidos/{pedido_id}`**
  - Obtiene detalles de un pedido
- **🔄 `PUT /pedidos/{pedido_id}/estado`**
  - Estados: `📝 pendiente`, `👨‍🍳 en_preparacion`, `✅ completado`, `❌ cancelado`

### 📦 API de Inventario

- **🌐 URL Base**: [http://localhost:8001](http://localhost:8001)
- **📖 Documentación Swagger**: [http://localhost:8001/docs](http://localhost:8001/docs)

#### Endpoints Disponibles

- **📋 `GET /productos/`**
  - Lista todos los productos
- **🔍 `GET /productos/{producto_id}`**
  - Detalles de un producto
- **📉 `POST /productos/{producto_id}/reducir`**
  - Reduce el stock

## 💡 Ejemplos de Uso

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
```

2. **Consultar el inventario**:
```bash
curl http://localhost:8001/productos/
```

3. **Actualizar estado de un pedido**:
```bash
curl -X PUT http://localhost:8000/pedidos/1/estado \
-H "Content-Type: application/json" \
-d '"en_preparacion"'
```

## 🚀 Pipeline de CI/CD

El pipeline incluye las siguientes etapas:

1. **📥 Clonar Repositorio**
   ```groovy
   git branch: "main", url: "https://github.com/Luisop05/Microservices.git"
   ```

2. **🏗️ Construir Microservicios**
   ```groovy
   docker-compose build
   ```

3. **🧪 Ejecutar Pruebas**
   ```groovy
   docker-compose run pedidos-api python -m unittest discover -s tests
   docker-compose run inventario-api python -m unittest discover -s tests
   ```

4. **📤 Deploy**
   ```groovy
   docker-compose up -d pedidos-api inventario-api
   ```

## 🛑 Detener los Servicios

```bash
docker-compose down
```

## 🤝 Contribuir

1. Fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 👥 Autores

- **Luis Ortiz** - [Luisop05](https://github.com/Luisop05)

## 🙏 Agradecimientos

- Gracias a todos los que han contribuido al proyecto
- Inspirado en las mejores prácticas de microservicios
- Construido con amor para la comunidad dev
