def zeros(num):

    save, count = 1, 0

    for i in range(len(num)):

        if save == num[i] and save=='0':
            count += 1

        save = num[i]
    
    return(count)
        

num = input('Escreva um inteiro\n? ')
print('O número tem ', zeros(num), ' zero(s) seguidos')