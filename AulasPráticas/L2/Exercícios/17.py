def c(notas):
    count = 0
    for i in range(len(notas)):
        if int(notas[i]) >= 10:
            count += 1

    print(count, ' Nota(s) Positivas ', round((count/i)*100, 2),' %')
    


notas = input().split()
c(notas)