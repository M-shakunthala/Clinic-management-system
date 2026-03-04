"""
Test API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestAPI:
    """Test general API functionality"""

    def test_docs_endpoint(self, client: TestClient):
        """Test API documentation endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_health_check(self, client: TestClient):
        """Test API health check"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data or "message" in data

    def test_openapi_json(self, client: TestClient):
        """Test OpenAPI JSON endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
