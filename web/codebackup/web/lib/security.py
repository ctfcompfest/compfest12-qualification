import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class EncryptDecrypt:
    def __init__(self, keyName):
        fileKey = open(keyName, 'rb')
        keyPair = RSA.importKey(fileKey.read())
        self.encryptor = PKCS1_OAEP.new(keyPair.publickey())
        self.decryptor = PKCS1_OAEP.new(keyPair)

    def encrypt(self, msg):
        return self.encryptor.encrypt(msg.encode()).hex()

    def decrypt(self, msg):
        return self.decryptor.decrypt(bytes.fromhex(msg)).decode('ascii')

def sanitize_content(s):
    blacklist = {
        "\"": "\u201D",
        "\'": "\u2019"
    }
    ret = [blacklist.get(c, c) for c in s]
    return ''.join(ret)

def check_path(s):
    blacklist = ['proc']
    for b in blacklist:
        if b in s:
            raise PermissionError()