def sublistas(lst):
    if not lst:
        return 0
    else:
        if type(lst[0])==list:
            return sublistas(lst[0]+lst[1:])+1
        else:
            return sublistas(lst[1:])


if __name__=='__main__':
    print(sublistas([[1], 2, [3]]))
    print(sublistas([[[[[1]]]]]))
    print(sublistas(['a', [2, 3, [[[1]], 6, 7], 'b']]))