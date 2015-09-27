import base64
import hashlib
import random
import string

from Crypto import Random
from Crypto.Cipher import AES
from google.appengine.ext import ndb

from .api import obfuscate


class EncryptionKey(ndb.Model):
    _use_cache = False
    value = ndb.StringProperty(indexed=False)

    @classmethod
    def get_or_create(cls, key):
        encryption_key = cls.get_by_id(key)
        if not encryption_key:
            choices = string.letters[:52] + string.digits
            rand_gen = random.SystemRandom(random.random())
            pwd = ''.join(rand_gen.choice(choices) for _ in xrange(256))
            encryption_key = cls(id=key, value=pwd)
            encryption_key.put()
        return encryption_key.value


class User(ndb.Model):
    _use_cache = False
    name = ndb.StringProperty(indexed=False)
    password_hash = ndb.StringProperty(indexed=False, default='')

    @classmethod
    def create(cls, name, password):
        return cls(id=name, name=name, password_hash=obfuscate(password)).put()


class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(
            cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return (
            s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
