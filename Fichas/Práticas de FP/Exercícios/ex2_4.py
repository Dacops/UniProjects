def prova(n):
    soma = 0
    while n != 0:
        soma += n%10
        n //= 10
    while soma >= 9:
        soma -= 9
    return soma

if __name__ == '__main__':
    n = int(input('Escreva um inteiro postitivo\n? '))
    print(prova(n))