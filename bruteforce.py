import random, crccheck
def generate(l):
    randomstr = b''
    for i in range(1,l):
        randomstr += bytes([random.randint(0,255)])
    #print(randomstr)
    return randomstr
def calculate(inputstr):
    a = crccheck.crc.Crc32()
    a.process(inputstr)
    #print(a.finalhex())
    return a.finalhex(),inputstr
def wrap(l):
    return calculate(generate(l))
while True:
    a = wrap(10)
    b = a[0]
    c = a[1]
    if b.startswith("0e") and b[2:4].isdecimal():
        print(b,c)
