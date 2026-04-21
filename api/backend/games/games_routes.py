from flask import Blueprint, make_response, current_app, jsonify

from backend.db_connection import get_db

games_routes = Blueprint("games_routes", __name__)

# cursor = get_db().cursor(dictionary = TRUE)

@games_routes.route("/games", methods=["GET"])
def get_all_games():
	cursor = get_db().cursor(dictionary = True)
	the_query = """
	SELECT * FROM games
	"""
	cursor.execute(the_query)
	the_data = cursor.fetchall()
	the_response = make_response(the_data)
	return the_response

@games_routes.route("/games/<id>", methods=["GET"])
def get_game(id):
	cursor = get_db().cursor(dictionary = True)
	cursor.execute('SELECT * FROM games WHERE game_id = {0}'.format(id))
	the_data = cursor.fetchall()
	the_response = make_response(the_data)
	return the_response

@games_routes.route("/games/<id>/tags", methods=["GET"])
def get_tags_by_game(id):
	cursor = get_db().cursor(dictionary = True)
	cursor.execute('SELECT tag_name FROM tags WHERE tag_id IN (SELECT tag_id FROM game_tags WHERE game_id = {0})'.format(id))
	the_data = cursor.fetchall()
	the_response = make_response(the_data)
	return the_response


