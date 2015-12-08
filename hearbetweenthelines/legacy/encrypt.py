"""
#Author: Eric Hennenfent
Compresses and encrypts the file to be hidden and stores it in the least significant bit of each byte. 
This is a messy way to to Stego but it works for small amounts.
"""

from itertools import izip_longest
from process import compress_and_encrypt, decrypt_and_decompress

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

def encode(cleartext_bin, encoding_bin):
    length = len(encoding_bin)
    out = []
    chunks = grouper(cleartext_bin, 8)
    bits = grouper(encoding_bin, 1)
    zipped = zip(chunks, bits)
    for k in zipped:
        temp = list(k[0])
        temp[7] = k[1][0]
        out.append(''.join(z for z in temp))
    i = 0
    for p in chunks:
        if(i <= length):
            i += 1
        else:
            out.append( pad_to_byte( ''.join(z for z in list(p)) ) )
    return ''.join(k for k in out)

def decode(ciphertext_bin):
    out = []
    chunks = grouper(ciphertext_bin, 8)
    for k in chunks:
        out.append(k[7])
    return ''.join(k for k in out)

def output(inpot, output_filename):
    f = open(output_filename,'w')
    f.write(inpot)
    f.close()

def hide(cleartext_filename, file_to_hide_in, key, output_filename=''):
    # Open cleartext and text to be hidden
    f = open(file_to_hide_in)
    k = f.read()
    bites = bytearray(k)

    f = open(cleartext_filename)
    k = compress_and_encrypt(f.read(),key) + 'EOStegF'
    hiddenbites = bytearray(k)

    # Encode stego
    out = encode(bytearray_to_binary(bites),bytearray_to_binary(hiddenbites))
    if(len(output_filename) < 1):
        name = 'out.' + str(file_to_hide_in).split('.')[1]
        print ('No filename specificed, outputting to ') + name
        output_filename = name
    output(binary_to_string(out), output_filename)
    return binary_to_string(out)

def extract(stego_file, key, printoutput=False):
    # Decode from file (comment the first two lines to use the output from before)
    f = open(stego_file)
    out = string_to_binary(f.read())
    full = binary_to_string(decode(out))
    decrypted = decrypt_and_decompress(full.split('EOStegF')[0], key)
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
            hide(b,a,key,str(sys.argv[1]))
        else:
            hide(b,a,key)

    if option == 'd':
        u = raw_input("Stego file >")
        key = raw_input("Encryption Key >")
        extract(u, key, True)

if __name__ == "__main__":
    main()
