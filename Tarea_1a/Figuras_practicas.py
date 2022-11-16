import numpy as np
from OpenGL.GL import *

SIZE_IN_BYTES = 4

# yo quiero que mi logo diga DCC, y que abajo haya un cuadrado
# es mejor una C como dos circulos super puestos
# la D será una C con un rectangulo unido
# todos otros problemas se resuelven con transformaciones

class Figura:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData

def Cuadrilatero(r,g,b):

    vertexData = np.array([
    #   pos             color
        -0.2, -0.2, 0.0,  r, g, b,
         0.2, -0.2, 0.0,  r, g, b,
         0.2,  0.2, 0.0,  r, g, b,
        -0.2,  0.2, 0.0,  r, g, b
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2, 
        2, 3, 0], dtype = np.uint32)
    
    return Figura(vertexData, indexData)

def Letra_C(N, r, g, b):
    
    vertexData = [
    #   pos            color
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    indexData = []

    dtheta = 2* np.pi /N

    R = 0.5
    for i in range(N//2+1):
        theta = i* dtheta

        x = R * np.cos(theta)
        y = R * np.sin(theta)
        z = 0

        vertexData += [
        #   pos      color
            x, y, z, r, g, b
        ]        

        indexData += [0,i ,i+1]
    
    R = 0.25
    for j in range(N//2,N+2):
        theta = -j*dtheta
            
        x = R * np.cos(theta)
        y = R * np.sin(theta)
        z = 0

        vertexData += [
        #   pos      color
            x, y, z, 0.0, 0.0, 0.0
        ]        

        indexData += [0,j ,j+1]
    indexData += [0,N+2,N//2+1]

    return Figura(vertexData, indexData)

def Rectangulo(r,g,b):
    # que el origen sea negro es 100% estetico
    vertexData = [
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    vertexData += [
        -0.5, -0.25, 0.0,  r, g, b]
    vertexData += [
         0.5, -0.25, 0.0,  r, g, b]
    vertexData += [
         0.5, 0.0, 0.0,  r, g, b]
    vertexData += [
        -0.5, 0.0, 0.0,  r, g, b]            
    
    indexData = []
    indexData += [0,4,1,0,1,2,0,2,3,0]

    return Figura(vertexData, indexData)