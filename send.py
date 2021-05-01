import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import requests
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
file = open('private.pem','rb')
key_exp = file.read()
file.close
key = RSA.import_key(key_exp)
private_key = key.export_key()
public_key = key.publickey().export_key()
public = True # connecting to outside
if public:
    a = requests.get('http://api.ipify.org?format=json')
    ip = json.loads(a.text)['ip']
else:
    ip = socket.gethostbyname(socket.gethostname())
print(ip)
h = SHA256.new(ip.encode())
signature = pkcs1_15.new(key).sign(h)
print(h.hexdigest(),signature)
i = 0
while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.178.66', 8485))
        break
    except:
        i += 1
        print(i,"failures")
connection = client_socket.makefile('wb')
client_socket.sendall(pickle.dumps({"public key":public_key,"signature":signature,"ip":ip}))
while True:
    a = client_socket.recv(8192)
    print(a)
    if a == b'i do not like you, you have a signature error, i will give you 1 more chance, please sign your ip(next messsage)':
        print("public varibale is probably wrong")
        a = client_socket.recv(8192)
        data = pickle.loads(a)
        ip = data["thing to sign"]
        h = SHA256.new(ip.encode())
        signature = pkcs1_15.new(key).sign(h)
        print(h.hexdigest(),signature,ip,data)
        client_socket.sendall(pickle.dumps({"signature":signature}))
    else:
        break
data = pickle.loads(a)
enc_key = data['encrypted session key']
nonce = data['nonce']
print(data)
decrypter = PKCS1_OAEP.new(RSA.import_key(private_key))
key = decrypter.decrypt(enc_key)
print(key,nonce)
#exit()
cipher_aes = AES.new(key, AES.MODE_CTR,nonce = nonce)
cam = cv2.VideoCapture(1)

cam.set(3, 1280)
cam.set(4, 720)
#cam.set(3,320)
#cam.set(4,240)
img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame,1)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = zlib.compress(pickle.dumps(frame, 5))
    #data = pickle.dumps(frame, 0)
    #print(data)
    data = cipher_aes.encrypt(data)
    #print(data)
    size = len(data)
    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
cam.release()
