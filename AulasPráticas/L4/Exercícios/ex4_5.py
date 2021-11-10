import ex4_2
import ex4_3
import ex4_4

def algarismos_pares(n):
    return ex4_3.implode(ex4_4.filtra_pares(ex4_2.explode(n)))


if __name__ == '__main__':
    n = eval(input())
    print(algarismos_pares(n))