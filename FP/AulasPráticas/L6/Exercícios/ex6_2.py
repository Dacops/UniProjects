def agrupa_por_chave(lst):
    dic = {}
    for tup in lst:
        if tup[0] not in dic:
            dic[tup[0]] = 1
        else:
            dic[tup[0]] +=  1 
    return dic

print(agrupa_por_chave([('a', 8), ('b', 9), ('a', 3)]))


