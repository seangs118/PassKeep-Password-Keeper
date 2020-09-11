import os
import io
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from encodings.base64_codec import base64_encode


"""
A simple program to encrypt one file to another in fixed size blocks
variables:
fname: source file name
fname2: destination file name
blocksize: size of blocks in bytes
password: the plaintext password
ivval: the plaintext iv seed
salt: the kdf seed
"""
def decrypt(website, username):
    backend = default_backend()
    # ksalt = os.urandom(16)
    salt = b"1234567812345678"

    #print(salt.hex())

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=100000,
        backend=backend)

    idf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=100000,
        backend=backend)

    file = open("passwords.txt", 'r+')
    hash1 = file.read()
    passwd = hash1.encode()

    ivval = b'hello'

    key = kdf.derive(passwd)
    iv = idf.derive(ivval)

    #print(key.hex())
    #print(iv.hex())

    unpadder = padding.PKCS7(128).unpadder()

    cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.CBC(iv),
        backend=backend)

    decryptor = cipher.decryptor()

    # filenames
 #   website = input ("What website is this? \n")
 #   username = input('Which account is this? \n')
    fname = 'passKeep/%s/%s.txt'%(website, username)


    # get the full path names
    path = os.path.abspath(fname)


    # print message to user
    #print('copying ', path, 'to ', path2)

    # set the blocksize
    blocksize = 16

    # set the totalsize counter
    totalsize = 0

    # create a mutable array to hold the bytes
    data = bytearray(blocksize)

    # open the files
    file = open(fname, 'rb')

    fsize = file.seek(0,io.SEEK_END)
    file.seek(0,io.SEEK_SET)
    #print('size:',fsize)
    userPassword = ''

    # loop until done
    while True:
        # read block from source file
        num = file.readinto(data)

        # adjust totalsize
        totalsize += num
        fsize -= num

        # print data, assuming text data
        # print(num,data)
        # use following if raw binary data
        #print(fsize,data.hex())

        # check if full block read
        if fsize > 0:
            # write full block to destination
            pdata = decryptor.update(bytes(data))
            plaintext = unpadder.update(pdata)
            print(num,plaintext)
            #file2.write(plaintext)
            userPassword = userPassword + (plaintext.decode())
        else:
            # extract subarray
            data2 = decryptor.update(bytes(data)) + decryptor.finalize()
            plaintext = unpadder.update(data2) + unpadder.finalize()
            
            # write subarray to destination and break loop
            print(num,plaintext)
            #file2.write(plaintext)
            userPassword = userPassword + (plaintext.decode())
            
            break

    # close files (note will also flush destination file

    file.close()

    return userPassword

    # print totalsize
   # print('read ',totalsize,' bytes')

