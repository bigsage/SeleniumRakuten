import Crypto.Cipher.AES as AES


class Encrypt:
    key = b'grak45l312o67rj4'
    iv = b'2456564345643447'
    mode = AES.MODE_CFB
    encoding = 'ascii'

    @classmethod
    def encrypt(cls, text: str) -> bytes:
        aes = AES.new(cls.key, cls.mode, cls.iv)
        return aes.encrypt(text.encode(cls.encoding))

    @classmethod
    def decrypt(cls, text: bytes) -> str:
        aes = AES.new(cls.key, cls.mode, cls.iv)
        return aes.decrypt(text).decode(cls.encoding)
