def subtrai(lst1, lst2):
    if not lst1:
        return []
    else:
        if lst1[0] in lst2:
            return subtrai(lst1[1:], lst2)
        else:
            return [lst1[0], ] + subtrai(lst1[1:], lst2)



if __name__=='__main__':
    print(subtrai([2, 3, 4, 5], [2, 3]))
    print(subtrai([2, 3, 4, 5], [6, 7]))