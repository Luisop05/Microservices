import pytest
from fastapi.testclient import TestClient
from app import app, EstadoPedido

client = TestClient(app)

def test_crear_pedido_exitoso():
    response = client.post("/pedidos/", json={
        "items": [
            {"producto_id": 1, "cantidad": 1}
        ],
        "mesa": 1
    })
    assert response.status_code == 200
    assert response.json()['mensaje'] == "Pedido creado exitosamente"

def test_crear_pedido_producto_no_existente():
    response = client.post("/pedidos/", json={
        "items": [
            {"producto_id": 99, "cantidad": 1}
        ],
        "mesa": 1
    })
    assert response.status_code == 400
    assert "Producto 99 no encontrado" in response.json()['detail']

def test_obtener_pedido_existente():
    # Primero, crea un pedido exitoso
    client.post("/pedidos/", json={
        "items": [
            {"producto_id": 1, "cantidad": 1}
        ],
        "mesa": 1
    })
    response = client.get("/pedidos/1")
    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'items' in response.json()
    assert 'mesa' in response.json()
    assert 'estado' in response.json()

def test_obtener_pedido_no_existente():
    response = client.get("/pedidos/99")
    assert response.status_code == 404
    assert response.json()['detail'] == "Pedido no encontrado"

def test_actualizar_estado_pedido():
    # Crear un pedido primero
    client.post("/pedidos/", json={
        "items": [
            {"producto_id": 1, "cantidad": 1}
        ],
        "mesa": 1
    })
    response = client.put("/pedidos/1/estado", json={"estado": EstadoPedido.COMPLETADO})
    assert response.status_code == 200
    assert response.json()['estado'] == EstadoPedido.COMPLETADO

def test_actualizar_estado_pedido_invalido():
    # Crear un pedido primero
    client.post("/pedidos/", json={
        "items": [
            {"producto_id": 1, "cantidad": 1}
        ],
        "mesa": 1
    })
    response = client.put("/pedidos/1/estado", json={"estado": "ESTADO_INVALIDO"})
    assert response.status_code == 422  # Validation error

def test_crear_pedido_sin_items():
    response = client.post("/pedidos/", json={
        "items": [],
        "mesa": 1
    })
    assert response.status_code == 400
    assert "El pedido debe contener al menos un item" in response.json()['detail']

def test_crear_pedido_cantidad_negativa():
    response = client.post("/pedidos/", json={
        "items": [
            {"producto_id": 1, "cantidad": -1}
        ],
        "mesa": 1
    })
    assert response.status_code == 400
    assert "La cantidad debe ser mayor que 0" in response.json()['detail']