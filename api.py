import flask
from flask import jsonify, request
import datetime
from db import db_session
from db.user import User

blueprint = flask.Blueprint(
    'users_api',
    __name__
)


@blueprint.route('/api/users', methods=['POST'])
def create_user():
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
    user.created = str(datetime.datetime.now()).split('.')[0]
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({
        'result': 'OK',
    })


@blueprint.route('/api/users/<nickname>', methods=['GET'])
def login(nickname):
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
    })


@blueprint.route('/api/users/', methods=['GET'])
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


@blueprint.route('/api/users/<nickname>', methods=['PUT'])
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
    db_sess.commit()
    return jsonify({
        'result': 'OK'
    })


@blueprint.route('/api/users/', methods=['DELETE'])
def clear():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    for user in users:
        db_sess.delete(user)
        db_sess.commit()
    return jsonify({
        'result': 'OK'
    })
