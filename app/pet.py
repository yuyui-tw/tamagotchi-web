import time
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Pet:
    name: str = "小雞"
    hunger: int = 80
    mood: int = 70
    energy: int = 80
    cleanliness: int = 80
    stage: str = "baby"
    updated_at: float = 0.0


def clamp(value: int) -> int:
    return max(0, min(100, value))


def apply_action(pet: Pet, action: str, now: float | None = None) -> Pet:
    updated_at = time.time() if now is None else now

    if action == "feed":
        return replace(
            pet,
            hunger=clamp(pet.hunger + 25),
            mood=clamp(pet.mood + 5),
            cleanliness=clamp(pet.cleanliness - 2),
            updated_at=updated_at,
        )
    if action == "play":
        return replace(
            pet,
            hunger=clamp(pet.hunger - 5),
            mood=clamp(pet.mood + 15),
            energy=clamp(pet.energy - 10),
            updated_at=updated_at,
        )
    if action == "sleep":
        return replace(
            pet,
            hunger=clamp(pet.hunger - 2),
            energy=clamp(pet.energy + 30),
            updated_at=updated_at,
        )
    if action == "clean":
        return replace(
            pet,
            mood=clamp(pet.mood + 2),
            cleanliness=clamp(pet.cleanliness + 30),
            updated_at=updated_at,
        )
    raise ValueError(f"Unknown action: {action}")


def decay(pet: Pet, elapsed_seconds: float) -> Pet:
    elapsed_hours = min(24, max(0, int(elapsed_seconds // 3600)))
    if elapsed_hours == 0:
        return pet

    return replace(
        pet,
        hunger=clamp(pet.hunger - 5 * elapsed_hours),
        mood=clamp(pet.mood - 2 * elapsed_hours),
        energy=clamp(pet.energy - elapsed_hours),
        cleanliness=clamp(pet.cleanliness - 3 * elapsed_hours),
        updated_at=pet.updated_at + elapsed_hours * 3600,
    )
