def divisor(n):
    d, count = 1, 0
    while d < n:
        if n%d==0:
            count += 1
        d += 2
    return count


if __name__ == '__main__':
    n = int(input('Número divisores pares\nEscreva um inteiro positivo '))
    print(divisor(n))