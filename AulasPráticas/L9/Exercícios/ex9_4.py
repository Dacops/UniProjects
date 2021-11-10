def soma_n_vezes(a, b, n):
    if n==0:
        return b
    else:
        return a+soma_n_vezes(a,b,n-1)


if __name__=='__main__':
    print(soma_n_vezes(3,2,5))