import serial
import time
a = serial.Serial("COM5",timeout=10)
#data = b"\x11\x01\x1E\xD0\x0D\x0A" # read filmware version
data = b"\x11\x01\x01\xED\x0D\x0A" # read co2
def check_status(status):
    if status == 0:
        print("senor nominal")
    if (status >> 0) & 1:
        print("preheat not done")
    if (status >> 1) & 1:
        print("general sensor error")
    if (status >> 2) & 1:
        print("ppm too high")
    if (status >> 3) & 1:
        print("ppm too low")
    if (status >> 4) & 1:
        print("not calibrated")
    if (status >> 5) & 1:
        print("sensor drift")
while True:
    a.write(data)
    header = a.read(2)
    if header[0] == 0x16:
        print("header seems intact")
    else:
        print("header seems corrupt")
    command = a.read(header[1])
    if command[0] == data[2]:
        print("command matches")
    else:
        print("command seems off")
    cksum = a.read(1)
    calc = 0
    for i in header+command:
        calc += i
    calc = calc % 256
    calc = 256 - calc
    if calc == cksum[0]:
        print("packet intact")
    else:
        print("invalid packet")
    ppm = command[1] * 256 + command[2] # decode ppm
    #name = command[1:17] # decode name
    status = command[3] # get status byte
    check_status(status)
    #print(header,command,cksum,calc,cksum[0],name.decode()) # print name
    print(header,command,cksum,calc,cksum[0],ppm) # print ppm
    time.sleep(1)
