import sqlite3
import time
from dataclasses import replace
from pathlib import Path

from app.pet import Pet, decay

DEFAULT_DATABASE = Path(__file__).resolve().parent.parent / "data" / "pet.db"


def init_db(database_path: Path = DEFAULT_DATABASE) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pet (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT NOT NULL,
                hunger INTEGER NOT NULL,
                mood INTEGER NOT NULL,
                energy INTEGER NOT NULL,
                cleanliness INTEGER NOT NULL,
                stage TEXT NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )


def save_pet(pet: Pet, database_path: Path = DEFAULT_DATABASE) -> None:
    init_db(database_path)
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            INSERT INTO pet (
                id, name, hunger, mood, energy, cleanliness, stage, updated_at
            ) VALUES (1, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                hunger = excluded.hunger,
                mood = excluded.mood,
                energy = excluded.energy,
                cleanliness = excluded.cleanliness,
                stage = excluded.stage,
                updated_at = excluded.updated_at
            """,
            (
                pet.name,
                pet.hunger,
                pet.mood,
                pet.energy,
                pet.cleanliness,
                pet.stage,
                pet.updated_at,
            ),
        )


def load_pet(
    database_path: Path = DEFAULT_DATABASE, now: float | None = None
) -> Pet:
    current_time = time.time() if now is None else now
    init_db(database_path)

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute("SELECT * FROM pet WHERE id = 1").fetchone()

    if row is None:
        pet = replace(Pet(), updated_at=current_time)
        save_pet(pet, database_path)
        return pet

    pet = Pet(
        name=row["name"],
        hunger=row["hunger"],
        mood=row["mood"],
        energy=row["energy"],
        cleanliness=row["cleanliness"],
        stage=row["stage"],
        updated_at=row["updated_at"],
    )
    elapsed_seconds = max(0, current_time - pet.updated_at)
    if elapsed_seconds > 86400:
        pet = replace(decay(pet, 86400), updated_at=current_time)
    else:
        pet = decay(pet, elapsed_seconds)

    if pet.updated_at != row["updated_at"] or elapsed_seconds > 86400:
        save_pet(pet, database_path)
    return pet
