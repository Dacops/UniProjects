def maior(lst):
    if len(lst)==1:
        return lst[0]
    if lst[0]>lst[1]:
        lst[0], lst[1] = lst[1], lst[0]
        return maior(lst[1:])
    else:
        return maior(lst[1:])

    
if __name__=='__main__':
    print(maior([5, 3, 8, 1, 9, 2]))