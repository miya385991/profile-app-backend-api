from sqlalchemy import Column, Integer, String, DateTime, Text, LargeBinary
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from database import Base
import datetime


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())


class Profiles(Base):
    __tablename__ = "profiles"
    id = Column(Integer,  autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id',
                                         onupdate='CASCADE',
                                         ondelete='CASCADE'))
    location = Column(String(200))
    short_intro = Column(String(200))
    bio = Column(Text)
    # profile_image = Column(LargeBinary)
    github = Column(String(200))
    twitter = Column(String(200))
    youtube = Column(String(200))
    website = Column(String(200))
    created = Column(DateTime(timezone=True), server_default=func.now())


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    owner = Column(Integer, ForeignKey("users.id",
                                       onupdate='CASCADE',
                                       ondelete="CASCADE"))
    title = String(200)
    description = Column(Text)
    featured_image = Column(LargeBinary)
    demo_link = Column(String(2000))
    source_link = Column(String(2000))
    vote_total = Column(Integer)
    vote_ratio = Column(Integer)
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)