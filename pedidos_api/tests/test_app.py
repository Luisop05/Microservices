# pedidos_api/tests/test_app.py

import unittest
from fastapi.testclient import TestClient
from app import app, EstadoPedido

class TestPedidosAPI(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)

    def test_crear_pedido_exitoso(self):
        response = self.client.post("/pedidos/", json={
            "items": [
                {"producto_id": 1, "cantidad": 1}
            ],
            "mesa": 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['mensaje'], "Pedido creado exitosamente")

    def test_crear_pedido_producto_no_existente(self):
        response = self.client.post("/pedidos/", json={
            "items": [
                {"producto_id": 99, "cantidad": 1}
            ],
            "mesa": 1
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Producto 99 no encontrado", response.json()['detail'])

    def test_obtener_pedido_existente(self):
        # Primero, crea un pedido exitoso
        self.client.post("/pedidos/", json={
            "items": [
                {"producto_id": 1, "cantidad": 1}
            ],
            "mesa": 1
        })
        response = self.client.get("/pedidos/1")
        self.assertEqual(response.status_code, 200)

    def test_obtener_pedido_no_existente(self):
        response = self.client.get("/pedidos/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Pedido no encontrado")

    def test_actualizar_estado_pedido(self):
        # Crear un pedido primero
        self.client.post("/pedidos/", json={
            "items": [
                {"producto_id": 1, "cantidad": 1}
            ],
            "mesa": 1
        })
        response = self.client.put("/pedidos/1/estado", json={"estado": EstadoPedido.COMPLETADO})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['estado'], EstadoPedido.COMPLETADO)

if __name__ == "__main__":
    unittest.main()
