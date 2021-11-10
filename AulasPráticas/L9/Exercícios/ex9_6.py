def inverte(lst):
    if len(lst)==0:
        return []
    else:
        return inverte(lst[1:]) + [lst[0], ]


if __name__=='__main__':
    print(inverte([9, 7, 4, 3]))