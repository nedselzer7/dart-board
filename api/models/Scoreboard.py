from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Numeric, DateTime

Base = declarative_base()

class Scoreboard(Base):
    __tablename__ = 'current_cricket_game'
    game_id = Column(String(10))
    player_name = Column(String(100), primary_key=True)
    count_12 = Column(Numeric)
    count_13 = Column(Numeric)
    count_14 = Column(Numeric)
    count_15 = Column(Numeric)
    count_16 = Column(Numeric)
    count_17 = Column(Numeric)
    count_18 = Column(Numeric)
    count_19 = Column(Numeric)
    count_20 = Column(Numeric)
    count_B = Column(Numeric)
