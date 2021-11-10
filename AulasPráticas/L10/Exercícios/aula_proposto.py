def soma_par_iter(lst):
    total = 0
    for elemento in lst:
        if elemento%2==0:
            total+=elemento
    return total


def soma_par_cauda(lst):
    def soma(par, lst):
        if not lst:
            return par
        if lst[0]%2==0:
            return soma(par+lst[0], lst[1:])
        else:
            return soma(par, lst[1:])

    if not lst:
        return 0
    else:
        if lst[0]%2==0:
            return soma(lst[0], lst[1:])
        else:
            return soma_par_cauda(lst[1:])


def soma_par_linear(lst):
    if not lst:
        return 0
    else:
        if lst[0]%2==0:
            return lst[0]+soma_par_linear(lst[1:])
        else:
            return soma_par_linear(lst[1:])

if __name__=='__main__':
    lst = [1,2,3,4,5,6,7,8,9]
    print(soma_par_iter(lst))
    print(soma_par_cauda(lst))
    print(soma_par_linear(lst))