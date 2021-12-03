def serie_geom(r, n):
    if n < 0:
        raise ValueError('serie_geom: argumento incorreto')
    else:
        soma = 0
        for i in range(n+1):
            soma += r**(i)
    return soma


if __name__ == '__main__':
    r, n = input().split()
    r, n = eval(r), eval(n)
    print(serie_geom(r, n))