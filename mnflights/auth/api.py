def encrypt(key, contents):
    from .models import AESCipher, EncryptionKey
    aes = AESCipher(EncryptionKey.get_or_create(key))
    return aes.encrypt(contents)


def decrypt(key, contents):
    from .models import AESCipher, EncryptionKey
    aes = AESCipher(EncryptionKey.get_or_create(key))
    return aes.decrypt(contents)


def obfuscate(contents):
    from hashlib import sha512
    for i in xrange(63227):
        contents = sha512(contents).hexdigest()
    return contents
