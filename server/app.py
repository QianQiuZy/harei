import os
import threading
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from server.db import init_db
from server.routes.admin import admin_bp
from server.routes.assets import assets_bp
from server.routes.captains import captains_bp
from server.routes.gifts import gifts_bp
from server.routes.messages import messages_bp
from server.routes.music import music_bp
from server.routes.health import health_bp
from server.services.live_service import LiveService


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__, static_folder=None)
    app.config["JSON_AS_ASCII"] = False
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    init_db()

    app.register_blueprint(health_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(captains_bp)
    app.register_blueprint(gifts_bp)
    app.register_blueprint(assets_bp)

    if os.getenv("BLIVE_IDENTITY_CODE"):
        live_service = LiveService()
        thread = threading.Thread(target=live_service.run, daemon=True)
        thread.start()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
