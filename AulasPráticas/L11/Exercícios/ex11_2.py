def piatorio(l_inf, l_sup, operacao, inc):
    total = 1
    while l_inf <= l_sup:
        total = total * operacao(l_inf)
        l_inf = inc(l_inf)
    return total

if __name__=='__main__':
    print(piatorio(1, 5, lambda x:x, lambda x:x+1))

# b) factorial, sendo l_sup o número do qual queremos o factorial e l_inf sempre 1.
#    operacao e inc devem-se manter