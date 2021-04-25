import sys
import struct
import numpy as np
import hashlib
import gc
name = sys.argv[1]
prefer = 0 #1 is assume block 1 and 2 are correct, 2 is assume parity and block 1 is correct, 3 is assume parity and block 2 is correct
name1 = name + ".bk1"
name2 = name + ".bk2"
name3 = name + ".par"
file1 = open(name1,"rb")
file2 = open(name2,"rb")
file3 = open(name3,"rb")
block1 = file1.read()
block2 = file2.read()
par = file3.read()
print("files read")
file1.close()
file2.close()
file3.close()
out = b""
hasher = hashlib.sha256()
hasher.update(block1[:-64])
hash1 = hasher.hexdigest().encode()
if hash1 == block1[-64:]:
    print("block 1 valid")
    bk1val = True
else:
    print("block 1 invalid")
    bk1val = False
hasher = hashlib.sha256()
hasher.update(block2[:-64])
hash2 = hasher.hexdigest().encode()
if hash2 == block2[-64:]:
    print("block 2 valid")
    bk2val = True
else:
    print("block 2 invalid")
    bk2val = False
hasher = hashlib.sha256()
hasher.update(par[:-64])
hashpar = hasher.hexdigest().encode()
if hashpar == par[-64:]:
    print("parity block valid")
    parval = True
else:
    print("parity block invalid")
    parval = False
    
if bk1val == True and bk2val == True and parval == True:
    prefer = 0
    print("all data valid")
if bk1val == False and bk2val == True and parval == True:
    prefer = 3
    print("block 1 invalid, block 2 and parity block ok")
if bk1val == True and bk2val == False and parval == True:
    prefer = 2
    print("block 2 invalid, block 1 and parity block ok")
if bk1val == True and bk2val == True and parval == False:
    prefer = 1
    print("parity block invalid, block 2 and block 1 ok")
if bk1val == False and bk2val == False and parval == True:
    prefer = 0
    print("block 1 and 2 invalid, parity block ok, UNRECOVARABLE")
    exit()
if bk1val == False and bk2val == True and parval == False:
    prefer = 0
    print("block 1 and parity block invalid, block 2 ok, UNRECOVARABLE")
    exit()
if bk1val == True and bk2val == False and parval == False:
    prefer = 0
    print("block 2 and parity block invalid, parity block ok, UNRECOVARABLE")
    exit()
if bk1val == False and bk2val == False and parval == False:
    prefer = 0
    print("all blocks invalid, UNRECOVARABLE")
    exit()
block1 = block1[:-64]
block2 = block2[:-64]
par = par[:-64]
tempb1 = bytearray(block1)
tempb2 = bytearray(block2)
temppar = bytearray(par)
del block2
del block1
del par
gc.collect()
print("about to convert")
arr1 = np.array(tempb1)
del tempb1
gc.collect()
print("block 1 converted")
arr2 = np.array(tempb2)
del tempb2
gc.collect()
print("block 2 converted")
arr3 = np.array(temppar)
del temppar
gc.collect()
print("parity block converted")
result = np.bitwise_xor(arr1,arr2)
if not np.all(arr3 == result):
    print("corrupted data detected, correcting")
    if prefer == 1:
        pass
    if prefer == 2:
        arr2 = np.bitwise_xor(arr1,arr3)
    if prefer == 3:
        arr1 = np.bitwise_xor(arr2,arr3)
del arr3
del result
print("xor complete")
gc.collect()
arr_tuple = (arr1, arr2)
del arr1
del arr2
gc.collect()
out1 = np.vstack(arr_tuple).reshape((-1,), order='F')
print("interleave complete")
del arr_tuple
gc.collect()
out = out1.tobytes()
print("convert to bytes complete")
del out1
gc.collect()
    sig = out[:9]
    print(sig)
    count,sizet = struct.unpack("HQ",out[9:25])
    print("number of files:",count)
    print("total size:",sizet)
    read = 0
    offset = 25
    sizes = []
    while read != count:
        if read != 0:
            sign = out[:9]
            print(sign)
            offset += 9
        length = struct.unpack("H",out[offset:offset+2])[0]
        offset += 2 + length
        print("length of filename:",length)
        print("filename:", out[offset-length:offset].decode())
        size = struct.unpack("Q",out[offset:offset+8])[0]
        offset += 8 + size
        print("size:",size)
        sizes.append([offset-length-size-10,length,size,offset])
        read += 1

signature = out[:9]
count,size = struct.unpack("HQ",out[9:25])
if signature != b"ROGER_PAR":
    print("incorrect/corrupted file")
    out = []
out = out[25:]
files_read = 0
while files_read != count:
    if files_read != 0:
        sig = out[:9]
        out = out[9:]
        print(sig)
    length = struct.unpack("H",out[:2])[0]
    out = out[2:]
    files_read +=1
    filename = out[:length]
    out = out[length:]
    filesize = struct.unpack("Q",out[:8])[0]
    out = out[8:]
    content = out[:filesize]
    if content.endswith(b"\x00"):
        content = content[:-1]
    out = out[filesize:]
    file = open(filename,"wb")
    file.write(content)
    file.close()
