def troco(euros):
    a, b, c, d, e, f, g, h, i, j, k, l = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    
    if (euros//50) != 0:
        a += (euros//50)
        euros -= (50*a)

    if (euros//20) != 0:
        b += (euros//20)
        euros -= (20*b)

    if (euros//10) != 0:
        c += (euros//10)
        euros -= (10*c)

    if (euros//5) != 0:
        d += (euros//5)
        euros -= (5*d)

    if (euros//2) != 0:
        e += (euros//2)
        euros -= (2*e)

    if (euros//1) != 0:
        f += (euros//1)
        euros -= (1*f)

    if (euros//.50) != 0:
        g += (euros//.50)
        euros -= (.50*g)

    if (euros//.20) != 0:
        h += (euros//.20)
        euros -= (.20*h)
    
    if (euros//.10) != 0:
        i += (euros//.10)
        euros -= (.10*i)

    if (euros//0.05) != 0:
        j += (euros//0.05)
        euros -= (0.05*j)

    if (euros//0.02) != 0:
        k += (euros//0.02)
        euros -= (0.02*k)

    if (euros//0.01) != 0:
        l += (euros//0.01)
        euros -= (0.01*l)
    
    print('Notas de 50€: ', int(a),
          '\nNotas de 20€: ', int(b),
          '\nNotas de 10€: ', int(c),
          '\nNotas de 5€: ', int(d),
          '\nMoedas de 2€: ', int(e),
          '\nMoedas de 1€: ', int(f),
          '\nMoedas de 0.50€: ', int(g),
          '\nMoedas de 0.20€: ', int(h),
          '\nMoedas de 0.10€: ', int(i),
          '\nMoedas de 0.05€: ', int(j),
          '\nMoedas de 0.02€: ', int(k),
          '\nMoedas de 0.01€: ', int(l),)

euros = float(input())
troco(euros)