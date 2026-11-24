from sqlalchemy import update
from sqlalchemy.orm import joinedload

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.product import Product
from app.models.stock_movement import StockMovement


movements_bp = Blueprint(
    "movements",
    __name__,
    url_prefix="/movements"
)


# HISTÓRICO DE MOVIMENTAÇÕES
@movements_bp.route("/")
@login_required
def list_movements():

    movements = StockMovement.query.options(
        joinedload(StockMovement.product),
        joinedload(StockMovement.user)
    ).order_by(
        StockMovement.created_at.desc()
    ).all()

    return render_template(
        "movements/list.html",
        movements=movements
    )


# REGISTRAR MOVIMENTAÇÃO
@movements_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_movement():

    products = Product.query.filter_by(
        is_active=True
    ).order_by(
        Product.name.asc()
    ).all()

    if request.method == "POST":

        try:
            product_id = int(request.form.get("product_id", ""))
            quantity = int(request.form.get("quantity", ""))
            movement_type = request.form.get("movement_type", "").strip()
            reason = request.form.get("reason", "").strip()

            if quantity <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")

            if movement_type not in ("entry", "exit"):
                raise ValueError("Selecione um tipo de movimentação válido.")

            product = db.session.get(Product, product_id)

            if not product or not product.is_active:
                raise ValueError("Produto não encontrado ou inativo.")

            # ENTRADA: aumenta o estoque
            if movement_type == "entry":

                result = db.session.execute(
                    update(Product)
                    .where(
                        Product.id == product_id,
                        Product.is_active.is_(True)
                    )
                    .values(
                        quantity=Product.quantity + quantity
                    )
                    .execution_options(synchronize_session=False)
                )

            # SAÍDA: diminui o estoque somente se houver saldo
            else:

                result = db.session.execute(
                    update(Product)
                    .where(
                        Product.id == product_id,
                        Product.is_active.is_(True),
                        Product.quantity >= quantity
                    )
                    .values(
                        quantity=Product.quantity - quantity
                    )
                    .execution_options(synchronize_session=False)
                )

            if result.rowcount != 1:
                raise ValueError(
                    "Estoque insuficiente para realizar essa saída."
                )

            movement = StockMovement(
                product_id=product_id,
                user_id=current_user.id,
                movement_type=movement_type,
                quantity=quantity,
                reason=reason or None
            )

            db.session.add(movement)
            db.session.commit()

            flash("Movimentação registrada com sucesso!", "success")

            return redirect(url_for("movements.list_movements"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

    return render_template(
        "movements/create.html",
        products=products
    )