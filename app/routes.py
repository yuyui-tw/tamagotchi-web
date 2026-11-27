from dataclasses import asdict
from pathlib import Path

from flask import Blueprint, Response, current_app, jsonify, render_template, request

from app.pet import apply_action
from app.storage import load_pet, save_pet

bp = Blueprint("main", __name__)


def _database_path() -> Path:
    return Path(current_app.config["DATABASE"])


@bp.get("/")
def index() -> str:
    return render_template("index.html")


@bp.get("/api/pet")
def get_pet() -> Response:
    return jsonify(asdict(load_pet(_database_path())))


@bp.post("/api/pet/action")
def perform_action() -> Response | tuple[Response, int]:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("action"), str):
        return jsonify(error="請提供有效的 action。"), 400

    pet = load_pet(_database_path())
    try:
        pet = apply_action(pet, payload["action"])
    except ValueError:
        return jsonify(error="不支援此操作。"), 400

    save_pet(pet, _database_path())
    return jsonify(asdict(pet))
