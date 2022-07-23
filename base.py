from pydantic import BaseModel


class Users(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class Profiles(BaseModel):
    user_id: int
    location: str
    short_intro: str
    bio: str
    # profile_image: str
    github: str
    twitter: str
    youtube: str
    website: str


class Projects(BaseModel):
    owner: int
    title: str
    description: str
    featured_image: str
    demo_link: str
    source_link: str
    vote_total: int
    vote_ratio: int
