from flask import Flask, make_response, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from database import DataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = '72697676798779827668'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'result': 'Not found',
        'error': error,
    }), 404)


@app.route('/api/users', methods=['POST'])
def sign_up():
    if not request.json:
        return jsonify({
            'result': 'Empty request'
        })
    elif not all(key in request.json for key in [
        'nickname',
        'password',
    ]):
        return jsonify({
            'result': 'Bad request'
        })
    database = DataBase()
    res = database.execute('SELECT * FROM users')
    ids = [i[0] for i in res]
    id_ = max(ids) + 1 if len(ids) > 0 else 0
    if id_ >= 10000:
        return jsonify({
            'result': 'Too many users',
        })
    users = [eval(i[1]) for i in res]
    if any([user['nickname'] == request.json['nickname'] for user in users]):
        return jsonify({
            'result': 'Nickname is already exists'
        })
    user = {
        'nickname': request.json['nickname'],
        'password': generate_password_hash(request.json['password']),
        'rating': 0,
        'best': 0,
        'created': str(datetime.datetime.now()).split(' ')[0],
    }
    database.execute("INSERT INTO users VALUES (%s, %s)",
                     (id_, str(user)))

    return jsonify({
        'result': 'OK',
        'user': user,
    })


@app.route('/api/users/<nickname>', methods=['GET'])
def sign_in(nickname):
    if not request.json:
        return jsonify({
            'result': 'Empty request'
        })
    elif not all(key in request.json for key in [
        'password',
    ]):
        return jsonify({
            'result': 'Bad request'
        })

    database = DataBase()
    users = [eval(i[0]) for i in database.execute('SELECT data FROM users')]
    for user in users:
        if user['nickname'] == nickname:
            if not check_password_hash(user['password'],
                                       request.json['password']):
                return jsonify({
                    'result': 'Incorrect password'
                })
            return jsonify({
                'result': 'OK',
                'user': user,
            })
    return jsonify({
        'result': 'Not found'
    })


@app.route('/api/users/', methods=['GET'])
def get_users():
    database = DataBase()
    users = []
    for i in database.execute('SELECT data FROM users'):
        user = eval(i[0])
        del user['password']
        users.append(user)
    return jsonify({
        'users': users,
    })


@app.route('/api/users/<nickname>', methods=['PUT'])
def edit_user(nickname):
    if not request.json:
        return jsonify({
            'result': 'Empty request'
        })
    elif not all(key in request.json for key in [
        'game_result',
        'token',
    ]):
        return jsonify({
            'result': 'Bad request'
        })
    elif request.json['token'] != generate_token(
            nickname,
            request.json['game_result'],
    ):
        print(nickname)
        print(request.json['game_result'])
        print(request.json['token'])
        print(generate_token(nickname, request.json['game_result']))
        return jsonify({
            'result': 'Incorrect token'
        })
    database = DataBase()
    res = database.execute('SELECT * FROM users')
    ids = [i[0] for i in res]
    users = [eval(i[1]) for i in res]
    for i, user in enumerate(users):
        if user['nickname'] == nickname:
            user['rating'] += int(request.json['game_result'])
            user['best'] = max(user['best'], int(request.json['game_result']))
            database.execute("UPDATE users SET data = %s WHERE id = %s",
                             (str(user), ids[i]))
            return jsonify({
                'result': 'OK'
            })
    return jsonify({
        'result': 'Not found'
    })


def generate_token(username, result):
    numbers = [int(result)] + [32767 + ord(i) for i in str(username)]
    numbers = [(i >> 119) ^ 37 for i in numbers]
    numbers = generate_password_hash('_'.join([chr(i) for i in numbers]))
    return str(generate_password_hash(str(numbers)))


if __name__ == '__main__':
    app.run()
