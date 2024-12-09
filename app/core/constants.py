from enum import Enum


class UserRolesEnum(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
