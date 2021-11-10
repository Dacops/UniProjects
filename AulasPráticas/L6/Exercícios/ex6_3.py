import random

def baralho():
    naipe = ('espadas', 'copas', 'ouros', 'paus')
    valor = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
    cartas = []
    for n in naipe:
        for v in valor:
            c = {}
            c['np']=n
            c['vlr']=v
            cartas.append(c)

    p, t = [], []
    for i in range(4):
        c_b = []
        while len(c_b)!=13:
            carta = round(random.random()*51)
            if cartas[carta] not in p:
                p.append(cartas[carta])
                c_b.append(cartas[carta])
        t.append(c_b)
    return t


print(baralho())