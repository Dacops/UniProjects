def soma_els_atomicos(tup):
    if not tup:
        return 0
    else:
        if type(tup[0])==tuple:
            return soma_els_atomicos(tup[0]+tup[1:])
        else:
            return soma_els_atomicos(tup[1:])+tup[0]

if __name__=='__main__':
    print(soma_els_atomicos((3, ((((((6, (7, ))), ), ), ), ), 2, 1)))
    print(soma_els_atomicos(((((),),),)))