def impar(n):
    t = ''
    for i in range(len(n)):
        if int(n[i])%2==0:
            pass
        else:
            t += n[i]
    return t


n = input('Escreva um inteiro positivo\n? ')
print('Resultado: ', impar(n))