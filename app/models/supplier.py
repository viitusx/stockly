
from app.extensions import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(db.String(120))

    phone = db.Column(db.String(20))

    document = db.Column(db.String(30))

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    products = db.relationship(
        "Product",
        back_populates="supplier"
    )

    def __repr__(self):
        return f"<Supplier {self.name}>"