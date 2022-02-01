from flask import request
from flask_restx import Resource, Namespace

from security.restrict_edit import admin_required_edit
from security.restrict_write import check_token
from models import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @check_token
    def get(self):
        rs = db.session.query(Genre).all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required_edit
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)

        db.session.add(new_genre)
        db.session.commit()
        return "", 201


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @check_token
    def get(self, rid):
        r = db.session.query(Genre).get(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required_edit
    def put(self, bid):
        genre = db.session.query(Genre).get(bid)
        req_json = request.json
        genre.name = req_json.get("name")

        db.session.add(genre)
        db.session.commit()
        return "", 204

    @admin_required_edit
    def delete(self, bid):
        genre = db.session.query(Genre).get(bid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204
