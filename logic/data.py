import hashlib
import os


def hash_password(password):
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + pwd_hash


def verify_password(stored_password, provided_password):
    salt = stored_password[:16]
    pwd_hash = stored_password[16:]
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return pwd_hash == new_hash


class Role:
    def __init__(self, role='admin', password=''):
        self._role = role
        self._password = password

    def set_role(self, role):
        self._role = role

    def set_password(self, password):
        self._password = hash_password(password)

    def get_hashed_password(self):
        return hash_password(self._password)

    def get_hashed_login(self):
        return hash_password(self._role)

    def get_role(self):
        return 'admin'

    def get_password(self):
        return '1234'
