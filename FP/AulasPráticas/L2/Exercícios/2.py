def km(dis, tempo):
    return round(dis/(tempo/60), 2)

def ms(dis, tempo):
    return round((dis*1000)/(tempo*60), 2)

dis = input('Qual a distância percorrida (em Km)? ')
tempo = input('Qual o tempo necessário para percorrer a dita distância (em Min)? ')
dis, tempo = int(dis), int(tempo)

print('Velocidades:\n', km(dis, tempo), ' Km/h\n', ms(dis, tempo), ' m/s')