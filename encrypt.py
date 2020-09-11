import os
import io
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from encodings.base64_codec import base64_encode
import randomGenerator

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
def encrypt(username, website, length, special, caps, nums):
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

    padder = padding.PKCS7(128).padder()

    cipher = Cipher(
        algorithm=algorithms.AES(key),
        mode=modes.CBC(iv),
        backend=backend)

    encryptor = cipher.encryptor()

    # filenames
    #fname = 'index.py'

    userPassword = randomGenerator.randomGenerate(length, special, caps, nums)
    userPassword = userPassword

    dirPath = ('passKeep/%s' %(website))
    #dirPath =('passKeep/https://google.com')

    if(not(os.path.isdir(dirPath))): #if directory doesnt exists
            try:
                os.mkdir(dirPath,0o777)
            except:
                print ("Creation of the directory %s failed" % dirPath)
                exit(0)


    fname2 = ('%s.txt' %(username))
    # get the full path names
    #path = os.path.abspath(fname)
    path2 = os.path.abspath('%s/%s' %(dirPath, fname2))

    # print message to user
    #print('copying ', path, 'to ', path2)

    # set the blocksize
    blocksize = 16

    # set the totalsize counter
    totalsize = 0

    # create a mutable array to hold the bytes
    data = bytearray(blocksize)

    # open the files
    #file = open(fname, 'rb')
    file2 = open(path2, 'wb+')

    #print('filesize:', os.fstat(file.fileno()).st_size)

    # loop until done
    while True:
        # read block from source file
        temp = userPassword.encode()
        num = len(temp)
        data = temp
        #num = file.readinto(data)

        # adjust totalsize
        totalsize += num

        # print data, assuming text data
        print(num,data)
        # use following if raw binary data
        # print(num,data.hex())

        # check if full block read
        if num == blocksize:
            # write full block to destination
            pdata = padder.update(bytes(data))
            ciphertext = encryptor.update(pdata)
            file2.write(ciphertext)
        else:
            # extract subarray
            data2 = data[0:num]
            pdata = padder.update(bytes(data2)) + padder.finalize()
            ciphertext = encryptor.update(pdata) + encryptor.finalize()

            # write subarray to destination and break lo1op
            file2.write(ciphertext)
        # file2.write(b"\n")
        break

    # close files (note will also flush destination file
    #file.close()
    file2.close()

    # print totalsize
    print('read ',totalsize,' bytes')

