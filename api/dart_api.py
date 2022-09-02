import flask
from flask import request, jsonify
import pandas as pd
from decouple import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from models.Players import Players
from models.Scoreboard import Scoreboard

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_db_session():
    user = config('user',default='')
    pw = config('pw',default='')
    db_server = config('server',default='')
    engine = create_engine('mysql+pymysql://' + user + ':' + pw + db_server + '/dartboard')
    Session = sessionmaker(bind=engine)
    return Session()

@app.route('/api/v1/resources/players/all_players', methods=['GET'])
# GET :: Returns all players in player_profiles
def get_existing_players():
    dart_session = get_db_session()
    return jsonify([player.player_name for player in dart_session.query(Players)])

@app.route('/api/v1/resources/players/new_player', methods=['POST'])
# POST :: Takes new player data and adds to player_profiles table
def create_player():
    dart_session = get_db_session()
    new_player_df = pd.DataFrame(request.json, index=[0])
    try:
        new_player = Players(
            player_name = new_player_df['player_name'][0],
            description = new_player_df['description'][0],
            win_count = new_player_df['win_count'][0]
        )
        dart_session.add(new_player)
        dart_session.commit()
        return "<h1>Success:</h1><p>New Player " + str(new_player_df['player_name'][0]) + " created.</p>"
    # Catch Integrity Error for duplicate player name
    except IntegrityError as e:
        print('Player with given name already exists')
        return "<h1>Error:</h1><p>Player with name " + str(new_player_df['player_name'][0]) + " already exists.</p>"

@app.route('/api/v1/resources/scoreboard/current_score', methods=['GET'])
# GET :: Takes player name and returns Player's current score
def get_current_score():
    if 'player_name' and 'game_id' in request.args:
        player_name = str(request.args['player_name'])
        game_id = str(request.args['game_id'])
    else:
        return "<h1>Error:</h1><p>No Player ID provided. Please specify a Player ID.</p>"

    dart_session = get_db_session()
    score_df = pd.read_sql(dart_session.query(Scoreboard).filter(Scoreboard.player_name==player_name && Scoreboard.game_id==game_id).statement,dart_session.bind)
    return jsonify(score_df.to_dict(orient='records'))

@app.route('/api/v1/resources/scoreboard/update_score', methods=['PUT'])
# PUT :: Takes current round score and updates player's current game scores
def update_score():
    dart_session = get_db_session()
    new_scores = pd.DataFrame(request.json, index=[0])
    player = new_scores['player_name'][0]
    game_id = new_scores['game_id'][0]
    current_score_df = pd.read_sql(dart_session.query(Scoreboard).filter(Scoreboard.player_name==player).statement,dart_session.bind)

    if not current_score_df.empty:
        # Try to update for existing player
        print('Found scoreboard for player ' + str(player) + '.')
        current_score_df = pd.read_sql(dart_session.query(Scoreboard).filter(Scoreboard.player_name==player).statement,dart_session.bind)
        scoreboard = dart_session.query(Scoreboard).filter(Scoreboard.player_name==player).update({
                Scoreboard.count_12: int(current_score_df['count_12'][0]) + int(new_scores['count_12'][0]),
                Scoreboard.count_13: int(current_score_df['count_13'][0]) + int(new_scores['count_13'][0]),
                Scoreboard.count_14: int(current_score_df['count_14'][0]) + int(new_scores['count_14'][0]),
                Scoreboard.count_15: int(current_score_df['count_15'][0]) + int(new_scores['count_15'][0]),
                Scoreboard.count_16: int(current_score_df['count_16'][0]) + int(new_scores['count_16'][0]),
                Scoreboard.count_17: int(current_score_df['count_17'][0]) + int(new_scores['count_17'][0]),
                Scoreboard.count_18: int(current_score_df['count_18'][0]) + int(new_scores['count_18'][0]),
                Scoreboard.count_19: int(current_score_df['count_19'][0]) + int(new_scores['count_19'][0]),
                Scoreboard.count_20: int(current_score_df['count_20'][0]) + int(new_scores['count_20'][0]),
                Scoreboard.count_B: int(current_score_df['count_B'][0]) + int(new_scores['count_B'][0])
        })
        dart_session.commit()
        print('Updated scoreboard for ' + str(player) + '.')
        return "<h1>Success:</h1><p>Current Scoreboard for player " + str(player) + " has been updated.</p>"
    else:
        print('No player with name ' + str(player) + ' found. Creating new entry.')
        # If player has not yet submitted any score
        new_scoreboard = Scoreboard(
            game_id = game_id,
            player_name = player,
            count_12 = int(new_scores['count_12'][0]),
            count_13 = int(new_scores['count_13'][0]),
            count_14 = int(new_scores['count_14'][0]),
            count_15 = int(new_scores['count_15'][0]),
            count_16 = int(new_scores['count_16'][0]),
            count_17 = int(new_scores['count_17'][0]),
            count_18 = int(new_scores['count_18'][0]),
            count_19 = int(new_scores['count_19'][0]),
            count_20 = int(new_scores['count_20'][0]),
            count_B = int(new_scores['count_B'][0])
        )
        dart_session.add(new_scoreboard)
        dart_session.commit()
        return "<h1>Success:</h1><p>New Scoreboard created for player " + str(player) + ".</p>"

@app.route('/api/v1/resources/scoreboard/get_cricket_winner', methods=['GET'])
# GET :: Checks if the player has won the game - to be called after submitting current scores
def get_cricket_winner():
    if 'player_name' and 'game_id' in request.args:
        player_name = str(request.args['player_name'])
        game_id = str(request.args['game_id'])
    else:
        return "<h1>Error:</h1><p>No Player ID provided. Please specify a Player ID.</p>"

    dart_session = get_db_session()
    score_df = pd.read_sql(dart_session.query(Scoreboard).filter(Scoreboard.player_name==player_name && Scoreboard.game_id==game_id).statement,dart_session.bind)

    if int(score_df['count_12'][0]) == int(score_df['count_13'][0]) == int(score_df['count_14'][0]) == int(score_df['count_15'][0]) == int(score_df['count_16'][0]) == int(score_df['count_17'][0]) == int(score_df['count_18'][0]) ==  int(score_df['count_19'][0]) == int(score_df['count_20'][0]) == int(score_df['count_B'][0]) == 3:
        return True
    else:
        return False

@app.route('/api/v1/resources/scoreboard/current_game', methods=['GET'])
# GET :: Get current game scoreboard
def get_current_game():
    



if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    # for runnning locally:
    app.run(host='localhost', port=8080, debug=True)
    # app.run(host=127.0.0.1, port=8080, debug=True)
