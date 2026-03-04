from hashlib import blake2b
from hmac import compare_digest


class CookieHandler:
    SECRET_KEY = b'bzbAAQQEor8AaEEkCav5i0as'
    AUTH_SIZE = 16

    @classmethod
    def sign(cls, cookie) -> str:
        h = blake2b(digest_size=cls.AUTH_SIZE, key=cls.SECRET_KEY)
        h.update(bytes(cookie, "utf-8"))
        return h.hexdigest()

    @classmethod
    def verify(cls, cookie, sig) -> bool:
        good_sig = cls.sign(cookie)
        return compare_digest(good_sig, sig)
