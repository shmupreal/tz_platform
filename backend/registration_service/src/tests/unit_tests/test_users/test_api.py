import pytest
import json
import pytest

@pytest.mark.asyncio
async def test_register_user(mock_auth_service, ac):
    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    
    user_data = users[0]

    response = await ac.post("/users", json={
        "name": user_data["name"],
        "phone_number": user_data["phone_number"],
        "email": user_data["email"],
        "password": "securepassword123"
    })

    assert response.status_code == 201

