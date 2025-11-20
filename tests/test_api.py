import unittest
from app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_get_health_empty(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)

    def test_add_device(self):
        response = self.client.post("/devices", json={"name": "TestDevice", "ip": "1.1.1.1"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json)

if __name__ == "__main__":
    unittest.main()
