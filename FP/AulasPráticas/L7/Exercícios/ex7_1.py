a, b = 1, 3
racional = {'num':a, 'den':b}

def cria_rac(n,d):
    racional = str(n) + '/' + str(d)
    return racional

def num(r):
    r.split('/')
    return eval(r[0])

def den(r):
    r.split('/')
    return eval(r[-1])

def eh_racional(r):
    if den(r)<1:
        return False
    return True

def eh_rac_zero(r):
    if num(r)==0:
        return True
    return False

def rac_iguais(r1, r2):
    if num(r1)==num(r2) and den(r1)==den(r2):
        return True
    return False

def produto_rac(x, y):
    n, d = num(x)*num(y), den(x)*den(y)
    return cria_rac(n, d)

def escreve_rac(r1, r2):
    return cria_rac(r1, r2)

