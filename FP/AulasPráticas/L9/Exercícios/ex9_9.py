def parte(lst, n):
    def partes(m, l, M, n):
        if not l:
            return [m, M]
        if l[0]<n:
            return partes(m+[l[0], ], l[1:], M, n)
        else:
            return partes(m, l[1:], M+[l[0], ], n)
    if lst[0]<n:
        return partes([lst[0], ], lst[1:], [], n)
    else:
        return partes([], lst[1:], [lst[0], ], n)
    

if __name__=='__main__':
    print(parte([3, 5, 1, 4, 5, 8, 9], 4))