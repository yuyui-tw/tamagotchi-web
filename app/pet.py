from dataclasses import dataclass, replace

DEFAULT_DECAY_INTERVAL: int = 30  # 正式版改為 3600
MAX_DECAY_STEPS: int = 24

ACTION_MAIN_STATS: dict[str, str] = {
    "feed": "hunger",
    "play": "mood",
    "sleep": "energy",
    "clean": "cleanliness",
}

STAT_NAMES: tuple[str, ...] = ("hunger", "mood", "energy", "cleanliness")


@dataclass(frozen=True)
class Pet:
    name: str = "小雞"
    hunger: int = 100
    mood: int = 100
    energy: int = 100
    cleanliness: int = 100
    stage: str = "baby"
    updated_at: float = 0.0


def clamp(value: int) -> int:
    return max(0, min(100, value))


def apply_action(pet: Pet, action: str) -> Pet:
    if action not in ACTION_MAIN_STATS:
        raise ValueError(f"Unknown action: {action}")

    if getattr(pet, ACTION_MAIN_STATS[action]) == 100:
        return pet

    if action == "feed":
        return replace(
            pet,
            hunger=clamp(pet.hunger + 25),
            mood=clamp(pet.mood + 5),
            cleanliness=clamp(pet.cleanliness - 2),
        )
    if action == "play":
        return replace(
            pet,
            hunger=clamp(pet.hunger - 5),
            mood=clamp(pet.mood + 15),
            energy=clamp(pet.energy - 10),
        )
    if action == "sleep":
        return replace(
            pet,
            hunger=clamp(pet.hunger - 2),
            energy=clamp(pet.energy + 30),
        )
    return replace(
        pet,
        mood=clamp(pet.mood + 2),
        cleanliness=clamp(pet.cleanliness + 30),
    )


def decay(
    pet: Pet,
    elapsed_seconds: float,
    interval: int = DEFAULT_DECAY_INTERVAL,
    max_steps: int = MAX_DECAY_STEPS,
) -> Pet:
    if interval <= 0:
        raise ValueError("interval must be positive")
    if max_steps < 0:
        raise ValueError("max_steps must not be negative")

    steps = min(max_steps, max(0, int(elapsed_seconds // interval)))
    if steps == 0:
        return pet

    return replace(
        pet,
        hunger=clamp(pet.hunger - 5 * steps),
        mood=clamp(pet.mood - 2 * steps),
        energy=clamp(pet.energy - steps),
        cleanliness=clamp(pet.cleanliness - 3 * steps),
        updated_at=pet.updated_at + steps * interval,
    )


def get_status(pet: Pet) -> str:
    if any(getattr(pet, name) == 0 for name in STAT_NAMES):
        return "critical"
    if pet.hunger < 30:
        return "hungry"
    if pet.energy < 30:
        return "sleepy"
    if pet.cleanliness < 30:
        return "dirty"
    if pet.mood < 30:
        return "sad"
    if all(getattr(pet, name) >= 70 for name in STAT_NAMES):
        return "happy"
    return "normal"
