def reconhece(caracteres):
    pas, n, l = 0, ('1', '2', '3', '4'), ('A', 'B', 'C', 'D')
    for i in caracteres:
        if i in n:
            pas = 1
        if i not in l and pas==0:
            return False
        if i not in n and pas==1:
            return False
    return True
             
        
if __name__ == '__main__':
    caracteres = input()
    print(reconhece(caracteres))