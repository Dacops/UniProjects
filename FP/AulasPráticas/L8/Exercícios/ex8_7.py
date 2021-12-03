def ordena(fich):
    f = open(fich, 'r')
    l = f.readlines()

    anterior, li, r = None, '', ''
    for linha in l:
        if anterior == None:
            anterior, li = ord(linha[0]), linha
        else:
            if anterior>ord(linha[0]):
                r += linha+li
            else:
                r+= linha
    return r


if __name__=='__main__':
    print(ordena('C:\\Users\\david\\OneDrive\\Desktop\\Uni\\Fprog\\AulasPráticas\\L8\\Ficheiros\\read.txt'))