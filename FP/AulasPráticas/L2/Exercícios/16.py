def r(n):

    casas, a, num, r = 0, 1, 0, 0

    while a != 0:
        a = n//(10**(casas+1))
        casas += 1

    num = n*(10**casas)
    
    for i in range(casas):
        r = n%(10**(i+1))
        r = r//(10**i)
        num += r*(10**(casas-(i+1)))
    
    return(num)


n = int(input('Escreva um inteiro\n? '))
print(r(n))