def op(x,y):
    return ((x+3*y)*(x-y))

x = input('Vou-lhe pedir dois números\nEscreva o primeiro número, x = ')
y = input('Escreva o segundo número, y = ')
x, y = int(x), int(y)
print('O valor de (',x,' + 3 * ',y,') * (',x,' - ',y,') é: ', op(x,y))