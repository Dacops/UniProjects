def elemento_matriz(m, linha, coluna):
    try:
        return m[coluna][linha]
    except:
        raise ValueError('elemento_matriz: indice invalido, coluna {}'.format(coluna))


if __name__ == '__main__':
    m, linha, coluna = eval(input())
    print(elemento_matriz(m, linha, coluna))