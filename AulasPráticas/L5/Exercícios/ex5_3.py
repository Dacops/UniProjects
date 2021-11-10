def soma_cumulativa(lista):
    soma, final = 0, []
    for i in lista:
        soma += i
        final.append(soma)
    return final


if __name__ == '__main__':
    lista = eval(input())
    print(soma_cumulativa(lista))