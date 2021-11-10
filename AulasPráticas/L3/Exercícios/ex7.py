def valor(q, j, n):
    if q<0 or j<0 or j>1 or n<0:
        raise ValueError('Os valores introduzidos não são válidos')
    else:
        return q * (1+j)**n

def duplicar(q, j):
    count = 0
    while q*(1+j)**count < 2*q:
        count += 1
    return count


if __name__ == '__main__':
    q, j, n = input().split()
    q, j, n = eval(q), eval(j), eval(n)
    print(valor(q, j, n))
    print(duplicar(q, j))