def linhas_ficheiro(f):
    l = f.readlines()
    return len(l)

if __name__=='__main__':
    f = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//read.txt", "r")
    print(linhas_ficheiro(f))