def remove_multiplos(lista, n):
    copia = lista.copy()
    for i in copia:
        print(copia, i)
        if i%n==0:
            lista.remove(i)
    return lista


if __name__ == '__main__':
    lista, n = eval(input())
    print(remove_multiplos(lista, n))