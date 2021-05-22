import socket
import math
HOST=''
PORT=8000

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
temp = 0
def do_start():
    global temp
    conn.sendall(b"please enter power laser setting(effects heat output, cannot be bigger then 100)")
    PL_level = int(conn.recv(8192).decode())
    conn.sendall(b"please enter heater setting(effects startup time, do not enter < 50 or > 100)")
    heater_level = int(conn.recv(8192).decode())
    i = 0
    while temp < 150000000 and i < 10000:
        temp = temp + math.sqrt(3000000*heater_level-temp)
        conn.sendall(b"current temp:"+str(temp).encode())
        i += 1
    print("STARTUP complete")
while True:
    conn,addr=s.accept()
    print(addr)
    conn.sendall(b"enter command:")
    command = conn.recv(8192)
    if command == b"start":
        if addr[0] != "192.168.178.20":
            conn.sendall(b"you do not have the permissions to start the fusion reactor, this can only be done from 192.168.178.20")
        else:
            conn.sendall(b"starting fusion reactor ingition squence, this MAY fail")
            do_start()
    else:
        conn.sendall(b"invalid command")
