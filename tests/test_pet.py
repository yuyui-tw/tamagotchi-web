import pytest

from app.pet import Pet, apply_action, decay, get_status


def test_apply_action_changes_stats_clamps_and_preserves_updated_at() -> None:
    pet = Pet(hunger=90, mood=95, energy=20, cleanliness=1, updated_at=100)

    updated = apply_action(pet, "feed")

    assert updated.hunger == 100
    assert updated.mood == 100
    assert updated.cleanliness == 0
    assert updated.updated_at == pet.updated_at
    assert pet.hunger == 90


def test_decay_uses_hour_intervals_and_preserves_partial_interval() -> None:
    pet = Pet(
        hunger=100,
        mood=70,
        energy=80,
        cleanliness=80,
        updated_at=100,
    )

    updated = decay(pet, 5400, interval=3600)

    assert updated.hunger == 95
    assert updated.mood == 68
    assert updated.energy == 79
    assert updated.cleanliness == 77
    assert updated.updated_at == 3700


def test_decay_uses_30_second_intervals_and_keeps_remainder() -> None:
    pet = Pet(updated_at=100)

    updated = decay(pet, 65, interval=30)

    assert updated.hunger == 90
    assert updated.mood == 96
    assert updated.energy == 98
    assert updated.cleanliness == 94
    assert updated.updated_at == 160
    assert updated.updated_at - pet.updated_at == 60
    assert 65 - (updated.updated_at - pet.updated_at) == 5


@pytest.mark.parametrize("action", ["feed", "play", "sleep", "clean"])
def test_action_with_full_primary_stat_returns_original_pet(action: str) -> None:
    pet = Pet()

    assert apply_action(pet, action) is pet


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        ("feed", (75, 55, 50, 48)),
        ("play", (45, 65, 40, 50)),
        ("sleep", (48, 50, 80, 50)),
        ("clean", (50, 52, 50, 80)),
    ],
)
def test_actions_apply_their_stat_changes(
    action: str, expected: tuple[int, int, int, int]
) -> None:
    updated = apply_action(
        Pet(hunger=50, mood=50, energy=50, cleanliness=50),
        action,
    )

    assert (
        updated.hunger,
        updated.mood,
        updated.energy,
        updated.cleanliness,
    ) == expected


def test_unknown_action_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown action: dance"):
        apply_action(Pet(), "dance")


@pytest.mark.parametrize(
    ("pet", "expected_status"),
    [
        (Pet(hunger=0, energy=0), "critical"),
        (Pet(hunger=29), "hungry"),
        (Pet(energy=29), "sleepy"),
        (Pet(cleanliness=29), "dirty"),
        (Pet(mood=29), "sad"),
        (Pet(), "happy"),
        (Pet(hunger=70, mood=70, energy=70, cleanliness=70), "happy"),
        (Pet(hunger=69), "normal"),
    ],
)
def test_get_status_returns_expected_status(pet: Pet, expected_status: str) -> None:
    assert get_status(pet) == expected_status
