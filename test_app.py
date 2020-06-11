import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


assistant_token = os.environ['ASSISTANT_TOKEN']
director_token = os.environ['DIRECTOR_TOKEN']
producer_token = os.environ['PRODUCER_TOKEN']


class AgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # drop all tables
            self.db.drop_all()
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Test name',
            'age': 0,
            'gender': 'Test gender'
        }
        self.new_movie = {
            'title': 'Test name',
            'release_date': '01/01/2000'
        }
        self.patched_actor = {
            'name': 'Patched name',
            'age': 100,
            'gender': 'Patched gender'
        }
        self.patched_movie = {
            'title': 'Patched title',
            'release_date': '12/12/1000'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests

    #  Casting Assistant
    #  ----------------------------------------------------------------

    # Actors
    def test_get_actors_as_an_assistant(self):
        res = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_403_if_post_actor_as_an_assistant(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_if_patch_actor_as_assistant(self):
        res = self.client().patch(
            '/actors/50',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_if_delete_actor_as_an_assistant(self):
        res = self.client().delete(
            '/actors/50',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Movies
    def test_get_movies_as_an_assistant(self):
        res = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_403_if_post_movie_as_an_assistant(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_if_patch_movie_as_assistant(self):
        res = self.client().patch(
            '/movies/50',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_if_delete_movie_as_an_assistant(self):
        res = self.client().delete(
            '/movies/50',
            headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    #  Casting Director
    #  ----------------------------------------------------------------

    # Actors
    def test_get_actors_as_a_director(self):
        res = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_post_actor_as_a_director(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_patch_actor_as_a_director(self):
        self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {producer_token}'})

        actor_id = Actor.query.first().id
        res = self.client().patch(
            f'/actors/{actor_id}',
            json=self.patched_actor,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_as_a_director(self):
        self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {producer_token}'})

        actor_id = Actor.query.first().id
        res = self.client().delete(
            f'/actors/{actor_id}',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(actor, None)

    # Movies
    def test_get_movies_as_a_director(self):
        res = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_403_if_post_movie_as_a_director(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_patch_movie_as_a_director(self):
        self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {producer_token}'})

        movie_id = Movie.query.first().id
        res = self.client().patch(
            f'/movies/{movie_id}',
            json=self.patched_movie,
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_403_if_delete_movie_as_a_director(self):
        self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {producer_token}'})

        movie_id = Movie.query.first().id
        res = self.client().delete(
            f'/movies/{movie_id}',
            headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    #  Executive Producer
    #  ----------------------------------------------------------------
    #
    # Actors
    def test_get_actors_as_a_producer(self):
        res = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_post_actor_as_a_producer(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_patch_actor_as_a_producer(self):
        self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {producer_token}'})

        actor_id = Actor.query.first().id
        res = self.client().patch(
            f'/actors/{actor_id}',
            json=self.patched_actor,
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_delete_actor_as_a_producer(self):
        self.client().post(
            '/actors',
            json=self.new_actor,
            headers={'Authorization': f'Bearer {producer_token}'})

        actor_id = Actor.query.first().id
        res = self.client().delete(
            f'/actors/{actor_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(actor, None)

    # Movies
    def test_get_movies_as_a_producer(self):
        res = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_post_movie_as_a_producer(self):
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_patch_movie_as_a_producer(self):
        self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {producer_token}'})

        movie_id = Movie.query.first().id
        res = self.client().patch(
            f'/movies/{movie_id}',
            json=self.patched_movie,
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_delete_movie_as_a_producer(self):
        self.client().post(
            '/movies',
            json=self.new_movie,
            headers={'Authorization': f'Bearer {producer_token}'})

        movie_id = Movie.query.first().id
        res = self.client().delete(
            f'/movies/{movie_id}',
            headers={'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertEqual(movie, None)

    # General tests
    def test_405_if_getting_actor_not_allowed(self):
        res = self.client().get('/actors/1', headers={
            'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/9999', headers={
            'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_if_getting_movie_not_allowed(self):
        res = self.client().get('/movies/1', headers={
            'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/9999', headers={
            'Authorization': f'Bearer {producer_token}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/1000', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_405_if_movie_creation_not_allowed(self):
        res = self.client().post('/movies/1000', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


if __name__ == "__main__":
    unittest.main()
