def primo(n):
    divisor, count = 2, 0
    while divisor < n:
        if n%divisor==0:
            print(divisor)
            divisor += 1
            count += 1
        else:
            divisor += 1
    if count == 0:
        print('primo')


if __name__ == '__main__':
    n = int(input('Escreva um inteiro positivo\n? '))
    primo(n)