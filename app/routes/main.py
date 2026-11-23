
from flask import Blueprint, render_template
from flask_login import login_required

from app.extensions import db
from app.models.product import Product
from app.models.category import Category

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():

    # Total de produtos ativos
    total_products = Product.query.filter_by(
        is_active=True
    ).count()

    # Total de categorias ativas
    total_categories = Category.query.filter_by(
        is_active=True
    ).count()

    # Produtos com estoque baixo
    low_stock = Product.query.filter(
        Product.is_active.is_(True),
        Product.quantity <= Product.min_quantity
    ).count()

    # Valor estimado do estoque pelo preço de custo
    inventory_value = db.session.query(
        db.func.coalesce(
            db.func.sum(Product.quantity * Product.cost_price),
            0
        )
    ).filter(
        Product.is_active.is_(True)
    ).scalar()

    return render_template(
        "index.html",
        total_products=total_products,
        total_categories=total_categories,
        low_stock=low_stock,
        inventory_value=inventory_value
    )