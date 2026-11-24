
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

    # Configuração do Flask-Login
    login_manager.login_view = "auth.login"

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
    from app.routes.auth import auth_bp
    from app.routes.categories import categories_bp
    from app.routes.suppliers import suppliers_bp
    from app.routes.products import products_bpgit add .
    from app.models.stock_movement import StockMovement
    from app.register_blueprint(movements_bp)

    app.register_blueprint(categories_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(movements_bp)

    return app