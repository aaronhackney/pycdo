from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto import Random
import base64


class EncryptCredentials:
    @staticmethod
    def encrypt(clear_text: str, public_key: str) -> str:
        """Takes a clear text str and RSA public key and returns an encrypted byte string that's been base64 encoded

        Args:
            clear_text (str): string that we wish to encrypt
            public_key (str): RSA Public key that we will use to encrypt the clear_text

        Returns:
            string: base64 encoded string of the encrypted clear_text data
        """
        key = RSA.importKey(base64.b64decode(public_key).decode("utf-8"))
        encryptor = PKCS1_v1_5.new(key)
        return base64.b64encode(encryptor.encrypt(clear_text.encode(encoding="UTF-8"))).decode()
