from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from database import Base

import secrets
import string


# ランダムな文字列
def get_random_password_string(length):
    pass_chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(pass_chars) for x in range(length))
    return password


class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    demo_link = Column(String(2000))
    source_link = Column(String(2000))
    image_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id',
                                         onupdate='CASCADE',
                                         ondelete='CASCADE'),
                     nullable=False)
    user = relationship("Users", back_populates="project_users")

    created = Column(DateTime(timezone=True), server_default=func.now())


class Skills(Base):
    __tablename__ = "skills"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id',
                                         onupdate='CASCADE',
                                         ondelete='CASCADE'), nullable=False)
    user = relationship("Users", back_populates="skill_users")

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hash_password = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())

    project_users = relationship("Projects", back_populates="user")
    profile_users = relationship("Profiles", back_populates="user")
    media_users = relationship('Medias', back_populates="user")
    skill_users = relationship('Skills', back_populates="user")


class Profiles(Base):
    __tablename__ = "profiles"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id',
                                         onupdate='CASCADE',
                                         ondelete='CASCADE'), nullable=False)
    user = relationship("Users", back_populates="profile_users")

    nick_name = Column(String, nullable=False)
    short_intro = Column(String(200))
    bio = Column(Text)
    location = Column(String(200))
    image_url = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())


class Medias(Base):
    __tablename__ = "medias"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id',
                                         onupdate='CASCADE',
                                         ondelete='CASCADE'), nullable=False)
    user = relationship("Users", back_populates="media_users")
