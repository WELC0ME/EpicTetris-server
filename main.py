from flask import Flask, make_response, jsonify
from db import db_session
import api

app = Flask(__name__)
app.config['SECRET_KEY'] = '72697676798779827668'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'result': 'Not found',
        'error': error,
    }), 404)


if __name__ == '__main__':
    db_session.global_init("db/tetris.db")
    app.register_blueprint(api.blueprint)
    app.run()
