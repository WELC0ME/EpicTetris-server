from flask import Flask, make_response, jsonify, request
import datetime
from db import db_session
from db.user import User

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
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(
        User.nickname == request.json['nickname']
    ).first()
    if user:
        return jsonify({
            'result': 'Nickname is already exists'
        })
    user = User()
    user.nickname = request.json['nickname']
    user.created = str(datetime.datetime.now()).split(' ')[0]
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({
        'result': 'OK',
        'user': user.to_dict(only=(
            'nickname',
            'rating',
            'best',
            'created'
        )),
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
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.nickname == nickname).first()
    if not user:
        return jsonify({
            'result': 'Not found'
        })
    if not user.check_password(request.json['password']):
        return jsonify({
            'result': 'Incorrect password'
        })
    return jsonify({
        'result': 'OK',
        'user': user.to_dict(only=(
            'nickname',
            'rating',
            'best',
            'created'
        )),
    })


@app.route('/api/users/', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify({
        'users': [user.to_dict(only=(
            'nickname',
            'rating',
            'best',
            'created'
        )) for user in users],
    })


@app.route('/api/users/<nickname>', methods=['PUT'])
def edit_user(nickname):
    if not request.json:
        return jsonify({
            'result': 'Empty request'
        })
    elif not all(key in request.json for key in [
        'game_result',
    ]):
        return jsonify({
            'result': 'Bad request'
        })
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.nickname == nickname).first()
    if not user:
        return jsonify({
            'result': 'Not found'
        })
    user.rating += int(request.json['game_result'])
    user.best = max(user.best, int(request.json['game_result']))
    db_sess.merge(user)
    db_sess.commit()
    return jsonify({
        'result': 'OK'
    })


@app.route('/api/users/', methods=['DELETE'])
def clear():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    for user in users:
        db_sess.delete(user)
        db_sess.commit()
    return jsonify({
        'result': 'OK'
    })


if __name__ == '__main__':
    app.run()
