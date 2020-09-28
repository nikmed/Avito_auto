import os
import sys

import pytest

import shorturly

sys.path.append(os.getcwd()[0:os.getcwd().rfind('/')] + '/shorturly')


@pytest.fixture
def client():
    test_dbname = 'test_database.db'
    with shorturly.app.test_client() as client:
        shorturly.init_db(test_dbname)
        yield client
    os.remove(test_dbname)


def test_empty(client):
    rv = client.get('/')
    assert rv.status_code == 200


def test_url(client):
    rv = client.post('/', data={'URL': 'https://start.avito.ru/tech'})
    assert rv.status_code == 200
    rv1 = client.get('/1')
    assert rv1.status_code == 302
    assert b'a href = 1' in rv.data
    assert rv1.location == 'https://start.avito.ru/tech'


def test_custom_url(client):
    rv = client.post('/', data={'URL': 'https://start.avito.ru/tech', 'short_url': 'avito-tech'})
    rv1 = client.get('/avito-tech')
    assert rv.status_code == 200
    assert b'a href = avito-tech' in rv.data
    assert rv1.status_code == 302
    assert rv1.location == 'https://start.avito.ru/tech'
    rv2 = client.post('/', data={'URL': 'https://start.avito.ru/tech', 'short_url': 'avito-tech'})
    assert rv2.status_code == 400


def test_wrong_shortid(client):
    rv = client.get('/2')
    assert rv.status_code == 400
    assert b'Page not found' in rv.data


def test_many_urls(client):
    rv = client.post('/', data={'URL': 'https://start.avito.ru/tech'})
    assert rv.status_code == 200
    rv1 = client.get('/1')
    assert rv1.status_code == 302
    assert b'a href = 1' in rv.data
    assert rv1.location == 'https://start.avito.ru/tech'
    rv = client.post('/', data={'URL': 'https://start.avito.ru/tech', 'short_url': 'avito-tech'})
    rv1 = client.get('/avito-tech')
    assert rv.status_code == 200
    assert b'a href = avito-tech' in rv.data
    assert rv1.status_code == 302
    assert rv1.location == 'https://start.avito.ru/tech'
    rv2 = client.post('/', data={'URL': 'https://start.avito.ru/tech', 'short_url': 'avito-tech'})
    assert rv2.status_code == 400
    rv = client.post('/', data={'URL': 'https://vk.com', 'short_url': 'vk'})
    rv1 = client.get('/vk')
    assert rv.status_code == 200
    assert b'a href = vk' in rv.data
    assert rv1.location == 'https://vk.com'
