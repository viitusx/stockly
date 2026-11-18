
from pathlib import Path

from flask import Flask

from config import Config
from app.extensions import db, migrate, login_manager, bcrypt


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    app.config.from_object(Config)

    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Importação dos modelos
    from app import models

    # Carregamento dos usuários
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User

        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    # Registro das rotas
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app