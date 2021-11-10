def eh_primo(n):
    if n == 1:
        return False
    else:
        for i in range(2, n):
            if n % i == 0:
                return False
        return True

def nao_primos(n):
    return list(filter(lambda x: not eh_primo(x), list(range(1,n))))


if __name__=='__main__':
    print(nao_primos(10))