import base64
import bcrypt


class HashService:

    @classmethod
    def hash(cls, password: str):
        salt = bcrypt.gensalt()
        hashpw = bcrypt.hashpw(password.encode("utf-8"), salt)
        hash_base64 = base64.b64encode(hashpw).decode("utf-8")
        return hash_base64
