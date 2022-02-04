import flask
from flask import request, jsonify
import pandas as pd
from decouple import config
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, String, Numeric, DateTime
from sqlalchemy.exc import IntegrityError

app = flask.Flask(__name__)
app.config["DEBUG"] = True

Base = declarative_base()

class Player(Base):
    __tablename__ = 'player_profiles'
    player_name = Column(String(100), primary_key=True)
    description = Column(String(350))
    win_count = Column(Numeric)
    date_added = Column(DateTime)


def get_db_engine():
    user = config('user',default='')
    pw = config('pw',default='')
    db_server = config('server',default='')
    return create_engine('mysql+pymysql://' + user + ':' + pw + db_server + '/dartboard')

@app.route('/api/v1/resources/players/all', methods=['GET'])
# GET :: Returns all records in
def get_existing_players():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    dart_session = Session()
    for player in dart_session.query(Player):
        player_df = pd.read_sql(dart_session.query(Player).statement,dart_session.bind)
        return jsonify(player_df.to_dict(orient='records'))

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    # for runnning locally:
    app.run(host='localhost', port=8080, debug=True)
