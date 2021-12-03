def par(n):
    count, total = 0, 0
    while count <= n:
        if count%2==0:
            total += count**3
        count += 1
    return total


if __name__ == '__main__':
    n = int(input('Soma cubos pares\nEscreva um inteiro positivo '))
    print(par(n))