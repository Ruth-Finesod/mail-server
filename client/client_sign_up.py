from typing import Dict


def client_sign_up() -> Dict[str: str]:
    username = input('email address: ')
    password = input('password: ')
    hashed_password = hash(password)


def password_validation(password: str) -> bool:
    valid = True
    if len(password) < 8:
        print('password must be at least 8 characters')
        valid = False
