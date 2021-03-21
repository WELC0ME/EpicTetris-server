from requests import get, post, put, delete
import logging
from threading import Thread
import time
from flask import Flask
from db import db_session
import api


def run_tests():
    time.sleep(1)
    server = 'http://127.0.0.1:8080/api/users'

    print('Create user')
    print(post(server, json={
        'nickname': 'TEST_01',
        'password': '12345'
    }).json())
    print(get(server).json())

    print('Create user with same nickname')
    print(post(server, json={
        'nickname': 'TEST_01',
        'password': '54321'
    }).json())
    print(get(server).json())

    print('Login with incorrect password')
    print(get(server + '/TEST_01', json={
        'password': '54321'
    }).json())

    print('Login with correct password')
    print(get(server + '/TEST_01', json={
        'password': '12345'
    }).json())

    print('Add game result')
    print(put(server + '/TEST_01', json={
        'game_result': '10'
    }).json())
    print(get(server).json())

    print('Add game result for non-existent user')
    print(put(server + '/TEST_02', json={
        'game_result': '10'
    }).json())
    print(get(server).json())

    print('Add another game result')
    print(put(server + '/TEST_01', json={
        'game_result': '10'
    }).json())
    print(get(server).json())

    print('Delete all users')
    print(delete(server).json())
    print(get(server).json())


if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '72697676798779827668'
    app.register_blueprint(api.blueprint)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    db_session.global_init("db/tetris.db")
    Thread(target=run_tests).start()
    app.run(host='127.0.0.1', port=8080)
