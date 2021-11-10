def media(data):
    global avg
    tot = int(data[0])+int(data[1])+int(data[2])+int(data[3])+int(data[4])
    avg = tot/5
    return tot/5

def desvio(data):
    des = []
    for i in range(len(data)):
        des.append((int(data[i])-avg)**2)
    tot = int(des[0])+int(des[1])+int(des[2])+int(des[3])+int(des[4])
    return round((tot*0.25)**.5, 2)

data = input()
data = data.split()
print('Média: ', media(data), '\nDesvio Padrão: ', desvio(data))