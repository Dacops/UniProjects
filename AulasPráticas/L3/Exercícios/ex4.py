def area_coroa(r1,r2):
    if r1>r2:
        raise ValueError('r1 não pode ser maior que r2')
    print('r1 : ', 3.14*(r1**2), '\nr2: ', 3.14*(r2**2))



r1, r2 = int(input('r1: ')), int(input('r2: '))
area_coroa(r1, r2)