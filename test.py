from random import randrange, getrandbits, randint
import math
from Crypto.Math.Numbers import Integer
from Crypto.PublicKey.RSA import RsaKey
from functools import cache
@cache
def is_prime(n, k=128):
    """ Test if a number is prime        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True
def generate_prime_candidate(length):
    """ Generate an odd integer randomly        Args:
            length -- int -- the length of the number to generate, in bits        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p
def generate_prime_number(length=1024):
    """ Generate a prime        Args:
            length -- int -- length of the prime to generate, in          bits        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 1):
        p = generate_prime_candidate(length)
    return p
class Key(RsaKey):
    def __init__(self,key):
        # {'n':n,'p':p,'q':q,'e':e,'d':d,'k':k,'phi n':a}
        self._n = key['n']
        self._p = key['p']
        self._q = key['q']
        self._e = key['e']
        self._d = key['d']
        self._u = key['u']
        self._dp = key['dp']
        self._dq = key['dq']
    def __str__(self):
        return(f"N:{self.n}\np:{self.p}\nq:{self.q}\ne:{self.e}")
def gen_key(size,e=65537,p=None,q=None,close_max=1):
    print(p,q)
    keep_p = False
    keep_q = False
    if p != None and q != None:
        print("p and q given")
        if type(p) != int:
            raise NotImplementedError("p must be a int")
        if type(q) != int:
            raise NotImplementedError("q must be a int")
    elif p == None and q != None:
        print("gen p")
        p = generate_prime_number(int(size/2))
        keep_q = True
    elif q == None and p != None:
        print("gen q")
        q = generate_prime_number(int(size/2))
        keep_p = True
    else:
        print("gen p and q")
        p = generate_prime_number(int(size/2))
        q = generate_prime_number(int(size/2))
    n = p * q
    a  = (p-1) * (q-1)
    b = math.gcd(e,a)
    if b > 1 or (p-q)/max(p,q) > close_max or (q-p)/max(p,q) > close_max:
        print("retry",q-p)
        if keep_p and not keep_q:
            key = gen_key(size,e,close_max=close_max,p=p)
        if not keep_p and keep_q:
            key = gen_key(size,e,close_max=close_max,q=q)
        if not keep_p and not keep_q:
            key = gen_key(size,e,close_max=close_max)
        return key
    k = 1
    valid = False
    while not valid:
        ed = k*a+1
        d = ed//e
        if ed == d*e and k % e != 0:
            valid = True
        else:
            k += 1
    n = Integer(n)
    p = Integer(p)
    q = Integer(q)
    e = Integer(e)
    d = Integer(d)
    u = Integer(p).inverse(q)
    dp = d % (p - 1)  # = (e⁻¹) mod (p-1)
    dq = d % (q - 1)  # = (e⁻¹) mod (q-1)
    return {'n':n,'p':p,'q':q,'e':e,'d':d,'k':k,'phi n':a,'u':u,'dp':dp,'dq':dq}
if __name__ == '__main__':
    pass
    #key = gen_key(2048)
    #a = Key(key)
