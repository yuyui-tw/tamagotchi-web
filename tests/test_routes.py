import sqlite3
from pathlib import Path

import pytest

from app import create_app
from app.pet import Pet
from app.storage import init_db, load_pet, save_pet


def test_pet_api_supports_read_and_effective_action(tmp_path: Path) -> None:
    database_path = tmp_path / "pet.db"
    app = create_app({"TESTING": True, "DATABASE": str(database_path)})
    client = app.test_client()

    page = client.get("/")
    page_text = page.get_data(as_text=True)
    assert page.status_code == 200
    assert "我的電子雞" in page_text
    assert "餵食、玩耍、睡覺、清潔" in page_text

    initial = client.get("/api/pet")
    assert initial.status_code == 200
    assert initial.json["hunger"] == 100
    assert initial.json["status"] == "happy"

    save_pet(
        Pet(
            hunger=75,
            mood=60,
            energy=80,
            cleanliness=90,
            updated_at=initial.json["updated_at"],
        ),
        database_path,
    )
    fed = client.post("/api/pet/action", json={"action": "feed"})

    assert fed.status_code == 200
    assert fed.json["hunger"] == 100
    assert fed.json["status"] == "normal"
    assert fed.json["delta"] == {
        "hunger": 25,
        "mood": 5,
        "energy": 0,
        "cleanliness": -2,
    }
    assert fed.json["effective"] is True
    assert fed.json["message"] == "餵食了，飽食度 +25"


def test_full_stat_action_returns_200_without_saving(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database_path = tmp_path / "pet.db"
    app = create_app({"TESTING": True, "DATABASE": str(database_path)})
    client = app.test_client()
    client.get("/api/pet")
    save_calls: list[tuple[object, ...]] = []
    monkeypatch.setattr("app.routes.save_pet", lambda *args: save_calls.append(args))

    response = client.post("/api/pet/action", json={"action": "feed"})

    assert response.status_code == 200
    assert response.json["effective"] is False
    assert response.json["delta"] == {
        "hunger": 0,
        "mood": 0,
        "energy": 0,
        "cleanliness": 0,
    }
    assert response.json["message"] == "已經吃飽了。"
    assert save_calls == []


def test_action_api_rejects_invalid_payload_and_unknown_action(
    tmp_path: Path,
) -> None:
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "pet.db")})
    client = app.test_client()

    invalid_payload = client.post("/api/pet/action", json={})
    unknown_action = client.post("/api/pet/action", json={"action": "dance"})

    assert invalid_payload.status_code == 400
    assert unknown_action.status_code == 400


def test_pet_load_caps_offline_decay_at_24_steps(tmp_path: Path) -> None:
    database_path = tmp_path / "pet.db"
    init_db(database_path)
    save_pet(
        Pet(
            hunger=100,
            mood=100,
            energy=100,
            cleanliness=100,
            updated_at=10,
        ),
        database_path,
    )

    pet = load_pet(
        database_path,
        now=10 + 25 * 3600,
        interval=3600,
        max_steps=24,
    )

    assert pet.hunger == 0
    assert pet.mood == 52
    assert pet.energy == 76
    assert pet.cleanliness == 28
    assert pet.updated_at == 10 + 25 * 3600


def test_app_uses_configured_30_second_decay_interval(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database_path = tmp_path / "pet.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_path),
            "DECAY_INTERVAL_SECONDS": 30,
        }
    )
    save_pet(Pet(updated_at=100), database_path)
    monkeypatch.setattr("app.storage.time.time", lambda: 130)

    response = app.test_client().get("/api/pet")

    assert app.config["DECAY_INTERVAL_SECONDS"] == 30
    assert response.json["hunger"] == 95
    assert response.json["mood"] == 98
    assert response.json["energy"] == 99
    assert response.json["cleanliness"] == 97
    assert response.json["updated_at"] == 130


def test_previous_three_level_database_migrates_stats_to_100(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "previous.db"
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE pet (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                hunger INTEGER NOT NULL,
                mood INTEGER NOT NULL,
                energy INTEGER NOT NULL,
                cleanliness INTEGER NOT NULL,
                stage TEXT NOT NULL,
                updated_at REAL NOT NULL,
                vitality_elapsed REAL NOT NULL DEFAULT 0
            )
            """
        )
        connection.execute(
            """
            INSERT INTO pet
                (id, name, hunger, mood, energy, cleanliness, stage, updated_at)
            VALUES (1, '小雞', 100, 2, 3, 100, 'baby', 100)
            """
        )

    pet = load_pet(database_path, now=100)

    assert pet.energy == 100
    assert pet.mood == 67

    save_pet(Pet(energy=1, mood=2, updated_at=100), database_path)
    persisted = load_pet(database_path, now=100)
    assert persisted.energy == 1
    assert persisted.mood == 2
