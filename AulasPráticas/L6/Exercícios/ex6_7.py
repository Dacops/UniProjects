def mostra_ordenado(cc):
    palavras = []
    for palavra in cc:
        palavras.append(palavra)
    palavras.sort()
    for palavra in palavras:
        print(palavra, cc[palavra])
        

if __name__ == '__main__':
    cc = {'a': 8, 'aranha': 4, 'arranha': 4, 'ra': 4, 'nem': 2}
    print(mostra_ordenado(cc))