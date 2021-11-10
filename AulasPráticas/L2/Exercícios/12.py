from math import factorial

def soma(x, m):
    tot = 0
    for i in range(n+1):
        t = x**i/factorial(i)
        tot += t
    return tot

x = int(input('Qual o valor de x\n? '))
n = int(input('Qual o valor de n\n? '))
print('O valor da soma é ', soma(x, n))