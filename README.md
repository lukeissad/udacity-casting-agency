# Udacity Capstone Project - Casting Agency

Hosted on Heroku: https://agencyfsnd.herokuapp.com/

## Motivation

This is the capstone project for the Udacity Full-Stack Web Development Nanodegree

## Setup

### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

### Virtual Environment

Working within a virtual environment is recommended. It keeps your dependencies separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the project directory and running:

```bash
pip install requirements.txt
```

This will install all of the required packages specified within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight sqlite database.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [PostgreSQL](https://www.postgresql.org/) is a powerful, open source object-relational database system that we'll use for our databases.

### Environment Variables

In your terminal run `setup.sh` as source to use all the needed variables defined in setup.sh.

```bash
source setup.sh
```

### Running the server

To run the server, execute:

```bash
flask run
```

`FLASK_ENV` variable is present in the `setup.sh` file and is set to `development`. Development environment will detect file changes and restart the server automatically.

### Generating new authorization tokens

To generate new authorization tokens log into the app using the following link:

[Authorization link](https://agencyfsnd.eu.auth0.com/authorize?audience=Agency&response_type=token&client_id=YgeULYwoufeLSqnsYuvVZatPXBHJbsm2&redirect_uri=http://localhost:5000/login-results)

After logging in you'll find the token for the particular role in the address bar. Copy it.

#### Login information

1. Assistant

```
email: assistant@agencyfsnd.com
password: Agencytest1
```

2. Director

```
email: director@agencyfsnd.com
password: Agencytest1
```

3. Producer

```
email: producer@agencyfsnd.com
password: Agencytest1
```

### Database Setup
With Postgres running, create two databases a main one, and one meant for testing.

```bash
$ psql
postgres=> CREATE DATABASE casting_agency;
postgres=> CREATE DATABASE casting_agency_test;
postgres=>\q
```

## Endpoints

#### GET '/actors'
- General:
    - Returns all actors.
    - Authorization required: Casting Assistant, Casting Director, Executive Producer
- Sample: `curl -X GET 'localhost:5000/actors' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN>'`

``` {
  "actors": [
    {
      "age": 82,
      "gender": "male",
      "id": 50,
      "name": "Anthony Hopkins"
    },
    {
      "age": 70,
      "gender": "female",
      "id": 5,
      "name": "Meryl Streep"
    }
  ],
  "success": true
}
```

#### GET '/movies'
- General:
    - Returns all movies.
    - Authorization required: Casting Assistant, Casting Director, Executive Producer.
- Sample: `curl -X GET 'localhost:5000/movies' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN>'`

``` {
  "movies": [
    {
      "id": 60,
      "release_date": "Fri, 30 Jun 2006 00:00:00 GMT",
      "title": "The Devil Wears Prada"
    },
    {
      "id": 50,
      "release_date": "Thu, 14 Feb 1991 00:00:00 GMT",
      "title": "The Silence of the Lambs"
    }
  ],
  "success": true
}
```

#### POST '/actors'
- General:
    - Adds a new actor to the database.
    - Authorization required: Casting Director, Executive Producer.
- Sample: `curl -X POST 'localhost:5000/actors' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN>' -H 'Content-Type: application/json' -d '{"id": 50, "name": "Anthony Hopkins", "age": 82, "gender": "male"}'`

``` {
  "actor": {
    "age": 82,
    "gender": "male",
    "id": 50,
    "name": "Anthony Hopkins"
  },
  "success": true
}
```

#### POST '/movies'
- General:
    - Adds a new movie to the database.
    - Authorization required: Executive Producer.
- Sample: `curl -X POST 'localhost:5000/movies' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN> -H 'Content-Type: application/json' -d '{"id": 50, "title": "The Silence of the Lambs", "release_date": "14/02/1991"}'`

``` {
  "movie": {
    "id": 50,
    "release_date": "Thu, 14 Feb 1991 00:00:00 GMT",
    "title": "The Silence of the Lambs"
  },
  "success": true
}
```

#### PATCH '/actors/<int:actor_id>'
- General:
    - Edits an actor present in the database.
    - Authorization required: Casting Director, Executive Producer.
- Sample: `curl -X PATCH 'localhost:5000/actors/50' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN> -H 'Content-Type: application/json' -d '{"name": "Meryl Streep", "age": 70, "gender": "female"}'`

``` {
  "actor": {
    "age": 70,
    "gender": "female",
    "id": 50,
    "name": "Meryl Streep"
  },
  "success": true
}
```


#### PATCH '/movies/<int:movie_id>'
- General:
    - Edits a movie present in the database.
    - Authorization required: Casting Director, Executive Producer.
- Sample: `curl -X PATCH 'localhost:5000/movies/50' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN> -H 'Content-Type: application/json' -d '{"title": "The Devil Wears Prada", "release_date": "30/06/2006"}'`

``` {
  "movie": {
    "id": 50,
    "release_date": "Fri, 30 Jun 2006 00:00:00 GMT",
    "title": "The Devil Wears Prada"
  },
  "success": true
}
```

#### DELETE '/actors/<int:actor_id>'
- General:
    - Deletes an actor with the given ID, if present in the database.
    - Request Arguments: `actor_id`
    - Authorization required: Casting Director, Executive Producer.
- Sample: `curl -X DELETE 'localhost:5000/actors/50' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN>`

``` {
  "deleted": 50,
  "success": true
}
```

#### DELETE '/movies/<int:movie_id>'
- General:
    - Deletes a movie with the given ID, if present in the database.
    - Request Arguments: `movie_id`
    - Authorization required: Executive Producer.
- Sample: `curl -X DELETE 'localhost:5000/movies/50' -H 'Authorization: Bearer <YOUR_JSON_WEB_TOKEN>`

``` {
  "deleted": 50,
  "success": true
}
```

## Testing
To run the tests update the ASSISTANT_TOKEN, DIRECTOR_TOKEN and PRODUCER_TOKEN variables present in the `setup.sh` file with newly generated tokens.

In the project directory run:

```bash
source setup.sh
```

and then
```bash
python test_app.py
```
