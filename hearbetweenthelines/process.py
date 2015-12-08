"""
#Author: Eric Hennenfent
Compresses and encrypts the file passed to it.
"""

from Crypto.Cipher import AES
from Crypto.Hash import MD5
import zlib

def pad_to_sixteen(stir):
    out=stir
    while(len(out) % 16 != 0):
        out += 'i'
    return out

def compress_and_encrypt(input_string, key):
    hashed = MD5.new()
    hashed.update(key)
    compressed = zlib.compress(input_string)
    encryptor = AES.new(hashed.digest(), AES.MODE_CBC, '3aa349e1d3552b44')
    ciphertext = encryptor.encrypt(pad_to_sixteen(compressed))
    return ciphertext

def decrypt_and_decompress(input_string, key):
    hashed = MD5.new()
    hashed.update(key)
    decryptor = AES.new(hashed.digest(), AES.MODE_CBC, '3aa349e1d3552b44')
    decrypted = decryptor.decrypt(input_string)
    decompressed = zlib.decompress(decrypted)
    return decompressed
