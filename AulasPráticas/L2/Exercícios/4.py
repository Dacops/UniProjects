def t(s):
    global d
    global h
    global m
    global seg
    d = s//86400

    while s>=86400:
        s -= 86400
    h = s //3600

    while s>=3600:
        s -= 3600
    m = s//60

    while s>=60:
        s -= 60
    seg = s

s = input('Escreva o número de segundos ')
s, d, h, m, seg = int(s), 0, 0, 0, 0
t(s)
print('dias: ', d, ' horas: ', h, ' mins: ', m, 'segs ', seg)
