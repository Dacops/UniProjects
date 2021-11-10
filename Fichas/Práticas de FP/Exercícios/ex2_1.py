def impar(n):
    count, total = 0, 0
    while count <= n:
        if count%2!=0:
            total += count**2
        count += 1
    return total


if __name__ == '__main__':
    n = int(input('Soma quadrados ímpares\nEscreva um inteiro positivo '))
    print(impar(n))