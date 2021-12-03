def conta_vogais(f):
    l = f.readlines()
    vogais = {'a':0, 'e':0, 'i':0, 'o':0, 'u':0}
    for linha in l:
        for caractere in linha:
            if caractere in vogais:
                vogais[caractere]+=1
    return vogais

if __name__=='__main__':
    f = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//read.txt", "r")
    print(conta_vogais(f))
