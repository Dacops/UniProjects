def metabolismo(d):
    for pessoa in d:
        if d[pessoa][0]=='M':
            d[pessoa] = 66 + 6.3*d[pessoa][3] + 12.9*d[pessoa][2] + 6.8*d[pessoa][1]
        else:
            d[pessoa] = 655 + 4.3*d[pessoa][3] + 4.7*d[pessoa][2] + 4.7*d[pessoa][1]
    return d

if __name__ == '__main__':
    d = {'Maria' : ('F', 34, 1.65, 64), 'Pedro': ('M', 34, 1.65, 64), 'Ana': ('F', 54, 1.65, 120), 'Hugo': ('M', 12, 1.82, 75)}
    print(metabolismo(d))
