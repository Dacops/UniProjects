def escreve_esparsa(cc):
    linha, coluna = [], []
    for coordenada in cc:
        linha.append(coordenada[0])
        coluna.append(coordenada[1])
    for l in range(max(linha)+1):
        linha = ''
        for c in range(max(coluna)+1):
            if (l,c) not in cc:
                linha += '0'
            else: 
                linha += str(cc[(l,c)])
        print(linha)


if __name__ == '__main__':
    cc = {(1,5): 4, (2, 3): 9, (4, 1): 1}
    print(escreve_esparsa(cc))