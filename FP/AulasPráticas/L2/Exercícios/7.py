def valor(horas, rate):
    if horas<40:
        return horas*rate
    else:
        return (40*rate)+((horas-40)*(rate*2))


data = input().split()
horas, rate = int(data[0]), int(data[1])

print('Ordenado semanal: ', valor(horas, rate))