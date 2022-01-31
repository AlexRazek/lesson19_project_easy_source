from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        rs = db.session.query(User).all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        new_user = User(**req_json)

        db.session.add(new_user)
        db.session.commit()
        return "", 201



@user_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid):
        b = db.session.query(User).get(bid)
        sm_d = UserSchema().dump(b)
        return sm_d, 200

    def get_by_username(self, username: str):
        return db.session.query(User).filter(User.username == username).one_or_none()

    def update_role(self, user_name: str, role : str):
        user = db.session.get_by_username(user_name)
        user.role = role
        db.session.add(user)
        db.session.commit()

    def update_password(self, user_name: str, password : str):
        user = db.session.get_by_username(user_name)
        user.password = password
        db.session.add(user)
        db.session.commit()

    def put(self, bid):
        user = db.session.query(User).get(bid)
        req_json = request.json
        user.username = req_json.get("username")
        user.password = req_json.get("password")
        user.role = req_json.get("role")

        db.session.add(user)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        user = db.session.query(User).get(bid)
        db.session.delete(user)
        db.session.commit()
        return "", 204
