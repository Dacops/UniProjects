def soma_fn_for(n, fn):
    total = 0
    for i in range(n):
        total = total + fn(i+1)
    return total 

def soma_fn_rec(n, fn):
    def aux(total, n, fn):
        if n==0:
            return total
        return aux(total+fn(n), n-1, fn)
    return aux(0, n, fn)

if __name__=='__main__':
    print(soma_fn_rec(4, lambda x:x*x))
    print(soma_fn_rec(4, lambda x:x+1))