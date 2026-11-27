from pathlib import Path

from flask import Flask

from app.routes import bp
from app.storage import init_db

DEFAULT_DATABASE = Path(__file__).resolve().parent.parent / "data" / "pet.db"


def create_app(test_config: dict[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(DATABASE=str(DEFAULT_DATABASE))
    if test_config is not None:
        app.config.update(test_config)

    init_db(Path(app.config["DATABASE"]))
    app.register_blueprint(bp)
    return app
