import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #  Actors
    #  ----------------------------------------------------------------

    # An endpoint to GET all actors
    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': formatted_actors
        }), 200

    # An endpoint to POST new actors
    @app.route('/actors', methods=['POST'])
    def post_actor():
        body = request.get_json()

        id = body.get('id', None)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = Actor(id=id, name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except Exception:
            abort(422)

    # An endpoint to PATCH an actor by id
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def patch_actor(actor_id):
        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = int(body.get('age'))
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200
        except Exception:
            abort(400)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
