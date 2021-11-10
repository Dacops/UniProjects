def junta_ordenadas(l1, l2):
    if len(l1)==0:
        return l2
    if len(l2)==0:
        return l1
    else:
        if l1[-1]>l2[-1]:
            return junta_ordenadas(l1[:-1], l2)+[l1[-1], ]
        else:
            return junta_ordenadas(l1, l2[:-1])+[l2[-1], ]
                

if __name__=='__main__':
    print(junta_ordenadas([2, 5, 90], [3, 5, 6, 12]))