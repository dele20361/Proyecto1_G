import random as rand
import math_lib as ml

import random as rand
from gl import *
        
def flat(render, **kwargs):
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = [-render.dirLight [0],
                -render.dirLight [1],
                -render.dirLight [2]]
    intensity = ml.dotProduct(triangleNormal, dirLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def gourad(render, **kwargs):
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w
    
    dirLight = [-render.dirLight [0],
                -render.dirLight [1],
                -render.dirLight [2]]

    triangleNormal = (nx, ny, nz)


    intensity = ml.dotProduct(triangleNormal, dirLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def powr(render, **kwargs):
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w
    
    dirLight = [-render.dirLight [0],
                -render.dirLight [1],
                -render.dirLight [2]]

    triangleNormal = (nx, ny, nz)


    intensity = ml.dotProduct(triangleNormal, dirLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return round(r, 1), round(g, 1), round(b, 1)
    else:
        return 0,0,0

def colrs(render, **kwargs):
    # Normal calculada por vertice
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w
    
    dirLight = [-render.dirLight [0],
                -render.dirLight [1],
                -render.dirLight [2]]

    triangleNormal = (nx, ny, nz)


    intensity = ml.dotProduct(triangleNormal, dirLight)

    colrs= rand.randint(0, 2)

    b *= intensity if colrs == 0 else 0
    g *= intensity if colrs == 1 else 0
    r *= intensity if colrs == 2 else 0

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def normalMap(render, **kwargs):
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    nA, nB, nC = kwargs["normals"]
    tangente = kwargs["tangente"]
    bitangente = kwargs["bitangente"]

    b /= 255
    g /= 255
    r /= 255

    tU = tA[0] * u + tB[0] * v + tC[0] * w
    tV = tA[1] * u + tB[1] * v + tC[1] * w

    if render.active_texture:
        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    nx = nA[0] * u + nB[0] * v + nC[0] * w
    ny = nA[1] * u + nB[1] * v + nC[1] * w
    nz = nA[2] * u + nB[2] * v + nC[2] * w
    
    dirLight = [-render.dirLight [0],
                -render.dirLight [1],
                -render.dirLight [2]]

    triangleNormal = (nx, ny, nz)

    if render.normal_map:
        texNormal = render.normal_map.getColor(tU, tV)
        texNormal = [texNormal[0] * 2 - 1,
                        texNormal[1] * 2 - 1,
                        texNormal[2] * 2 - 1]

        texNormal2 =[]
        for i in range(len(texNormal)):
            norm = texNormal[i] / ml.normalize(texNormal)
            texNormal2.append(norm)
        texNormal = texNormal2

        tanM = [tangente[0],bitangente[0],triangleNormal[0],tangente[1],bitangente[1],triangleNormal[1],tangente[2],bitangente[2],triangleNormal[2]]
        tangentMatrix = ml.defineMatrix(3,3,tanM)

        texNormal = ml.matrixMultiplication(tangentMatrix,texNormal)

        texNormal1 =[]
        for i in range(len(texNormal)):
            norm = texNormal[i] / ml.normalize(texNormal)
            texNormal1.append(norm)
        texNormal = texNormal1

        intensity = ml.dotProduct(texNormal, dirLight)
    else:
        intensity = ml.dotProduct(triangleNormal, dirLight)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0