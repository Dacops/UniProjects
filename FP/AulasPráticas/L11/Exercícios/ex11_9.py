import ex11_8, functools

def produto_digitos(n, pred):
    return functools.reduce(lambda x,y:int(x)*int(y), list(filter(pred, ex11_8.lista_digitos(n))))

if __name__=='__main__':
    print(produto_digitos(12345, lambda x:x>3))