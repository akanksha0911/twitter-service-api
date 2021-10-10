import pytest
import json
from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_tweet_for_bad_id(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    res = client.post('/getTweet', data=json.dumps({"id": "test"}), headers=headers)
    assert res.status_code == 200


def test_delete_tweet_for_bad_id(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    res = client.post('/deleteTweet', data=json.dumps({"id": "test"}), headers=headers)
    assert res.status_code == 200
    assert """Sorry, that page does not exist","code":34""" in res.get_data(as_text=True)


def test_get_tweet_for_good_id(app, client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    res = client.post('/getTweet', data=json.dumps({"id": "1447082688746250244"}), headers=headers)
    assert res.status_code == 200
    assert """tsssss22ssssss22""" in res.get_data(as_text=True)


def test_failure_with_bad_route(app, client):
    res = client.get('/')
    assert res.status_code == 404
