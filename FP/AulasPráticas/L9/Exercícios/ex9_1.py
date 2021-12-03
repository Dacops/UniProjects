def apenas_digitos_impares(n):
    if n==0:
        return 0
    if n%2!=0:
        return apenas_digitos_impares(n//10)*10+n%10
    else:
        return apenas_digitos_impares(n//10)

if __name__=='__main__':
    print(apenas_digitos_impares(12345))


"""
>fun(12345) = fun(1234)*10 + 5
>fun(1234) = fun(123)
>fun(123) = fun(12)*10 + 3
>fun(12) = fun(1)
>fun(1) = fun(0)*10 + 1
>fun(0) = 0

>fun(1) = 0*10 + 1 = 1
>fun(12) = 1
>fun(123) = 1*10 + 3 = 13
>fun(1234) = 13
>fun (12345) = 13*10 + 5 = 135
"""