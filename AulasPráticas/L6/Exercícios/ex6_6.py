def conta_palavras(cc):
    palavras = {}
    cc = cc.split()
    for palavra in cc:
        if palavra not in palavras:
            palavras[palavra] = 1
        else:
            palavras[palavra] += 1
    return palavras

if __name__ == '__main__':
    cc = 'a aranha arranha a ra a ra arranha a aranha nem a aranha arranha a ra nem a ra arranha a aranha'
    print(conta_palavras(cc))