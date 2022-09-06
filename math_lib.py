# Librería de matemáticas
# Paola De León

from math import sin

# Matriz de indentidad
def identidad(num):
    identity = []
    iPos = 1
    for i in range(num*num):
        row = []
        if len(identity)%num != 0:
            if (iPos%num) == 0:
                row.append(1)
            else:
                row.append(0)
            iPos = iPos + 1
        else:
            identity.append(row)
            row = []

    return identity


def matrixMultiplication (A, B):
    '''
        Multiplicación de matrices
            m1: Primera matriz
            m2: Segunda matriz
            res: Matriz resultante
    '''
    result = [[(sum(a * b for a, b in zip(B_row, A_col)))
                            for A_col in zip(*B)]
                                for B_row in A]
    return result

def cross2(a, b):
    c=[]
    for c in range(len(a), len(b)):
        c = [a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]]

    return c

def defineMatrix (rowCount, colCount, dataList):
    '''
        Función para definir una matriz.
            rowCount: Cantidad de filas
            colCount: Cantidad de columnas
            dataList: Lista con los datos.
            mat: Matriz resultante.
    '''
    mat = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            rowList.append(dataList[rowCount * i + j])
        mat.append(rowList)

    return mat

def multiplyVectorMatrix(M, v):
    '''
        Función para mutiplicar un vector por una matriz.
            v: Vector
            M: Matriz como una lista de list.
            result: Matriz resultante.
    '''
    # Comprobar que se pueda multiplicar
    if len(M[0]) != len(v):
        # No se puede multiplicar
        return None
    res = []

    # Si se puede multiplicar
    for i in range(len(M)):
        suma = 0
        for j in range(len(M[0])):
            # print("M[i][j] ", M[i][j])
            # print("v[j] ", v[j])
            suma += M[i][j]*v[j]
        res.append(suma)

    return res

def cross(a, b):
    '''
        Producto cruz de 2 vectores
        result: Vector resultante
    '''
    x, y, z = 0, 1, 2
    return [(a[y]*b[z]) - (a[z]*b[y]),
            (a[z]*b[x]) - (a[x]*b[z]),
            (a[x]*b[y]) - (a[y]*b[x])]

def subtract(a, b):
    return [a[i] - b[i] for i in range(min(len(a), len(b)))]

def normalize(a):
    return ( ( (a[0])**2) + ((a[1])**2) + ((a[2])**2 ) )**0.5

def dotProduct(a,b):
    return sum(x*y for x, y in zip(a, b))

######################################################################################################
# Inverso de una matriz
# Tomado de https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    cofactors = list(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant

    return cofactors

    ######################################################################################################