import pytest

from app.pet import Pet, apply_action, decay


def test_apply_action_changes_stats_and_clamps_values() -> None:
    pet = Pet(hunger=90, mood=95, energy=20, cleanliness=1)

    updated = apply_action(pet, "feed", now=100)

    assert updated.hunger == 100
    assert updated.mood == 100
    assert updated.cleanliness == 0
    assert updated.updated_at == 100
    assert pet.hunger == 90


def test_decay_applies_full_hours_and_preserves_partial_hour() -> None:
    pet = Pet(updated_at=100)

    updated = decay(pet, 5400)

    assert updated.hunger == 75
    assert updated.mood == 68
    assert updated.energy == 79
    assert updated.cleanliness == 77
    assert updated.updated_at == 3700


def test_unknown_action_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown action: dance"):
        apply_action(Pet(), "dance", now=100)
