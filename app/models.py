from . import db
from werkzeug.security import generate_password_hash

class Property(db.Model):
    __tablename__ = 'property'

    id  = db.Column(db.Integer, primary_key  = True, autoincrement=True)
    title =db.Column(db.String(255), unique=True)
    bedrooms = db.Column(db.String(255))
    bathrooms = db.Column(db.String(255))
    location= db.Column(db.String(255))
    price = db.Column (db.Integer)
    type = db.Column (db.String(255))
    description = db.Column (db.String(255))
    photo = db.Column (db.String)

    def __init__(self, title, bedrooms,bathrooms, location, price, type, description, photo):
        self.title = title
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.location = location
        self.price= price
        self.description = description
        self.type = type
        self.photo = photo