def explode(n):
    if type(n)!=int:
        raise ValueError('explode: argumento não inteiro')
    tup, n = (), str(n)
    for i in n:
        i = eval(i)
        tup += (i, )
    return tup


if __name__ == '__main__':
    n = eval(input())
    print(explode(n))