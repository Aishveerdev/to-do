# databasse models will be defined here
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from services.database import Base


# this "base" is the "declarative_base" that we created in database.py and it will allow us to create our database models
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer , ForeignKey("users.id"))  # CORE!!!


