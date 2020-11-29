def cross(a, b):
       c = [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]
       return c

def substractV3(a, b):
       c = [a[0]-b[0],
            a[1]-b[1],
            a[2]-b[2]]
       return c

def root(x,a):
    y = 1 / a
    y = float(y)
    z = x ** y
    return z

def normV3(a):
    c = root(float(a[0]**2)+(a[1]**2)+(a[2]**2), 2)
    return c

def dotV3(a, b):
    c = a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    return c

def deg2rad(a):
    a = (a * 3.14159165) / 180
    return a

def matrixmul(a, b):
    c=[]
    for i in range(len(a)):
        c.append([0]*len(b[0]))

    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                c[i][j] += a[i][k]*b[k][j]

    return c

def VecMatriz(a,b):
    c=[]
    for i in range(len(a)):
        c.append(0)
    for i in range(len(a)):
        for k in range(len(a[0])):
            c[i] += a[i][k]*b[k]
    return c

#Codigo para hacer el inverso de una matriz obtenido de:
#https://www.it-swarm.dev/es/python/inversion-matricial-sin-numpy/1054196902/
def transpuesta(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = list(transpuesta(cofactors))
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
