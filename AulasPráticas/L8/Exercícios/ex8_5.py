def procura(caracteres, ficheiro):
    f = open(ficheiro, 'r')
    l = f.readlines()
    linhas = ''
    for linha in l:
        l2 = linha
        for palavra in l2.split():
            if palavra==caracteres:
                linhas+=linha
    return linhas


if __name__=='__main__':
    print(procura('ficheiro', 'C:\\Users\\david\\OneDrive\\Desktop\\Uni\\Fprog\\AulasPráticas\\L8\\Ficheiros\\read.txt'))