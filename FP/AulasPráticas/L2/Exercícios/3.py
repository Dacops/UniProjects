def dias(s):
    return s/86400

s = input('Escreva um número de segundos\n? ')
s = int(s)
print('O número de dias correspondentes é ', dias(s))