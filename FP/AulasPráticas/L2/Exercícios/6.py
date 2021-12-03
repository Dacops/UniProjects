def maior(x):
    b = int(x[0])
    for i in range(len(x)):
        c = int(x[i])
        if c > b:
            b = c
        else:
            pass
    return b

x = input().split()
print('O maior número é: ', maior(x))