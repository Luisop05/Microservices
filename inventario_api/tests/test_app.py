# inventario_api/tests/test_app.py

import unittest
from fastapi.testclient import TestClient
from app import app, Producto

class TestInventarioAPI(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)

    def test_listar_productos(self):
        response = self.client.get("/productos/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_obtener_producto_existente(self):
        response = self.client.get("/productos/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['nombre'], "Hamburguesa Clásica")

    def test_obtener_producto_no_existente(self):
        response = self.client.get("/productos/99")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Producto no encontrado")

    def test_reducir_stock_exitoso(self):
        response = self.client.post("/productos/1/reducir", json={"cantidad": 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['stock'], 40)

    def test_reducir_stock_insuficiente(self):
        # Intentar reducir más stock del que hay
        response = self.client.post("/productos/1/reducir", json={"cantidad": 100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], "Stock insuficiente")

if __name__ == "__main__":
    unittest.main()
