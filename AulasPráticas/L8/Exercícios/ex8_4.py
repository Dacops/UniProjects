def concatena(r, w):
    saida = []
    for ficheiro in r:
        l = ficheiro.readlines()
        saida+=l
        saida[-1]=saida[-1]+'\n'

    l = w.readlines()
    saida.append(l)
    
    for linha in saida:
        w.writelines(linha)
    
    s = w.readlines()
    return s


if __name__=='__main__':
    r1 = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//read.txt", "r")
    r2 = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//read2.txt", "r")
    w = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//write.txt", "r+")
    r = [r1, r2]
    print(concatena(r, w))