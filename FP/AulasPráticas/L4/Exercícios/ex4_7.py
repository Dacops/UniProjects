def amigas(f1, f2):
    if len(f1) != len(f2):
        return False 

    count = 0
    for i in range(len(f1)):
        if f1[i]==f2[i]:
            count += 1
    
    if count/len(f1) < 0.9:
        return False 
    return True

if __name__ == '__main__':
    f1, f2 = input().split()
    f1, f2 = str(f1), str(f2)
    print(amigas(f1, f2))