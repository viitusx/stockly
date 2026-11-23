
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.models.category import Category

categories_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories"
)


# Listar categorias
@categories_bp.route("/")
@login_required
def list_categories():

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "categories/list.html",
        categories=categories
    )


# Cadastrar categoria
@categories_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_category():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("O nome da categoria é obrigatório.", "danger")
            return redirect(url_for("categories.create_category"))

        existing_category = Category.query.filter(
            db.func.lower(Category.name) == name.lower()
        ).first()

        if existing_category:
            flash("Essa categoria já existe.", "danger")
            return redirect(url_for("categories.create_category"))

        category = Category(
            name=name,
            description=description or None
        )

        db.session.add(category)
        db.session.commit()

        flash("Categoria cadastrada com sucesso!", "success")

        return redirect(url_for("categories.list_categories"))

    return render_template("categories/create.html")


# Editar categoria
@categories_bp.route("/edit/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):

    category = db.get_or_404(Category, category_id)

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("O nome da categoria é obrigatório.", "danger")
            return redirect(
                url_for("categories.edit_category", category_id=category.id)
            )

        existing_category = Category.query.filter(
            db.func.lower(Category.name) == name.lower(),
            Category.id != category.id
        ).first()

        if existing_category:
            flash("Já existe outra categoria com esse nome.", "danger")
            return redirect(
                url_for("categories.edit_category", category_id=category.id)
            )

        category.name = name
        category.description = description or None

        db.session.commit()

        flash("Categoria atualizada com sucesso!", "success")

        return redirect(url_for("categories.list_categories"))

    return render_template(
        "categories/edit.html",
        category=category
    )


# Desativar categoria
@categories_bp.route("/deactivate/<int:category_id>", methods=["POST"])
@login_required
def deactivate_category(category_id):

    category = db.get_or_404(Category, category_id)

    if category.products:
        flash(
            "Não é possível desativar uma categoria que possui produtos vinculados.",
            "danger"
        )
        return redirect(url_for("categories.list_categories"))

    category.is_active = False

    db.session.commit()

    flash("Categoria desativada com sucesso!", "success")

    return redirect(url_for("categories.list_categories"))