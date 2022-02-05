from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Numeric, DateTime

Base = declarative_base()

class Players(Base):
    __tablename__ = 'player_profiles'
    player_name = Column(String(100), primary_key=True)
    description = Column(String(350))
    win_count = Column(Numeric)
    date_added = Column(DateTime)
