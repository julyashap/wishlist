from fastapi.testclient import TestClient


def test_create_wish_requires_auth(client: TestClient) -> None:
    """Анонимный пользователь должен получать 401 Unauthorized."""
    response = client.post("/api/wishes/", json={"title": "Запрещенка"})
    assert response.status_code == 401


def test_wish_full_lifecycle(auth_client: TestClient) -> None:
    """Проверка полной цепочки: Создание -> Получение -> Изменение -> Удаление."""
    wish_payload = {"title": "Кроссовки", "price": 9500.0, "priority": "medium"}

    create_res = auth_client.post("/api/wishes/", json=wish_payload)
    assert create_res.status_code == 201
    wish_id: int = create_res.json()["id"]

    get_res = auth_client.get(f"/api/wishes/{wish_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Кроссовки"

    update_payload = {"title": "Пастельные кроссовки", "is_bought": True}
    update_res = auth_client.patch(f"/api/wishes/{wish_id}", json=update_payload)
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Пастельные кроссовки"
    assert update_res.json()["is_bought"] is True

    delete_res = auth_client.delete(f"/api/wishes/{wish_id}")
    assert delete_res.status_code == 204

    final_check = auth_client.get(f"/api/wishes/{wish_id}")
    assert final_check.status_code == 404
