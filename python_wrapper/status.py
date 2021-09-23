from enum import Enum


class Status(Enum):
    MOVIE_SEEN = 101
    ALL_MOVIES_SEEN_BY_BOT = 201
    MOVIE_NOT_SEEN = 102
    ALL_MOVIES_NOT_SEEN_BY_BOT = 202
