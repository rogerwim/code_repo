import sys
import struct
import numpy as np
import hashlib
import gc
import os
def add(name,to_add):
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
    if prefer != 0:
        print("corrupted data")
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
    del temppar
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
    out += b"ROGER_PAR"
    out += struct.pack("H",len(to_add))
    out += to_add.encode()
    if (len(out)+ os.path.getsize(to_add))% 2 == 1:
        out += struct.pack("Q", os.path.getsize(to_add)+1) # size of file
    else:
        out += struct.pack("Q", os.path.getsize(to_add)) # size of file
    file = open(to_add,'rb')
    out += file.read()
    file.close()
    if len(out) % 2 == 1:
        out += b"\x00"
    middle = struct.pack("HQ",count+1,len(out))
    start = out[:9]
    out = out[25:]
    out = start + middle + out
    CHANNEL_COUNT = 2
    out = bytearray(out)
    frames = np.array(out)
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
    out1 = open(name+".bk1","wb")
    out2 = open(name+".bk2","wb")
    out3 = open(name+".par","wb")
    out1.write(block1)
    out2.write(block2)
    out3.write(par)
    out1.close()
    out2.close()
    out3.close()
