from pathlib import Path

from app import create_app
from app.pet import Pet
from app.storage import save_pet


def test_pet_api_supports_read_and_action(tmp_path: Path) -> None:
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "pet.db")})
    client = app.test_client()

    page = client.get("/")
    assert page.status_code == 200
    assert "我的電子雞" in page.get_data(as_text=True)

    initial = client.get("/api/pet")
    assert initial.status_code == 200
    assert initial.json["hunger"] == 80

    updated = client.post("/api/pet/action", json={"action": "feed"})
    assert updated.status_code == 200
    assert updated.json["hunger"] == 100


def test_pet_load_caps_offline_decay_at_24_hours(tmp_path: Path) -> None:
    database_path = tmp_path / "pet.db"
    app = create_app({"TESTING": True, "DATABASE": str(database_path)})
    pet = Pet(
        hunger=100,
        mood=100,
        energy=100,
        cleanliness=100,
        updated_at=10,
    )
    save_pet(pet, database_path)

    response = app.test_client().get("/api/pet")

    assert response.status_code == 200
    assert response.json["hunger"] == 0
    assert response.json["mood"] == 52
    assert response.json["updated_at"] > 10


def test_action_api_rejects_unknown_action(tmp_path: Path) -> None:
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "pet.db")})

    response = app.test_client().post("/api/pet/action", json={"action": "dance"})

    assert response.status_code == 400
