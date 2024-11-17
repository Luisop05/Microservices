import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_listar_productos():
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    # Verificar que hay productos en la lista
    assert len(response.json()) > 0
    # Verificar la estructura de los productos
    for producto in response.json():
        assert 'id' in producto
        assert 'nombre' in producto
        assert 'precio' in producto
        assert 'stock' in producto

def test_obtener_producto_existente():
    response = client.get("/productos/1")
    assert response.status_code == 200
    assert response.json()['nombre'] == "Hamburguesa Clásica"
    assert isinstance(response.json()['precio'], (int, float))
    assert isinstance(response.json()['stock'], int)

def test_obtener_producto_no_existente():
    response = client.get("/productos/99")
    assert response.status_code == 404
    assert response.json()['detail'] == "Producto no encontrado"

def test_reducir_stock_exitoso():
    # Primero obtener el stock actual
    producto_response = client.get("/productos/1")
    stock_inicial = producto_response.json()['stock']
    
    # Reducir el stock
    cantidad_reducir = 1
    response = client.post("/productos/1/reducir", json={"cantidad": cantidad_reducir})
    
    assert response.status_code == 200
    assert response.json()['stock'] == stock_inicial - cantidad_reducir

def test_reducir_stock_insuficiente():
    # Primero obtener el stock actual
    producto_response = client.get("/productos/1")
    stock_actual = producto_response.json()['stock']
    
    # Intentar reducir más del stock disponible
    response = client.post("/productos/1/reducir", json={"cantidad": stock_actual + 1})
    assert response.status_code == 400
    assert response.json()['detail'] == "Stock insuficiente"

def test_reducir_stock_cantidad_negativa():
    response = client.post("/productos/1/reducir", json={"cantidad": -1})
    assert response.status_code == 400
    assert "La cantidad debe ser mayor que 0" in response.json()['detail']

def test_reducir_stock_producto_no_existente():
    response = client.post("/productos/99/reducir", json={"cantidad": 1})
    assert response.status_code == 404
    assert response.json()['detail'] == "Producto no encontrado"

def test_verificar_precio_producto():
    response = client.get("/productos/1")
    assert response.status_code == 200
    assert response.json()['precio'] > 0