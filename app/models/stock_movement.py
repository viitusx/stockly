from datetime import datetime, timezone

from app.extensions import db


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    __table_args__ = (
        db.CheckConstraint(
            "quantity > 0",
            name="ck_stock_movements_quantity_positive"
        ),
        db.CheckConstraint(
            "movement_type IN ('entry', 'exit')",
            name="ck_stock_movements_type"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    movement_type = db.Column(
        db.String(10),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    reason = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    product = db.relationship("Product")
    user = db.relationship("User")

    def __repr__(self):
        return f"<StockMovement {self.movement_type}: {self.quantity}>"