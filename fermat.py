def factor(n, verbose=True):
    for q in range(2,n):
        p = n//q
        if verbose:
            print(p,q,p*q)
        if p*q == n:
            return p,q

n=463182115968721326101398370978205943762
factors = factor(n)
