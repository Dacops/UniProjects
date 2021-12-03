def dia_da_semana(q, m, a):

    meses = ('Sábado', 'Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira')
    if m==1:
        m, a = 13, a-1
    if m==2:
        m, a = 14, a-1

    K, J= a%100, int(a/100)
    h = (q+int((13*(m+1))/5)+K+int(K/4)+int(J/4)-2*J)%7

    return meses[h]


if __name__ == '__main__':
    q, m, a = input().split()
    q, m, a = eval(q), eval(m), eval(a)
    print(dia_da_semana(q, m, a))
    