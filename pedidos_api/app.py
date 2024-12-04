from fastapi import FastAPI, HTTPException
import sentry_sdk
from pydantic import BaseModel
from typing import List, Optional
import requests
from datetime import datetime
from enum import Enum


class EstadoPedido(str, Enum):
    PENDIENTE = "pendiente"
    EN_PREPARACION = "en_preparacion"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"

class ItemPedido(BaseModel):
    producto_id: int
    cantidad: int
    notas: Optional[str] = None

class Pedido(BaseModel):
    id: Optional[int] = None
    items: List[ItemPedido]
    mesa: int
    estado: EstadoPedido = EstadoPedido.PENDIENTE
    fecha_creacion: Optional[str] = None
    total: Optional[float] = None

class PedidoResponse(BaseModel):
    pedido: Pedido
    mensaje: str

sentry_sdk.init(
    dsn="https://dba308987dcb11ef76e61234e2717584@o4508393627254784.ingest.us.sentry.io/4508393928720384",
    traces_sample_rate=1.0,  
    profiles_sample_rate=1.0,
)

app = FastAPI(
    title="API de Pedidos - Restaurante",
    description="API para gestionar pedidos del restaurante",
    version="1.0.0"
)

# Simulamos una base de datos de pedidos
pedidos = {}
ultimo_id = 0


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

@app.post("/pedidos/", 
          response_model=PedidoResponse,
          tags=["pedidos"],
          summary="Crear nuevo pedido",
          description="Crea un nuevo pedido verificando la disponibilidad de productos")
async def crear_pedido(pedido: Pedido):
    global ultimo_id
    with sentry_sdk.start_transaction(name="crear pedido"):
        try:
            # Verificar inventario para cada item
            for item in pedido.items:
                response = requests.get(
                    f"http://inventario-api:8001/productos/{item.producto_id}"
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=400, 
                                    detail=f"Producto {item.producto_id} no encontrado")
                
                producto = response.json()
                if producto["stock"] < item.cantidad:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stock insuficiente para {producto['nombre']}"
                    )
                
                # Actualizar inventario
                requests.post(
                    f"http://inventario-api:8001/productos/{item.producto_id}/reducir",
                    json={"cantidad": item.cantidad}
                )
            
            # Crear pedido
            ultimo_id += 1
            pedido.id = ultimo_id
            pedido.fecha_creacion = datetime.now().isoformat()
            
            # Calcular total
            total = 0
            for item in pedido.items:
                response = requests.get(
                    f"http://inventario-api:8001/productos/{item.producto_id}"
                )
                producto = response.json()
                total += producto["precio"] * item.cantidad
            
            pedido.total = total
            pedidos[pedido.id] = pedido
            import time
            time.sleep(2)
            
            return PedidoResponse(
                pedido=pedido,
                mensaje="Pedido creado exitosamente"
            )
        
        except requests.RequestException:
            raise HTTPException(
                status_code=503,
                detail="Error al comunicarse con el servicio de inventario"
            )

@app.get("/pedidos/{pedido_id}", 
         response_model=Pedido,
         tags=["pedidos"],
         summary="Obtener pedido por ID",
         description="Retorna los detalles de un pedido específico")
async def obtener_pedido(pedido_id: int):
    if pedido_id not in pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedidos[pedido_id]

@app.put("/pedidos/{pedido_id}/estado", 
         response_model=Pedido,
         tags=["pedidos"],
         summary="Actualizar estado del pedido",
         description="Actualiza el estado de un pedido existente")
async def actualizar_estado_pedido(pedido_id: int, estado: EstadoPedido):
    if pedido_id not in pedidos:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    pedidos[pedido_id].estado = estado
    return pedidos[pedido_id]