
from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    sku = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    description = db.Column(db.Text)

    cost_price = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    sale_price = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    min_quantity = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    category = db.relationship(
        "Category",
        back_populates="products"
    )

    supplier = db.relationship(
        "Supplier",
        back_populates="products"
    )

    def __repr__(self):
        return f"<Product {self.name}>"