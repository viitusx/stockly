
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.extensions import db
from app.models.supplier import Supplier


suppliers_bp = Blueprint(
    "suppliers",
    __name__,
    url_prefix="/suppliers"
)


# LISTAR FORNECEDORES
@suppliers_bp.route("/")
@login_required
def list_suppliers():

    suppliers = Supplier.query.order_by(
        Supplier.name.asc()
    ).all()

    return render_template(
        "suppliers/list.html",
        suppliers=suppliers
    )


# CADASTRAR FORNECEDOR
@suppliers_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_supplier():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        document = request.form.get("document", "").strip()

        if not name:
            flash("O nome do fornecedor é obrigatório.", "danger")
            return redirect(url_for("suppliers.create_supplier"))

        supplier = Supplier(
            name=name,
            email=email or None,
            phone=phone or None,
            document=document or None
        )

        db.session.add(supplier)
        db.session.commit()

        flash("Fornecedor cadastrado com sucesso!", "success")

        return redirect(url_for("suppliers.list_suppliers"))

    return render_template("suppliers/create.html")


# EDITAR FORNECEDOR
@suppliers_bp.route("/edit/<int:supplier_id>", methods=["GET", "POST"])
@login_required
def edit_supplier(supplier_id):

    supplier = db.get_or_404(Supplier, supplier_id)

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        if not name:
            flash("O nome do fornecedor é obrigatório.", "danger")
            return redirect(
                url_for("suppliers.edit_supplier", supplier_id=supplier.id)
            )

        supplier.name = name
        supplier.email = request.form.get("email", "").strip() or None
        supplier.phone = request.form.get("phone", "").strip() or None
        supplier.document = request.form.get("document", "").strip() or None

        db.session.commit()

        flash("Fornecedor atualizado com sucesso!", "success")

        return redirect(url_for("suppliers.list_suppliers"))

    return render_template(
        "suppliers/edit.html",
        supplier=supplier
    )


# DESATIVAR FORNECEDOR
@suppliers_bp.route("/deactivate/<int:supplier_id>", methods=["POST"])
@login_required
def deactivate_supplier(supplier_id):

    supplier = db.get_or_404(Supplier, supplier_id)

    supplier.is_active = False

    db.session.commit()

    flash("Fornecedor desativado com sucesso!", "success")

    return redirect(url_for("suppliers.list_suppliers"))