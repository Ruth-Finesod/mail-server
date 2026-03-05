from hashlib import blake2b
from hmac import compare_digest


class CookieHandler:
    SECRET_KEY = b'bzbAAQQEor8AaEEkCav5i0as'
    AUTH_SIZE = 16

    @classmethod
    def sign(cls, cookie: str) -> str:
        """
        signs a string using blake2b encryption and a secret key
        :param cookie: the given string to sign
        :return: a string of the signed cookie
        """
        h = blake2b(digest_size=cls.AUTH_SIZE, key=cls.SECRET_KEY)
        h.update(bytes(cookie, "utf-8"))
        return h.hexdigest()

    @classmethod
    def verify(cls, cookie, sig) -> bool:
        """
        signs the cookie using cls.sign and compares it to the sig
        :param cookie: the given string unsigned
        :param sig: the given signed string
        :return: True if the same, else otherwise
        """
        good_sig = cls.sign(cookie)
        return compare_digest(good_sig, sig)
