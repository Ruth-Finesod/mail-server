from hashlib import blake2b
from hmac import compare_digest


class CookieHandler:
    SECRET_KEY = b'bzbAAQQEor8AaEEkCav5i0as'
    AUTH_SIZE = 16

    @classmethod
    def sign(cls, cookie):
        h = blake2b(digest_size=cls.AUTH_SIZE, key=cls.SECRET_KEY)
        h.update(cookie)
        return h.hexdigest().encode('utf-8')

    @classmethod
    def verify(cls, cookie, sig):
        good_sig = cls.sign(cookie)
        return compare_digest(good_sig, sig)
