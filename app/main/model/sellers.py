from .. import db
import datetime


class Sellers(db.Model):
    """ Sellers Model """
    __tablename__ = 'sellers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)    
    public_id = db.Column(db.String(100), unique=True)
    created_on = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean(), default=False)
