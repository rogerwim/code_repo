import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
key = RSA.generate(2048)
private_key = key.export_key()
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()






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
client_socket.sendall(pickle.dumps({"public key":public_key}))
time.sleep(0.5)
a = client_socket.recv(8192)
exit()
cipher_aes = AES.new(session_key, AES.MODE_CTR,nonce = nonce)
cam = cv2.VideoCapture(1)

cam.set(3, 1920);
cam.set(4, 1080);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = zlib.compress(pickle.dumps(frame, 0))
    #data = pickle.dumps(frame, 0)
    data = cipher_aes.encrypt(data)
    size = len(data)

    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()
