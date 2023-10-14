"""
This module contains the main entry point for the APDI application.
"""

import sys
import os

from typing import NoReturn, Callable

import flask

from src import exceptions
from src import services
from src import objects
from src import db


__version__ = "v1"

def _route_app(app: flask.Flask) -> tuple[Callable]:
    endpoint = f"/api/{__version__}"

    @app.before_request
    def before_request() -> None:
        user_token = flask.request.headers.get("Authorization")
        flask.request.user_token = user_token
        flask.request.get_json(cache=True, silent=True)

    @app.errorhandler(exceptions.BlobNotFoundError)
    @app.errorhandler(exceptions.adiauth.UserNotExists)
    def handle_not_found(error: Exception) -> flask.Response:
        return flask.jsonify({
            "error": str(error)
            }), 404

    @app.route(f"{endpoint}/blobs/<blob>", methods=["GET"])
    def get_blob(blob: str) -> flask.Response:
        blob_ = services.get_blob(blob, flask.request.user_token)

        return flask.send_file(blob_, mimetype="application/octet-stream")

    @app.route(f"{endpoint}/blobs/", methods=["GET"])
    def get_blobs() -> flask.Response:
        blobs = services.get_user_blobs(flask.request.user_token)

        return {
            "blobs": blobs,
            "message": f"Retrieved {len(blobs)} blobs successfully"
        }

    @app.route(f"{endpoint}/blobs/", methods=["POST"])
    def post_blob() -> flask.Response:
        visibility = objects.Visibility.PUBLIC#flask.request.get_json(silent=True).get('visibility', objects.Visibility.PRIVATE)

        blob_ = services.create_blob(flask.request.user_token, visibility)

        return {
            "id": blob_.id_,
            "message": "Blob created successfully"
        }

    @app.route(f"{endpoint}/blobs/<blob>", methods=["PUT"])
    def put_blob(blob: str) -> flask.Response:
        stream = flask.request.stream

        services.update_blob(blob, flask.request.user_token, stream)

        return {
            "message": f"Blob {blob} updated successfully"
        }

    @app.route(f"{endpoint}/blobs/<blob>", methods=["DELETE"])
    def delete_blob(blob: str) -> flask.Response:
        services.delete_blob(blob, flask.request.user_token)

        return {
            "message": f"Blob {blob} deleted successfully"
        }

    @app.route(f"{endpoint}/blobs/<blob>/permissions/<username>", methods=["POST"])
    def post_blob_permission(blob: str, username: str) -> flask.Response:
        try:
            services.add_read_permission(blob, flask.request.user_token, username)
        except exceptions.UserHavePermissionsError:
            return {
                "message": f"User {username} already has permissions for blob {blob}"
            }, 409

        return {
            "message": f"Permission added to user {username} successfully"
        }

    @app.route(f"{endpoint}/blobs/<blob>/permissions/<username>", methods=["DELETE"])
    def delete_blob_permission(blob: str, username: str) -> flask.Response:
        try:
            services.remove_read_permission(blob, flask.request.user_token, username)
        except exceptions.UserHaveNoPermissionsError:
            return {
                "message": f"User {username} has no permissions to remove for blob {blob}"
            }, 409

        return {
            "message": f"Permission removed from user {username} successfully"
        }

    @app.route(f"{endpoint}/blobs/<blob>/hashes", methods=["GET"])
    def get_blob_hashes(blob: str) -> flask.Response:
        _md5, _sha256 = services.get_hash_blob(blob, flask.request.user_token)

        return {
            "md5": _md5,
            "sha256": _sha256,
        }

    return (
        before_request,
        get_blob,
        get_blobs,
        post_blob,
        put_blob,
        delete_blob,
        post_blob_permission,
        delete_blob_permission,
        get_blob_hashes,

        handle_not_found)

def main(port=3002, host="0.0.0.0", db_path="pyblob.db", storage="storage", auth_api="http://localhost:3001") -> NoReturn:
    """
    Creates a DB connection and runs the Flask app.
    """

    os.environ["STORAGE"] = storage
    os.environ["AUTH_API"] = auth_api

    os.makedirs(storage, exist_ok=True)

    with db.connect(db_path):
        app = flask.Flask(__name__)

        _route_app(app)

        app.run(
            host=host,
            port=port,
            debug=True)

    sys.exit(0)
