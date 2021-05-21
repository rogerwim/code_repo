import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import string
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import time
import random
HOST=''
PORT=8485
def generate(l):
    randomstr = b''
    for i in range(1,l):
        randomstr += bytes([random.randint(0,255)])
    #print(randomstr)
    return randomstr
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()
session_key = get_random_bytes(16)
nonce = get_random_bytes(8)
data_in = pickle.loads(conn.recv(8192))
public_key = data_in["public key"]
signature = data_in["signature"]
recipient_key = RSA.import_key(public_key)
print(data_in)
print(addr)
while True:
        try:
                pkcs1_15.new(recipient_key).verify(h,signature)
                print("signature correct")
                break
        except:
                thing = generate(100)
                h = SHA256.new(thing)
                print(h.hexdigest())
                print("signature error, abort")
                conn.sendall(b"i do not like you, you have a signature error, i will give you 1 more chance, please sign the next messsage")
                conn.sendall(pickle.dumps({"thing to sign":thing}))
                signature = pickle.loads(conn.recv(8192))['signature']
                print(signature)
# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)


session_key = get_random_bytes(16)
nonce = get_random_bytes(8)
# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_CTR,nonce=nonce)
conn.sendall(pickle.dumps({'encrypted session key':enc_session_key,
                                    'nonce':nonce}))
print(session_key,nonce)
data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(8192)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(8192)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame_data = cipher_aes.decrypt(frame_data)
    frame_data = zlib.decompress(frame_data)
    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)
