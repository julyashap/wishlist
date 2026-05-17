from fastapi.testclient import TestClient


def test_user_registration(client: TestClient) -> None:
    """Проверка успешного создания аккаунта."""
    payload = {"username": "julia", "password": "secure_password"}
    
    response = client.post("/api/auth/register", json=payload)
    
    assert response.status_code == 200
    assert "регистрация успешна" in response.json().get("message", "").lower()


def test_user_login(client: TestClient) -> None:
    """Проверка входа и получения HttpOnly куки."""
    user = {"username": "login_test", "password": "password123"}
    
    client.post("/api/auth/register", json=user)
    
    response = client.post("/api/auth/login", json=user)
    assert response.status_code == 200
    assert "access_token" in response.cookies
