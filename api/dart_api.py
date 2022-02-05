import flask
from flask import request, jsonify
import pandas as pd
from decouple import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from Players import Players
from Scoreboard import Scoreboard

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
    # Either return a list or a dict:
    # player_df = pd.read_sql(dart_session.query(Players.player_name).statement,dart_session.bind)
    # return jsonify(player_df.to_dict(orient='records'))
    return jsonify([player.player_name for player in dart_session.query(Players)])

@app.route('/api/v1/resources/players/new_player', methods=['POST'])
# POST :: Takes player name and returns current game scoring
def create_player():
    # Figure out how to send data to this POST method
    dart_session = get_db_session()
    try:
        print('INSERT new player profile')
    # Use Integrity Error here for duplicate player name
    except IntegrityError:
        print('Player with given name already exists')

@app.route('/api/v1/resources/players/current_game', methods=['GET'])
# GET :: Takes player name and returns current game scoring
def get_current_game():
    if 'player_name' in request.args:
        player_name = str(request.args['player_name'])
    else:
        return "<h1>Error:</h1><p>No Player ID provided. Please specify a Player ID.</p>"

    dart_session = get_db_session()
    score_df = pd.read_sql(dart_session.query(Scoreboard).filter(Scoreboard.player_name==player_name).statement,dart_session.bind)
    return jsonify(score_df.to_dict(orient='records'))

@app.route('/api/v1/resources/players/update_score', methods=['POST'])
# POST :: Takes player name and returns current game scoring
def update_score():
    dart_session = get_db_session()
    try:
        # Try to update for existin player
        print('Update current player\'s score')
    except:
        # If player has not yet submitted any score
        print('Create new row with player and submitted score')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    # for runnning locally:
    app.run(host='localhost', port=8080, debug=True)
