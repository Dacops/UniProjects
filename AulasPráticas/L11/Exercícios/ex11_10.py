import ex11_8

def apenas_digitos_impares(n):
    return list(filter(lambda x:x%2!=0, ex11_8.lista_digitos(n)))

 
if __name__=='__main__':
    print(apenas_digitos_impares(12345))
