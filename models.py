from sqlalchemy import Column, Integer, String
from database import Base

# table: status
# fields: id - player - score

class Status(Base):
    __tablename__ = "status"
    
    id = Column(Integer, primary_key=True, index=True)
    player = Column(String)
    score = Column(Integer)
