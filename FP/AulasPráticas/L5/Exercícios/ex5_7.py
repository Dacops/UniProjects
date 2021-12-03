import ex5_5

def multiplica_mat(m1, m2):
    m_t1, m_t2, m_t3, count = [], [], [], 0
    for v in range(len(m1)):
        for n_lin in range(len(m1)):
            m = []
            for n_col in range(len(m1)):
                m.append(m1[n_col][n_lin]*m2[n_lin][v])

            if count%3==0:
                m_t1.append(m)
            if (count-1)%3==0:
                m_t2.append(m)
            if (count-2)%3==0:
                m_t3.append(m)

            count+=1
    return m_t1, m_t2, m_t3
    
 

    




if __name__ == '__main__':
    m1, m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(multiplica_mat(m1, m2))