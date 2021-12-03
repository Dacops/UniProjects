def pertence(lst, n):
    if not lst:
        return False
    else:
        if lst[0]==n:
            return True
        else:
            return pertence(lst[1:], n)


if __name__=='__main__':
    print(pertence([3, 4, 5], 2))
    print(pertence([3, 4, 5], 5))