def dias(s):
    return s/86400 

s = int(input('Escreva um número de segundos\n(um número negativo para terminar)\n? '))
while s>0:
    print('O número de dias correspondentes é ', dias(s))
    s = int(input('Escreva um número de segundos\n(um número negativo para terminar)\n? '))