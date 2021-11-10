

n, t = int(input('Escreva um dígito\n(-1 para terminar)\n? ')), ''
while n!=-1:
    t += str(n)
    n = int(input('Escreva um dígito\n(-1 para terminar)\n? '))
print('O número é ', t)