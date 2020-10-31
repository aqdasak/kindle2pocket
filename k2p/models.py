from werkzeug.security import generate_password_hash

from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(), unique=True, nullable=False)
    _hashed_password = db.Column(db.String(255), nullable=False, server_default='')
    access_token = db.Column(db.String(33))

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, unhashed_password):
        self._hashed_password = generate_password_hash(unhashed_password)
