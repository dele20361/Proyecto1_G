
import struct
from obj import Obj
import math as math
import math_lib as ml
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])


def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

# function to set colors 
def color(r, g, b):
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)] )

def baryCoords(A, B, C, P): 
    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w

class Renderer(object):

    # Define size of the screen 
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.clearColor = color(0.5,0.5,0.5)
        self.currColor = color(1,1,1)

        self.active_shader = None
        self.active_texture = None
        self.active_texture2 = None

        self.background = None
        
        #Light 
        self.dirLight = V3(0,0,-1)
        
        self.glViewMatrix()
        self.glViewport(0,0,self.width, self.height)
        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height
        
        VPM = [width/2,0,0,posX+width/2,0,height/2,0,posY+height/2,0,0,0.5,0.5,0,0,0,1]

        self.viewportMatrix = ml.defineMatrix(4,4, VPM)
        self.glProjectionMatrix()

    def glViewMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0)):
        self.camMatrix = self.glCreateObjectMatrix(translate, rotate)
        self.viewMatrix = ml.getMatrixInverse(self.camMatrix)


    def glLookAt(self, eye, camPosition = V3(0,0,0)):
        forward = ml.subtract(camPosition, eye)

        forward1 =[]
        for i in range(len(forward)):
            norm = forward[i] / ml.normalize(forward)
            forward1.append(norm)
        
        forward = forward1

        right = ml.cross(V3(0,1,0), forward)

        right1 =[]
        for i in range(len(right)):
            norm = right[i] / ml.normalize(right)
            right1.append(norm)
        
        right = right1

        up = ml.cross(forward, right)

        up1 =[]
        for i in range(len(up)):
            norm = up[i] / ml.normalize(up)
            up1.append(norm)

        up = up1
        
        CM = [right[0],up[0],forward[0],camPosition[0],right[1],up[1],forward[1],camPosition[1],right[2],up[2],forward[2],camPosition[2], 0,0,0,1]
        self.camMatrix = ml.defineMatrix(4,4,CM)

        self.viewMatrix = ml.getMatrixInverse(self.camMatrix)

    def glProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):
        aspectRatio = self.vpWidth / self.vpHeight
        t = math.tan( (fov * math.pi / 180) / 2) * n
        r = t * aspectRatio

        PM = [n/r,0,0,0,0,n/t,0,0,0,0,-(f+n)/(f-n),-(2*f*n)/(f-n),0,0,-1,0]
        self.projectionMatrix = ml.defineMatrix(4,4,PM)


    #Determinate the background color & array of pixels
    def glClear(self):
        self.pixels = [[ self.clearColor 
                         for y in range(self.height)] # por cada y en el ancho se le agrega el color definido 
                         for x in range(self.width)] # por cada x en el largo se le agrega el color definido

        self.zbuffer = [[ float('inf') 
                          for y in range(self.height)]
                          for x in range(self.width)]
    def glClearBackground(self):
            if self.background:
                for x in range(self.vpX, self.vpX + self.vpWidth + 1):
                    for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                        
                        tU = (x - self.vpX) / self.vpWidth
                        tV = (y - self.vpY) / self.vpHeight

                        texColor = self.background.getColor(tU, tV)

                        if texColor:
                            self.glPoint(x,y, color(texColor[0], texColor[1], texColor[2]))

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)

     # HOW TO MAKE POINTS 
    def glPoint(self, x, y, clr = None): 
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    #HOW TO MAKE LINES 
    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorithm
        # y = m * x + b
        x0 = int(v0.x)
        x1 = int(v1.x)
        y0 = int(v0.y)
        y1 = int(v1.y)

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0,clr)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        #Inclinacion de una linea 
        steep = dy > dx

        #Invierto las lineas (Dibujo vertical y no horizontal)
        #Slope is bigger than 1 so I change it 
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        #Draw left to right 
        #Initial dot is bigger than final dot I change the values      
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        
        #Need to redifine because I change the invert the values 
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.5 #Represents the middle of a pixel # Este puede cambiar de acuerdo a nuestras necesidades, pero se recomienda usar .5
        m = dy / dx
        y = y0

        for x in range(x0, x1 + 1):
            #Draw de manera vertical
            if steep:
                self.glPoint(y, x, clr)

            #Draw de manera horizontal 
            else:
                self.glPoint(x, y, clr)

            offset += m

            if offset >= limit:
                if y0 < y1: #I am going down to up (well the line)
                    y += 1
                else: # The line is been drawing up to down
                    y -= 1
                
                limit += 1

    #Function to create matrix 
    def glCreateObjectMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):

        #Data of the matrix 
        TM = [1, 0, 0, translate.x, 0, 1, 0, translate.y, 0, 0, 1, translate.z, 0, 0, 0, 1]
        SM = [scale.x, 0, 0, 0, 0, scale.y, 0, 0, 0, 0, scale.z, 0, 0, 0, 0, 1]
        RM = [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]

        #Create Matrix 
        translation = ml.defineMatrix(4,4, TM)
        scales = ml.defineMatrix(4,4, SM)
        rotation = self.glRotationMatrix(rotate.x, rotate.y, rotate.z)

        #Multiplication of matrix 
        Matrix_init = ml.matrixMultiplication(translation, rotation)
        Matrix_final = ml.matrixMultiplication(Matrix_init, scales)

        return Matrix_final

    def glTransform(self, vertex, matrix):
        #Vector 
        v = (vertex[0], vertex[1], vertex[2], 1)
        
        #Multiplication of matrix and vector 
        vt = ml.multiplyVectorMatrix(matrix, v)

        vf = V3(vt[0] / vt[3],
                vt[1] / vt[3],
                vt[2] / vt[3])

        return vf

    def glRotationMatrix(self, pitch = 0, yaw = 0, roll = 0):
        
        pitch *= math.pi/180
        yaw   *= math.pi/180
        roll  *= math.pi/180

        pM = [1, 0, 0, 0, 0, math.cos(pitch),-math.sin(pitch), 0 ,0, math.sin(pitch), math.cos(pitch), 0 ,0, 0, 0, 1]
        yM = [math.cos(yaw), 0, math.sin(yaw), 0, 0, 1, 0, 0,-math.sin(yaw), 0, math.cos(yaw), 0, 0, 0, 0, 1]
        rM = [math.cos(roll),-math.sin(roll), 0, 0, math.sin(roll), math.cos(roll), 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]

        pitchMat = ml.defineMatrix(4,4, pM)
        yawMat = ml.defineMatrix(4,4, yM)
        rollMat =ml.defineMatrix(4,4, rM)

        #Multiplication of matrix 
        Matrix_i = ml.matrixMultiplication(pitchMat, yawMat)
        Matrix_f = ml.matrixMultiplication(Matrix_i, rollMat)

        return Matrix_f

    def glTransform(self, vertex, matrix):
        v = V4(vertex[0], vertex[1], vertex[2], 1)
        vt = ml.multiplyVectorMatrix(matrix ,v)
      
        vf = V3(vt[0] / vt[3],
                vt[1] / vt[3],
                vt[2] / vt[3])

        return vf

    def glDirTransform(self, dirVector, rotMatrix):
        v = V4(dirVector[0], dirVector[1], dirVector[2], 0)
        vt = ml.multiplyVectorMatrix(rotMatrix,v)
        
        vf = V3(vt[0],
                vt[1],
                vt[2])

        return vf

    def glCamTransform(self, vertex):
        v = V4(vertex[0], vertex[1], vertex[2], 1)
        vt1 = ml.matrixMultiplication(self.viewportMatrix,self.projectionMatrix)
        vt2 = ml.matrixMultiplication(vt1,self.viewMatrix)
        vt = ml.multiplyVectorMatrix(vt2,v)
  
        vf = V3(vt[0] / vt[3],
                vt[1] / vt[3],
                vt[2] / vt[3])

        return vf


    #GENERATE OBJ 
    def glLoadModel(self, filename, translate = V3(0,0,0), rotate = V3(0,0,0), scale = V3(1,1,1)):
        #Open file 
        model = Obj(filename)
        modelMatrix = self.glCreateObjectMatrix(translate, rotate, scale)
        rotationMatrix = self.glRotationMatrix(rotate[0], rotate[1], rotate[2])

        for face in model.faces:
            vertCount = len(face)

            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]

            v0 = self.glTransform(v0, modelMatrix)
            v1 = self.glTransform(v1, modelMatrix)
            v2 = self.glTransform(v2, modelMatrix)
 
            A = self.glCamTransform(v0)
            B = self.glCamTransform(v1)
            C = self.glCamTransform(v2)

            #We add this so if we have saquares the will be also fill 
            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]

            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]

            vn0 = self.glDirTransform(vn0, rotationMatrix)
            vn1 = self.glDirTransform(vn1, rotationMatrix)
            vn2 = self.glDirTransform(vn2, rotationMatrix)

            self.glTriangle_bc(A,B,C, verts=(v0, v1, v2), texCoords = (vt0, vt1, vt2), normals = (vn0, vn1, vn2))

            #Squares filling 
            if vertCount == 4:
                v3 = model.vertices[ face[3][0] - 1]
                v3 = self.glTransform(v3, modelMatrix)
                D = self.glCamTransform(v3)
                vt3 = model.texcoords[face[3][1] - 1]
                vn3 = model.normals[face[3][2] - 1]
                vn3 = self.glDirTransform(vn3, rotationMatrix)

                self.glTriangle_bc(A, C, D,
                                   verts=(v0, v2, v3),
                                   texCoords = (vt0, vt2, vt3),
                                   normals = (vn0, vn2, vn3))

    #Fill a poligon base on triagles 
    def glTriangle_std(self, A, B, C, clr = None):
        
        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        self.glLine(A,B, clr)
        self.glLine(B,C, clr)
        self.glLine(C,A, clr)

        def flatBottom(vA,vB,vC):
            try:
                mBA = (vB.x - vA.x) / (vB.y - vA.y)
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
            except:
                pass
            else:
                x0 = vB.x
                x1 = vC.x
                for y in range(int(vB.y), int(vA.y)):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 += mBA
                    x1 += mCA

        def flatTop(vA,vB,vC):
            try:
                mCA = (vC.x - vA.x) / (vC.y - vA.y)
                mCB = (vC.x - vB.x) / (vC.y - vB.y)
            except:
                pass
            else:
                x0 = vA.x
                x1 = vB.x
                for y in range(int(vA.y), int(vC.y), -1):
                    self.glLine(V2(x0, y), V2(x1, y), clr)
                    x0 -= mCA
                    x1 -= mCB

        if B.y == C.y:
            # Flat bottom 
            flatBottom(A,B,C)
        elif A.y == B.y:
            # Flat top
            flatTop(A,B,C)
        else:
            # Two types of triagnles. I use the intercept teorem 
            D = V2( A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x), B.y)
            flatBottom(A,B,D)
            flatTop(B,D,C)

    def glTriangle_bc(self, A, B, C, verts=(),texCoords = (), normals = (), clr = None):
        # bounding box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y)) 
        
        edge1 = ml.subtract(verts[1], verts[0])
        edge2 = ml.subtract(verts[2], verts[0])

        triangleNormal = ml.cross( edge1, edge2)
        
        # normalizar
        triangleNormal1 =[]
        for i in range(len(triangleNormal)):
            norm = triangleNormal[i] / ml.normalize(triangleNormal)
            triangleNormal1.append(norm)
        
        #gives the vector normalized to the original 
        triangleNormal = triangleNormal1

       
        deltaUV1 = ml.subtract(texCoords[1], texCoords[0])
        deltaUV2 = ml.subtract(texCoords[2], texCoords[0])
       
        deltadiv = (deltaUV1[0] * deltaUV2[1] - deltaUV2 [0] * deltaUV1[1])
        
        if (deltadiv == 0):
            deltadiv = 0 
        else: 
            global f
            f = 1 / deltadiv
        

        tangente = [f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0]),
                    f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1]),
                    f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])]

        # normalizar
        tan =[]
        for i in range(len(tangente)):
            try:
                norm = tangente[i] / ml.normalize(tangente)
                tan.append(norm)
                
            except ZeroDivisionError:
                norm = 0
        tangente = tan

        bitangente = ml.cross2(triangleNormal, tangente)

        #Normalizar
        btan =[]
        for i in range(len(bitangente)):
            norm = bitangente[i] / ml.normalize(bitangente)
            btan.append(norm)
        
        #gives the vector normalized to the original 
        tangente = tan

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, V2(x, y))

                if 0<=u and 0<=v and 0<=w:

                    z = A.z * u + B.z * v + C.z * w

                    if 0<=x<self.width and 0<=y<self.height:
                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z

                            if self.active_shader:
                                r, g, b = self.active_shader(self, 
                                                             baryCoords=(u,v,w), 
                                                             vColor = clr or self.currColor,
                                                             texCoords = texCoords, 
                                                             normals = normals,
                                                             triangleNormal = triangleNormal,
                                                             tangente = tangente,
                                                             bitangente = bitangente)



                                self.glPoint(x, y, color(r,g,b))
                            else:
                                self.glPoint(x,y, clr)


    #Function to define image 
    def glFinish(self, filename):
        with open(filename, "wb") as file:
             #HEADER (STEP 1) default BM size(14 bytes)
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))

            #offset 40 bytes + header 14 bytes and color w * h * 3(de bytes)
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

           #INFO HEADER (SETP 2) size(40 bytes)
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))

             #Entre mas color quiera debo de aumentar el bits per pixel 
            file.write(word(24))
            file.write(dword(0)) #compression
            file.write(dword(self.width * self.height * 3)) #size of the screen
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #COLOR TABLE 
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])
