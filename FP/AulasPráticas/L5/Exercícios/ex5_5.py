def matriz(m):
    forma = ''
    for linha in m:
        for indice in linha:
            forma += str(indice) + ' '
        forma += '\n'
    return forma

if __name__ == '__main__':
    m = eval(input())
    print(matriz(m))