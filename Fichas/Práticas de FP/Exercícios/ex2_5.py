def ocorrencias(n, a):
    count = 0
    while n > 0:
        if n%10==a:
            count+=1
        n //= 10
    return count


if __name__ == '__main__':
    n = int(input('Escreva um inteiro positivo\n? '))
    a = int(input('Escreva um dígito\n? '))
    print('Número de ocorrencias do digito {}: {}'.format(a, ocorrencias(n,a)))