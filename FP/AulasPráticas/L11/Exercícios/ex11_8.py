def lista_digitos(n):
    return list(map(lambda x:int(x), str(n)))

if __name__=='__main__':
    print(lista_digitos(123))