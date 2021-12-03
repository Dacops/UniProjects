def inverte(r,w):
    l=r.readlines()
    l[-1]=l[-1]+'\n'
    l=l[::-1]
    w.writelines(l)
    l=w.readlines()
    return l

if __name__=='__main__':
    r = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//read.txt", "r")
    w = open("C://Users//david//OneDrive//Desktop//Uni//Fprog//AulasPráticas//L8//Ficheiros//write.txt", "r")
    print(inverte(r,w))