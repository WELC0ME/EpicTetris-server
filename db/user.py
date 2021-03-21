import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, default='')
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    best = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created = sqlalchemy.Column(sqlalchemy.String, default='')

    def set_password(self, _password):
        self.password = generate_password_hash(_password)

    def check_password(self, _password):
        return check_password_hash(self.password, _password)
