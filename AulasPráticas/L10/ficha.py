def invert(tup):
    def partes(tup_inv, tup):
        if not tup:
            return tup_inv
        return(partes(tup_inv+(tup[-1], ), tup[:-1]))
    return(partes((), tup))


    
#    t = ()
#    for i in range(len(tup)):
#        t += (tup[-1-i], )
#    return t
    
#    if not tup:
#        return ()
#    if len(tup)==1:
#        return tup
#    else:
#        return (tup[-1], )+invert(tup[1:-1])+(tup[0], )


if __name__=='__main__':
    print(invert((1,2,True)))
