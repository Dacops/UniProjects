import ex11_4

def soma_quadrados_impares(lst):
    lst = ex11_4.filtra(lst, lambda x:x%2!=0)
    lst = ex11_4.transforma(lst, lambda x:x**2)
    return ex11_4.acumula(lst, lambda x,y:x+y)

if __name__=='__main__':
    print(soma_quadrados_impares([1,2,3,4,5,6]))
