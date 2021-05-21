import sys
import os
import struct
import numpy as np
import hashlib
temp = b""
filen = sys.argv[1]
filen = os.path.abspath(os.path.expanduser(sys.argv[1]))
file = open(filen,"rb")
temp += b"ROGER_PAR" # signature
temp += b"\x00"*18
temp += filen.encode() # filename
if (len(temp)+ os.path.getsize(filen))% 2 == 1:
    temp += struct.pack("Q", os.path.getsize(filen)+1) # size of file
else:
    temp += struct.pack("Q", os.path.getsize(filen)) # size of file
temp += file.read()
if len(temp) % 2 == 1:
    temp += b"\x00"
file.close()
size = len(temp)
temp = bytearray(temp)
begin = temp[:9]
end = temp [27:]
temp = (begin + struct.pack("HQH",1,size,len(filen)) + end ) # file count, total size of file, length of filename
block1 = b""
block2 = b""
par = b""
CHANNEL_COUNT = 2
frames = np.array(temp)
deinterleaved = [frames[idx::CHANNEL_COUNT] for idx in range(CHANNEL_COUNT)]
output = np.bitwise_xor(deinterleaved[0],deinterleaved[1])
block1 = bytes(deinterleaved[0])
block2 = bytes(deinterleaved[1])
par = bytes(output)
hasher = hashlib.sha256()
hasher.update(block1)
block1 += hasher.hexdigest().encode()
hasher = hashlib.sha256()
hasher.update(block2)
block2 += hasher.hexdigest().encode()
hasher = hashlib.sha256()
hasher.update(par)
par += hasher.hexdigest().encode()
out1 = open(filen+".bk1","wb")
out2 = open(filen+".bk2","wb")
out3 = open(filen+".par","wb")
out1.write(block1)
out2.write(block2)
out3.write(par)
out1.close()
out2.close();
out3.close()
