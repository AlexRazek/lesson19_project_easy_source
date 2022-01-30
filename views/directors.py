from flask import request
from flask_restx import Resource, Namespace

from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)

        db.session.add(new_director)
        db.session.commit()
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    def put(self, bid):
        director = db.session.query(Director).get(bid)
        req_json = request.json
        director.name = req_json.get("name")

        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, bid):
        director = db.session.query(Director).get(bid)
        db.session.delete(director)
        db.session.commit()
        return "", 204
