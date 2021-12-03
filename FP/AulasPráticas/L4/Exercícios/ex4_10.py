def codifica(caracteres):
    par, impar = caracteres[0::2], caracteres[1::2]
    return par + impar

def descodifica(caracteres):
    i = len(caracteres)//2+1
    par, impar, r, count = caracteres[:i], caracteres[i:], '', 0
    for i in range(len(impar)):
        r += par[i]
        r += impar[i]
        count += 1
    if len(par) > len(impar):
        r += par[count]
    return r

if __name__=='__main__':
    caracteres = input()
    print(codifica(caracteres))
    print(descodifica(codifica(caracteres)))