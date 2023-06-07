from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.card import Card, CardSchema
from models.user import User

cards_bp = Blueprint("cards", __name__)


@cards_bp.route("/cards")
@jwt_required()
def all_cards():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not user.is_admin:
        return {"error": "You must be an admin"}, 401

    # select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)
