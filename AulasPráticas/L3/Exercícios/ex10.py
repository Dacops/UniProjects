def misterio(n):

    if abs(n%10 - n//100) < 1:
        print(''' 'Condições não verificadas' ''')
       
    else:
        def troca(n):
            ni, ns, count, algarismo = 0, 0, 1, 0
            while count!=4:

                algarismo = ((n%10**count)-algarismo)

                while algarismo > 10:
                    algarismo //= 10

                ni = ni + (algarismo*(10**(3-count)))
                count += 1
            return ni

        ni = troca(n)
        ns = abs(n-ni)
        nsi = troca(ns)
        return ns + nsi
    

if __name__ == '__main__':
    n = eval(input())
    print(misterio(n))
    
    