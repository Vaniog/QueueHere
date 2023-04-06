from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login

from hashlib import sha1
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    queues = db.relationship('UserQueue', back_populates='member', cascade='all, delete-orphan, merge, save-update')
    owned_queues = db.relationship('Queue', back_populates='admin')

    is_guest = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(30), default='')
    name_to_print = db.Column(db.String(30), default="")

    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    @staticmethod
    def generate_ip_hash(ip_address):
        return sha1(ip_address.encode('utf-8')).hexdigest()[15:44]

    def set_ip_address(self, ip_address):
        self.ip_address = self.generate_ip_hash(ip_address)

    def check_ip_address(self, ip_address):
        return self.ip_address == self.generate_ip_hash(ip_address)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
