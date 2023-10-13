"""
This module contains the main entry point for the APDI application.
"""

import sys

from typing import NoReturn, Callable

import flask

from src import exceptions
from src import services


__version__ = "v1"

def route_app(app: flask.Flask) -> tuple[Callable]:

    endpoint = f"/api/{__version__}"

    @app.before_request
    def before_request() -> None:
        user_token = flask.request.headers.get("Authorization")
        flask.request.user_token = user_token

    @app.route(f"{endpoint}/blobs/<blob>", methods=["GET"])
    def get_blob(blob: str) -> flask.Response:
        blob = services.get_blob(blob, flask.request.user_token)

        return flask.jsonify(blob)

    @app.route(f"{endpoint}/blobs/", methods=["GET"])
    def get_blobs() -> flask.Response:
        blobs = services.get_user_blobs(flask.request.user_token)

        return flask.jsonify(blobs)

    @app.route(f"{endpoint}/blobs/", methods=["POST"])
    def post_blob() -> flask.Response:
        blob = services.create_blob(flask.request.user_token)

        return flask.jsonify(blob)

    @app.route(f"{endpoint}/blobs/<blob>", methods=["PUT"])
    def put_blob(blob: str) -> flask.Response:
        blob = services.update_blob(blob, flask.request.user_token)

        return flask.jsonify(blob)

    @app.route(f"{endpoint}/blobs/<blob>", methods=["DELETE"])
    def delete_blob(blob: str) -> flask.Response:
        services.delete_blob(blob, flask.request.user_token)

        return flask.Response(status=204)

    @app.route(f"{endpoint}/blobs/<blob>/permissions/<username>", methods=["POST"])
    def post_blob_permission(blob: str, username: str) -> flask.Response:
        services.add_read_permission(blob, flask.request.user_token, username)

        return flask.Response(status=200)

    @app.route(f"{endpoint}/blobs/<blob>/permissions/<username>", methods=["DELETE"])
    def delete_blob_permission(blob: str, username: str) -> flask.Response:
        services.remove_read_permission(blob, flask.request.user_token, username)

        return flask.Response(status=200)

    @app.route(f"{endpoint}/blobs/<blob>/hashes", methods=["GET"])
    def get_blob_hashes(blob: str) -> flask.Response:
        hashes = services.get_hash_blob(blob, flask.request.user_token)

        return flask.jsonify(hashes)

    return (
        before_request,
        get_blob,
        get_blobs,
        post_blob,
        put_blob,
        delete_blob,
        post_blob_permission,
        delete_blob_permission,
        get_blob_hashes)

def main() -> NoReturn:
    app = flask.Flask(__name__)

    route_app(app)

    app.run(
        host="127.0.0.1",
        port=80,
        debug=True)

    sys.exit(0)
