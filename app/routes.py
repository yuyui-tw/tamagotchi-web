from dataclasses import asdict
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, render_template, request

from app.pet import ACTION_MAIN_STATS, STAT_NAMES, Pet, apply_action, get_status
from app.storage import load_pet, save_pet

bp = Blueprint("main", __name__)

ACTION_MESSAGES: dict[str, tuple[str, str, str]] = {
    "feed": ("餵食了", "飽食度", "已經吃飽了。"),
    "play": ("玩耍了", "心情", "心情已經很好了。"),
    "sleep": ("休息了", "體力", "體力已經充足了。"),
    "clean": ("清潔完成", "清潔度", "已經很乾淨了。"),
}


def _database_path() -> Path:
    return Path(current_app.config["DATABASE"])


def _load_pet() -> Pet:
    return load_pet(
        _database_path(),
        interval=current_app.config["DECAY_INTERVAL_SECONDS"],
    )


@bp.get("/")
def index() -> str:
    return render_template("index.html")


@bp.get("/api/pet")
def get_pet() -> Response:
    pet = _load_pet()
    return jsonify({**asdict(pet), "status": get_status(pet)})


@bp.post("/api/pet/action")
def perform_action() -> Response | tuple[Response, int]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("action"), str):
        return jsonify(error="請提供有效的 action。"), 400

    pet = _load_pet()
    before = pet
    try:
        pet = apply_action(pet, payload["action"])
    except ValueError:
        return jsonify(error="不支援此操作。"), 400

    delta = {
        name: getattr(pet, name) - getattr(before, name)
        for name in STAT_NAMES
    }
    effective = any(delta.values())
    action_label, stat_label, no_effect_message = ACTION_MESSAGES[payload["action"]]

    if effective:
        save_pet(pet, _database_path())
        amount = delta[ACTION_MAIN_STATS[payload["action"]]]
        message = f"{action_label}，{stat_label} {amount:+d}"
    else:
        message = no_effect_message

    return jsonify(
        {
            **asdict(pet),
            "status": get_status(pet),
            "delta": delta,
            "effective": effective,
            "message": message,
        }
    )
