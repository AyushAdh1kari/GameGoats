from mysql.connector import Error
from flask import Blueprint, jsonify, request

from backend.db_connection import get_db

games_routes = Blueprint("games_routes", __name__)


def _request_data():
    return request.get_json(silent=True) or {}


def _missing_fields(data, required_fields):
    return [field for field in required_fields if field not in data]


# Endpoints for listing and retrieving games. 
@games_routes.route("/games", methods=["GET"])
def get_games():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT g.*, s.studio_name AS published_by_studio_name
               FROM games AS g
               LEFT JOIN studios AS s ON g.published_by_studio_id = s.studio_id
               ORDER BY g.title, g.platform"""
        )
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()

# Endpoints for creating, updating, and deleting games. Normally requires RBAC but not a part of project.
@games_routes.route("/games", methods=["POST"])
def create_game():
    data = _request_data()
    required_fields = ("title", "description", "genre", "platform", "release_year")
    missing_fields = _missing_fields(data, required_fields)
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO games
               (title, description, genre, platform, release_year,
                average_rating, lifecycle_status, published_by_studio_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                data["title"],
                data["description"],
                data["genre"],
                data["platform"],
                data["release_year"],
                data.get("average_rating", 0.00),
                data.get("lifecycle_status", "active"),
                data.get("published_by_studio_id"),
            ),
        )
        db.commit()
        return jsonify({"game_id": cursor.lastrowid}), 201
    except Error as exc:
        db.rollback()
        return jsonify({"error": str(exc)}), 400
    finally:
        cursor.close()


# Endpoints for updating and deleting games. Normally requires RBAC but not a part of project.
@games_routes.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT g.*, s.studio_name AS published_by_studio_name
               FROM games AS g
               LEFT JOIN studios AS s ON g.published_by_studio_id = s.studio_id
               WHERE g.game_id = %s""",
            (game_id,),
        )
        game = cursor.fetchone()
        if not game:
            return jsonify({"error": "Game not found"}), 404
        return jsonify(game), 200
    finally:
        cursor.close()

# Endpoints for updating and deleting games. Normally requires RBAC but not a part of project.
@games_routes.route("/games/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    data = _request_data()
    db = get_db()
    cursor = db.cursor()

    allowed_fields = (
        "title",
        "description",
        "genre",
        "platform",
        "release_year",
        "average_rating",
        "lifecycle_status",
        "published_by_studio_id",
    )

    try:
        fields = []
        values = []
        for column in allowed_fields:
            if column in data:
                fields.append(f"{column} = %s")
                values.append(data[column])

        if not fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(game_id)
        cursor.execute(
            f"UPDATE games SET {', '.join(fields)} WHERE game_id = %s",
            values,
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Game not found"}), 404
        return jsonify({"message": "Game updated"}), 200
    except Error as exc:
        db.rollback()
        return jsonify({"error": str(exc)}), 400
    finally:
        cursor.close()


# Endpoints for updating and deleting games. Normally requires RBAC but not a part of project.
@games_routes.route("/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM games WHERE game_id = %s", (game_id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Game not found"}), 404
        return jsonify({"message": "Game deleted"}), 200
    finally:
        cursor.close()
