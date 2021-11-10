def lista_codigos(caracteres):
    unicode = []
    for i in caracteres:
        unicode.append(ord(i))
    return unicode

if __name__ == '__main__':
    caracteres = input()
    print(lista_codigos(caracteres))