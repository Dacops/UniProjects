def soma_digito(n):
    if n//10==0:
        return n
    else:
        return n%10+soma_digito(n//10)

def soma_digitos_tuplo(n):
    if len(n)==1:
        return n[0]
    else:
        return n[-1]+soma_digitos_tuplo(n[:-1])       

def factorial(n):
    if n==1:
        return 1
    else:
        return n*factorial(n-1)

def soma_prog_aritmetica(n):
    if n==1:
        return 1
    else:
        return n+soma_prog_aritmetica(n-1)


