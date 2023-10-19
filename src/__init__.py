"""
This module contains the main entry point for the APDI application.
"""

import os
import logging

from typing import Callable

import flask

from src import exceptions
from src import services
from src import objects
from src import db


logger = logging.getLogger("APDI")

__app__ = "APDI"
__version__ = "v1"

def _route_app(app: flask.Flask) -> tuple[Callable]:
    endpoint = f"/api/{__version__}"

    @app.before_request
    def before_request() -> None:
        user_token = flask.request.headers.get("AuthToken")
        flask.request.user_token = user_token
        flask.request.json_ = flask.request.get_json(silent=True) or {}

    @app.errorhandler(500)
    def handle_server_error(error: Exception) -> flask.Response:
        logger.exception(error)
        return flask.jsonify({
            "error": str(error)
            }), 500

    @app.errorhandler(exceptions.adiauth.UserNotExists)
    def handle_user_not_exists(error: Exception) -> flask.Response:
        return flask.jsonify({
            "error": str(error)
            }), 401

    @app.errorhandler(exceptions.BlobNotFoundError)
    def handle_blob_not_found(error: Exception) -> flask.Response:
        return flask.jsonify({
            "error": str(error)
            }), 404

    @app.route("/", methods=["GET"])
    @app.route(f"{endpoint}/status/", methods=["GET"])
    def get_status() -> flask.Response:
        return {
            "message": f"API {__app__} {__version__} up and running"
        }

    @app.route(f"{endpoint}/blobs/<blob>", methods=["GET"])
    def get_blob(blob: str) -> flask.Response:
        blob_ = services.get_blob(blob, flask.request.user_token)

        return flask.send_file(blob_, mimetype="application/octet-stream")

    @app.route(f"{endpoint}/blobs/", methods=["GET"])
    def get_blobs() -> flask.Response:
        blob_ids = services.get_user_blobs(flask.request.user_token)

        res = [
            {
                "blobId": id,
                "accessUrl": f"{endpoint}/blobs/{id}"
            }
            for id in blob_ids
        ]

        return {
            "blobs": res
        }

    @app.route(f"{endpoint}/blobs/", methods=["POST"])
    def post_blob() -> flask.Response:
        _v = flask.request.json_.get('visibility', objects.Visibility.PRIVATE)

        visibility = objects.Visibility(_v)

        blob_ = services.create_blob(flask.request.user_token, visibility)

        return {
            "blobId": blob_.id_,
            "accessUrl": f"{endpoint}/blobs/{blob_.id_}"
        }, 201

    @app.route(f"{endpoint}/blobs/<blob>", methods=["PUT"])
    def put_blob(blob: str) -> flask.Response:
        services.update_blob(blob, flask.request.user_token, flask.request.stream)

        return "", 204

    @app.route(f"{endpoint}/blobs/<blob>", methods=["DELETE"])
    def delete_blob(blob: str) -> flask.Response:
        services.delete_blob(blob, flask.request.user_token)

        return "", 204

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

    @app.route(f"{endpoint}/blobs/<blob>/hash", methods=["GET"])
    def get_blob_hashes(blob: str) -> flask.Response:
        hash_type = flask.request.args.get("type", "md5")

        hash_list = hash_type.split(",")

        try:
            _hashes = services.get_hash_blob(blob, flask.request.user_token, hash_list)
        except ValueError as e:
            return {
                "error": str(e)
            }, 400

        return _hashes

    return (
        before_request,
        get_status,
        get_blob,
        get_blobs,
        post_blob,
        put_blob,
        delete_blob,
        post_blob_permission,
        delete_blob_permission,
        get_blob_hashes,

        handle_blob_not_found,
        handle_user_not_exists,
        handle_server_error)

def main(
        port=3002,
        host="0.0.0.0",
        db_path="pyblob.db",
        storage="storage",
        auth_api="http://localhost:3001") -> None:
    """
    Creates a DB connection and runs the Flask app.
    """

    os.environ["STORAGE"] = storage
    os.environ["AUTH_API"] = auth_api

    #if not entities.Client.check_connection():
    #    raise RuntimeError(f"Could not connect to {auth_api}")

    with db.connect(db_path):
        app = flask.Flask(__app__)

        _route_app(app)

        app.run(
            host=host,
            port=port)
