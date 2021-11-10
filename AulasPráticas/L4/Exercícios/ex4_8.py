def junta_ordenados(t1, t2):
    t3, a, t = t1 + t2, [], ()
    for i in t3:
        a += [i, ]
    a.sort()
    for i in a:
        t += (i, )
    return t


if __name__ == '__main__':
    t1, t2 = input().split('), ')
    t1 = t1 + ')'
    t1, t2 = eval(t1), eval(t2)
    print(junta_ordenados(t1, t2))