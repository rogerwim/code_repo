
import hashlib,time,secrets
seed = b""
def gen():
    token = secrets.token_hex(32)
    return token
def init(data):
    global seed
    seed = data.encode()
def next_block(count=1, hide_seed=True):
    global seed
    output = []
    for i in range(count):
        hasher = hashlib.sha256()
        hasher.update(seed)
        hasher2 = hashlib.sha256()
        hasher2.update(hasher.digest())
        out = hasher2.hexdigest()
        seed = hasher.hexdigest().encode()
        if not hide_seed:
            output.append([out,seed.decode()])
        else:
            output.append([out,"XX"*32])
    return output
def show(output):
    for h in output:
        print("output:",h[0],"\nseed:",h[1],"\n")
def randint(low,high,count):
    output = []
    blocks = next_block(count)
    for block in blocks:
        a = int(block[0],16)
        b = low + (a % (1+high-low))
        print(b)
        output.append(b)
    return output
