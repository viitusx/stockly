from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier


products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)


def get_form_data():
    """Obtém e valida os dados enviados pelo formulário."""

    name = request.form.get("name", "").strip()
    sku = request.form.get("sku", "").strip().upper()
    description = request.form.get("description", "").strip()

    try:
        cost_price = Decimal(
            request.form.get("cost_price", "0").replace(",", ".")
        )
        sale_price = Decimal(
            request.form.get("sale_price", "0").replace(",", ".")
        )

        min_quantity = int(request.form.get("min_quantity", "0"))
        category_id = int(request.form.get("category_id", "0"))

        supplier_value = request.form.get("supplier_id", "").strip()
        supplier_id = int(supplier_value) if supplier_value else None

    except (ValueError, InvalidOperation):
        raise ValueError("Verifique os valores informados.")

    if not name or not sku:
        raise ValueError("Nome e SKU são obrigatórios.")

    if not cost_price.is_finite() or not sale_price.is_finite():
        raise ValueError("Os preços informados são inválidos.")

    if cost_price < 0 or sale_price < 0:
        raise ValueError("Os preços não podem ser negativos.")

    if cost_price > Decimal("99999999.99") or sale_price > Decimal("99999999.99"):
        raise ValueError("O preço ultrapassa o limite permitido.")

    if min_quantity < 0:
        raise ValueError("O estoque mínimo não pode ser negativo.")

    category = db.session.get(Category, category_id)

    if not category or not category.is_active:
        raise ValueError("Selecione uma categoria válida.")

    supplier = None

    if supplier_id is not None:
        supplier = db.session.get(Supplier, supplier_id)

        if not supplier or not supplier.is_active:
            raise ValueError("Selecione um fornecedor válido.")

    return {
        "name": name,
        "sku": sku,
        "description": description or None,
        "cost_price": cost_price,
        "sale_price": sale_price,
        "min_quantity": min_quantity,
        "category_id": category.id,
        "supplier_id": supplier.id if supplier else None
    }


def get_form_options():
    """Retorna categorias e fornecedores ativos."""

    categories = Category.query.filter_by(
        is_active=True
    ).order_by(Category.name.asc()).all()

    suppliers = Supplier.query.filter_by(
        is_active=True
    ).order_by(Supplier.name.asc()).all()

    return categories, suppliers


# LISTAR PRODUTOS
@products_bp.route("/")
@login_required
def list_products():

    products = Product.query.order_by(
        Product.name.asc()
    ).all()

    return render_template(
        "products/list.html",
        products=products
    )


# CADASTRAR PRODUTO
@products_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_product():

    categories, suppliers = get_form_options()

    if request.method == "POST":

        try:
            data = get_form_data()

            existing_product = Product.query.filter(
                db.func.lower(Product.sku) == data["sku"].lower()
            ).first()

            if existing_product:
                raise ValueError("Já existe um produto com esse SKU.")

            product = Product(**data)

            # A quantidade inicial começa em zero.
            # As entradas serão registradas pelo controle de movimentações.

            db.session.add(product)
            db.session.commit()

            flash("Produto cadastrado com sucesso!", "success")

            return redirect(url_for("products.list_products"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

    return render_template(
        "products/create.html",
        categories=categories,
        suppliers=suppliers
    )


# EDITAR PRODUTO
@products_bp.route("/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):

    product = db.get_or_404(Product, product_id)
    categories, suppliers = get_form_options()

    if request.method == "POST":

        try:
            data = get_form_data()

            existing_product = Product.query.filter(
                db.func.lower(Product.sku) == data["sku"].lower(),
                Product.id != product.id
            ).first()

            if existing_product:
                raise ValueError("Esse SKU já está sendo utilizado.")

            for field, value in data.items():
                setattr(product, field, value)

            db.session.commit()

            flash("Produto atualizado com sucesso!", "success")

            return redirect(url_for("products.list_products"))

        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")

    return render_template(
        "products/edit.html",
        product=product,
        categories=categories,
        suppliers=suppliers
    )


# DESATIVAR PRODUTO
@products_bp.route("/deactivate/<int:product_id>", methods=["POST"])
@login_required
def deactivate_product(product_id):

    product = db.get_or_404(Product, product_id)

    product.is_active = False

    db.session.commit()

    flash("Produto desativado com sucesso!", "success")

    return redirect(url_for("products.list_products"))