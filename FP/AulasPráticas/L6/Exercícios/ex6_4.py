def resumo_FP(notas_dict):
    chumbo, count, valor = 0, 0, 0
    for i in range(21):
        if i in notas_dict:
            if i<10:
                chumbo += len(notas_dict[i])
            else:
                count += len(notas_dict[i])
                valor += len(notas_dict[i])*i
    return(valor/count, chumbo)


notas_dict = {1 : [46592, 49212, 90300, 59312], 15 : [52592, 59212], 20 : [58323]}
print(resumo_FP(notas_dict))