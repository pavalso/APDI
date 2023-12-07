#!/usr/bin/env python3

from flask import Flask


app = Flask(import_name=__name__)

@app.route('/v1/status', methods=['GET'])
def status():
    return '', 200

@app.route('/v1/<user>', methods=['GET'])
def get_user(user):
    if user == 'USER':
        return '', 204
    return '', 404

@app.route('/v1/token/<token>', methods=['GET'])
def get_token(token):
    if token == 'USER_TOKEN':
        return {'user': 'USER'}, 200
    return '', 404

app.run(debug=True)
