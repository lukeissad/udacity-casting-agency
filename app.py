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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
