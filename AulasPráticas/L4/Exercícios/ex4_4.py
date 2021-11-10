def filtra_pares(n):
    tup = ()
    for i in n:
        if i%2==0:
            tup += (i, )
    return tup
        

if __name__ == '__main__':
    n = eval(input())
    print(filtra_pares(n))