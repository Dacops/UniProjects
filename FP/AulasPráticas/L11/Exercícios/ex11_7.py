# a) Esta funcao recebe um numero natural 'n' e uma funcao 'p', se 'num%10', ou seja a ultima casa do numero 'n'
#    ao ser inserida como argumento na funcao p der return de True eh devolvido esse numero e a funcao chamada outra
#    vez. Se este caso se repetir a casa devolvida eh multiplicada por 10, ocupando no output final a casa ah esquerda
#    da casa anterior. No caso de der return False apenas eh chamada a mesma funcao sem essa casa. Indo reduzindo o 
#    numero, quando chegar a 0 eh devolvido 0 e assim, atraves de uma recursao linear eh nos devolvido o resultado.

def misterio(num, p):
    if num == 0:
        return 0
    elif p(num % 10):
        return num % 10 + 10 * misterio(num // 10, p)
    else:
        return misterio(num // 10, p)

def filtra_pares(n):
    return misterio(n, lambda x:True if x%2==0 else False)

if __name__=='__main__':
    print(filtra_pares(5467829))