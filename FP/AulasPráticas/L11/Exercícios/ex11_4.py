def filtra(lst, tst):
    def aux(lst, tst, fil):
        if not lst:
            return fil
        else:
            if tst(lst[0]):
                fil.append(lst[0])
        return aux(lst[1:], tst, fil)
    return aux(lst, tst, [])

def transforma(lst, fn):
    def aux(lst, fn, tra):
        if not lst:
            return tra
        else:
            tra.append(fn(lst[0]))
        return aux(lst[1:], fn, tra)
    return aux(lst, fn, [])

def acumula(lst, fn):
    if len(lst)==1:
        return lst[0]
    lst[1] = fn(lst[0], lst[1])
    return acumula(lst[1:], fn)

if __name__=='__main__':
    print(filtra([1,2,3,4,5], lambda x:x%2==0))
    print(transforma([1,2,3,4], lambda x:x**3))
    print(acumula([1,2,3,4], lambda x,y:x+y))