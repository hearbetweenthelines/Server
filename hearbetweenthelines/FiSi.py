"""
#Author: Eric Hennenfent
Compresses and encrypts the file to be hidden and stores after the last MP3 frame.
"""

from itertools import izip_longest
from process import compress_and_encrypt, decrypt_and_decompress
import md5

def pad_to_byte(stir):
    out=''
    num = 8 - len(stir)
    for i in range(num):
        out += '0'
    out += stir
    out = out.replace('None','0')
    return out

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def string_to_binary(stir):
    return ''.join(pad_to_byte(format(ord(x), 'b')) for x in stir)

def binary_to_string(stir):
    out = ""
    for k in grouper(stir, 8):
        stir = ""
        for j in k:
            stir += str(j)
        out += chr(int(pad_to_byte(stir), 2))
    return out

def bytearray_to_binary(bites):
    return ''.join(pad_to_byte(format(x, 'b')) for x in bites)

def output(inpot, output_filename):
    f = open(output_filename,'w')
    f.write(inpot)
    f.close()

def hide(cleartext_filename, file_to_hide_in, key, offset=0, output_filename=''):
    # Open cleartext and text to be hidden
    f = open(file_to_hide_in)
    k = f.read()
    hashy = md5.new()
    hashy.update(k)
    hashy = hashy.digest()
    bites = bytearray(k)

    f = open(cleartext_filename)
    j = 'EOMp3F' +  hashy + compress_and_encrypt(f.read(),key)
    hiddenbites = bytearray(k)

    out = k + j
    output(out, output_filename)
    return out

def extract(stego_file, key, offset=0, printoutput=False):
    # Decode from file (comment the first two lines to use the output from before)
    f = open(stego_file)
    full = f.read()
    audio = full.split('EOMp3F')[0]
    hashy = md5.new()
    hashy.update(audio)
    hashy = hashy.digest()
    ciphertext = full.split(hashy)[1]
    decrypted = decrypt_and_decompress(ciphertext, key)
    if(printoutput):
        try:
            print decrypted
        except:
            output(decrypted, 'extracted.txt')
    return decrypted

def main():
    import sys
    option = raw_input("Encode (e) or Decode (d) >")
    if option == 'e':
        b = raw_input("File to hide >")
        a = raw_input("File to hide " + b + " in >")
        key = raw_input("Encryption Key >")
        if(len(sys.argv) > 1):
            hide(b, a, key, output_filename=str(sys.argv[1]))
        else:
            hide(b, a, key)

    if option == 'd':
        u = raw_input("Stego file >")
        key = raw_input("Encryption Key >")
        extract(u, key, printoutput=True)

if __name__ == "__main__":
    main()