# coding=utf-8
"""
Vertices and indices for a variety of simple shapes.
"""

__all__ = [
    'applyOffset',
    'createAxis',
    'createColorCircle',
    'createColorConeOFF',
    'createColorCube',
    'createColorCubeOFF',
    'createColorCylinderOFF',
    'createColorNormalsCube',
    'createColorQuad',
    'createColorSphereOFF',
    'createFacetedCube',
    'createRainbowCircle',
    'createRainbowCube',
    'createRainbowNormalsCube',
    'createRainbowQuad',
    'createRainbowTriangle',
    'createTextureCube',
    'createTextureNormalsCube',
    'createTextureQuad',
    'createTextureQuadWithNormal',
    'merge',
    'readOFF',
    'scaleVertices',
    'Shape'
]

import math
import numpy as np
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from assets_path import getAssetPath

__author__ = "Daniel Calderon"
__license__ = "MIT"

################################################# CAMBIOS EN EL ARCHIVO QUE HICE YO ################################################################
# AÑADI A SHAPES la propiedad image_filename
# FUNCION createTextureTri(nx, ny)
# FUNCION createTextureTriangle(image_filename)
# FUNCION Esfera2(r,lats,longs,red,g,b)
####################################################################################################################################################

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices, image_filename = None):
        self.vertices = vertices
        self.indices = indices
        self.image_filename = image_filename # PARA RECIBIR TEXTURAS

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n" \
                                                   "indices: " + str(self.indices)


def merge(destinationShape, strideSize, sourceShape):
    # current vertices are an offset for indices refering to vertices of the new shape
    offset = len(destinationShape.vertices)
    destinationShape.vertices += sourceShape.vertices
    destinationShape.indices += [(offset / strideSize) + index for index in sourceShape.indices]


def applyOffset(shape, stride, offset):
    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index] += offset[0]
        shape.vertices[index + 1] += offset[1]
        shape.vertices[index + 2] += offset[2]


def scaleVertices(shape, stride, scaleFactor):
    numberOfVertices = len(shape.vertices) // stride

    for i in range(numberOfVertices):
        index = i * stride
        shape.vertices[index] *= scaleFactor[0]
        shape.vertices[index + 1] *= scaleFactor[1]
        shape.vertices[index + 2] *= scaleFactor[2]


def createAxis(length=1.0):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -length, 0.0, 0.0, 0.0, 0.0, 0.0,
        length, 0.0, 0.0, 1.0, 0.0, 0.0,

        0.0, -length, 0.0, 0.0, 0.0, 0.0,
        0.0, length, 0.0, 0.0, 1.0, 0.0,

        0.0, 0.0, -length, 0.0, 0.0, 0.0,
        0.0, 0.0, length, 0.0, 0.0, 1.0]

    # This shape is meant to be drawn with GL_LINES,
    # i.e. every 2 indices, we have 1 line.
    indices = [
        0, 1,
        2, 3,
        4, 5]

    return Shape(vertices, indices)


def createRainbowTriangle():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.0, 0.5, 0.0, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2]

    return Shape(vertices, indices)


def createRainbowQuad():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.0, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createColorQuad(r, g, b):
    # Defining locations and colors for each vertex of the shape
    vertices = [
        #   positions        colors
        -0.5, -0.5, 0.0, r, g, b,
        0.5, -0.5, 0.0, r, g, b,
        0.5, 0.5, 0.0, r, g, b,
        -0.5, 0.5, 0.0, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


# Tarea4: Nueva función para generar un cuadrado texturado con normales
def createTextureQuadWithNormal(nx, ny):
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
        #   positions        texture  normal
        -0.5, -0.5, 0.0, 0, ny, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.0, nx, ny, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.0, nx, 0, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.0, 0, 0, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)


def createTextureQuad(nx, ny):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture
        -0.5, -0.5, 0.0, 0, ny,
        0.5, -0.5, 0.0, nx, ny,
        0.5, 0.5, 0.0, nx, 0,
        -0.5, 0.5, 0.0, 0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,
        2, 3, 0]

    return Shape(vertices, indices)

def createTextureTri(nx, ny): # codigo para hacer un triangulo
    # este codigo es bastante simple, es solo el colored quad con un vertice borrado y los indices como corresponde
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture
        -0.5, -0.5, 0.0, 0, ny,
        0.5, -0.5, 0.0, nx, ny,
        0.5, 0.5, 0.0, nx, 0,]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,0]

    return Shape(vertices, indices)

def createColorCircle(N, r, g, b):
    # First vertex at the center
    colorOffsetAtCenter = 0.3
    vertices = [0, 0, 0,
                r + colorOffsetAtCenter,
                g + colorOffsetAtCenter,
                b + colorOffsetAtCenter]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,
            # color
            r, g, b]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i + 1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return Shape(vertices, indices)


def createRainbowCircle(N):
    # First vertex at the center, white color
    vertices = [0, 0, 0, 1.0, 1.0, 1.0]
    indices = []

    dtheta = 2 * math.pi / N

    for i in range(N):
        theta = i * dtheta

        vertices += [
            # vertex coordinates
            0.5 * math.cos(theta), 0.5 * math.sin(theta), 0,

            # color generates varying between 0 and 1
            math.sin(theta), math.cos(theta), 0]

        # A triangle is created using the center, this and the next vertex
        indices += [0, i, i + 1]

    # The final triangle connects back to the second vertex
    indices += [0, N, 1]

    return Shape(vertices, indices)


def createRainbowCube():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions         colors
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def readOFF(filename, color):
    vertices = []
    normals = []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line == "OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]

        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        # print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices, 3), dtype=np.float32)
        # print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]

            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1],
                    vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1],
                    vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]
            normals[aux[1]][1] += res[1]
            normals[aux[1]][2] += res[2]

            normals[aux[2]][0] += res[0]
            normals[aux[2]][1] += res[1]
            normals[aux[2]][2] += res[2]

            normals[aux[3]][0] += res[0]
            normals[aux[3]][1] += res[1]
            normals[aux[3]][2] += res[2]
            # print(faces)
        norms = np.linalg.norm(normals, axis=1)
        normals = normals / norms[:, None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        # print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0], :]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1], :]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2], :]
            vertexDataF += vertex.tolist()

            indices += [index, index + 1, index + 2]
            index += 3

        return Shape(vertexDataF, indices)


def createColorCubeOFF(r, g, b):
    return readOFF(getAssetPath('cube.off'), (r, g, b))


def createColorSphereOFF(r, g, b):
    return readOFF(getAssetPath('sphere.off'), (r, g, b))


def createColorCylinderOFF(r, g, b):
    return readOFF(getAssetPath('cylinder.off'), (r, g, b))


def createColorConeOFF(r, g, b):
    return readOFF(getAssetPath('cone.off'), (r, g, b))


def createColorCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5, 0.5, r, g, b,
        0.5, -0.5, 0.5, r, g, b,
        0.5, 0.5, 0.5, r, g, b,
        -0.5, 0.5, 0.5, r, g, b,

        -0.5, -0.5, -0.5, r, g, b,
        0.5, -0.5, -0.5, r, g, b,
        0.5, 0.5, -0.5, r, g, b,
        -0.5, 0.5, -0.5, r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createFacetedCube():
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 0.0,
        -0.5, 0.5, 0.5, 1.0, 0.0, 0.0,
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, 0.5, 1.0, 0.0, 0.0,

        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
        0.5, 0.5, -0.5, 0.0, 1.0, 0.0,

        0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5, 0.5, 0.5, 0.0, 0.0, 1.0,

        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
        -0.5, 0.5, -0.5, 1.0, 0.0, 0.0,
        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
        0.5, 0.5, -0.5, 1.0, 0.0, 0.0,

        -0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0,
        -0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
        -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
        -0.5, 0.5, -0.5, 0.0, 1.0, 0.0,

        0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5, -0.5, 0.0, 0.0, 1.0,
        -0.5, -0.5, 0.5, 0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = range(36)

    return Shape(vertices, indices)


def createTextureCube(image_filename):
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.5, -0.5, 0.5, 0, 1,
        0.5, -0.5, 0.5, 1, 1,
        0.5, 0.5, 0.5, 1, 0,
        -0.5, 0.5, 0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, 0.5, -0.5, 1, 0,
        -0.5, 0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0, 1,
        0.5, 0.5, -0.5, 1, 1,
        0.5, 0.5, 0.5, 1, 0,
        0.5, -0.5, 0.5, 0, 0
        ,

        # X-
        -0.5, -0.5, -0.5, 0, 1,
        -0.5, 0.5, -0.5, 1, 1,
        -0.5, 0.5, 0.5, 1, 0,
        -0.5, -0.5, 0.5, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, 0, 1,
        0.5, 0.5, -0.5, 1, 1,
        0.5, 0.5, 0.5, 1, 0,
        -0.5, 0.5, 0.5, 0, 0,

        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5, 0.5, 1, 0,
        -0.5, -0.5, 0.5, 0, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices,image_filename)

def createTextureTriangle(image_filename): #piramide
    # codigo poco optimo hecho a partir del cubo
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.0, -0.0, 0.5, 0, 1, # cambio los z+ para ser la punto del triangulo (piramide)
        0.0, -0.0, 0.5, 1, 1,
        0.0, 0.0, 0.5, 1, 0,
        -0.0, 0.0, 0.5, 0, 0,

        # Z-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, 0.5, -0.5, 1, 0,
        -0.5, 0.5, -0.5, 0, 0,

        # X+
        0.5, -0.5, -0.5, 0, 1,
        0.5, 0.5, -0.5, 1, 1,
        0.5, 0.0, 0.5, 1, 0,
        0.5, 0.0, 0.5, 0, 0
        ,

        # X-
        -0.5, -0.5, -0.5, 0, 1,
        -0.5, 0.5, -0.5, 1, 1,
        -0.5, 0.0, 0.5, 1, 0,
        -0.5, 0.0, 0.5, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, 0, 1,
        0.5, 0.5, -0.5, 1, 1,
        0.5, 0.5, 0.5, 1, 0,
        -0.5, 0.5, 0.5, 0, 0,

        # Y-
        -0.5, -0.5, -0.5, 0, 1,
        0.5, -0.5, -0.5, 1, 1,
        0.5, -0.5, 0.5, 1, 0,
        -0.5, -0.5, 0.5, 0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified4
    indices = [ 7,6,5,5,4,7, # uno los vertices normales y luego paso por la punto que es el vertice 2
               8,2,9,9,2,8,
               17,2,16,16,2,17,
               12,2,13,13,2,12,
               20,2,21,21,2,20
               ]
    # indices = [
    #     0, 1, 2, 2, 3, 0,  # Z+
    #     7, 6, 5, 5, 4, 7,  # Z-
    #     8, 9, 2, 2, 11, 8,  # X+
    #     15, 14, 2, 2, 12, 15,  # X-
    #     19, 18, 17, 17, 16, 19,  # Y+
    #     20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices,image_filename)



def createRainbowNormalsCube():
    sq3 = 0.57735027

    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #    positions        colors          normals
        -0.5, -0.5, 0.5, 1.0, 0.0, 0.0, -sq3, -sq3, sq3,
        0.5, -0.5, 0.5, 0.0, 1.0, 0.0, sq3, -sq3, sq3,
        0.5, 0.5, 0.5, 0.0, 0.0, 1.0, sq3, sq3, sq3,
        -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, -sq3, sq3, sq3,

        -0.5, -0.5, -0.5, 1.0, 1.0, 0.0, -sq3, -sq3, -sq3,
        0.5, -0.5, -0.5, 0.0, 1.0, 1.0, sq3, -sq3, -sq3,
        0.5, 0.5, -0.5, 1.0, 0.0, 1.0, sq3, sq3, -sq3,
        -0.5, 0.5, -0.5, 1.0, 1.0, 1.0, -sq3, sq3, -sq3]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [0, 1, 2, 2, 3, 0,
               4, 5, 6, 6, 7, 4,
               4, 5, 1, 1, 0, 4,
               6, 7, 3, 3, 2, 6,
               5, 6, 2, 2, 1, 5,
               7, 4, 0, 0, 3, 7]

    return Shape(vertices, indices)


def createColorNormalsCube(r, g, b):
    # Defining the location and colors of each vertex  of the shape
    vertices = [
        #   positions         colors   normals
        # Z+
        -0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, -0.5, 0.5, r, g, b, 0, 0, 1,
        0.5, 0.5, 0.5, r, g, b, 0, 0, 1,
        -0.5, 0.5, 0.5, r, g, b, 0, 0, 1,

        # Z-
        -0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, -0.5, -0.5, r, g, b, 0, 0, -1,
        0.5, 0.5, -0.5, r, g, b, 0, 0, -1,
        -0.5, 0.5, -0.5, r, g, b, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, -0.5, r, g, b, 1, 0, 0,
        0.5, 0.5, 0.5, r, g, b, 1, 0, 0,
        0.5, -0.5, 0.5, r, g, b, 1, 0, 0,

        # X-
        -0.5, -0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, -0.5, r, g, b, -1, 0, 0,
        -0.5, 0.5, 0.5, r, g, b, -1, 0, 0,
        -0.5, -0.5, 0.5, r, g, b, -1, 0, 0,

        # Y+
        -0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, -0.5, r, g, b, 0, 1, 0,
        0.5, 0.5, 0.5, r, g, b, 0, 1, 0,
        -0.5, 0.5, 0.5, r, g, b, 0, 1, 0,

        # Y-
        -0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, -0.5, r, g, b, 0, -1, 0,
        0.5, -0.5, 0.5, r, g, b, 0, -1, 0,
        -0.5, -0.5, 0.5, r, g, b, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)


def createTextureNormalsCube(image_filename):
    # Defining locations,texture coordinates and normals for each vertex of the shape
    vertices = [
        #   positions            tex coords   normals
        # Z+
        -0.5, -0.5, 0.5, 0, 1, 0, 0, 1,
        0.5, -0.5, 0.5, 1, 1, 0, 0, 1,
        0.5, 0.5, 0.5, 1, 0, 0, 0, 1,
        -0.5, 0.5, 0.5, 0, 0, 0, 0, 1,
        # Z-
        -0.5, -0.5, -0.5, 0, 1, 0, 0, -1,
        0.5, -0.5, -0.5, 1, 1, 0, 0, -1,
        0.5, 0.5, -0.5, 1, 0, 0, 0, -1,
        -0.5, 0.5, -0.5, 0, 0, 0, 0, -1,

        # X+
        0.5, -0.5, -0.5, 0, 1, 1, 0, 0,
        0.5, 0.5, -0.5, 1, 1, 1, 0, 0,
        0.5, 0.5, 0.5, 1, 0, 1, 0, 0,
        0.5, -0.5, 0.5, 0, 0, 1, 0, 0,
        # X-
        -0.5, -0.5, -0.5, 0, 1, -1, 0, 0,
        -0.5, 0.5, -0.5, 1, 1, -1, 0, 0,
        -0.5, 0.5, 0.5, 1, 0, -1, 0, 0,
        -0.5, -0.5, 0.5, 0, 0, -1, 0, 0,
        # Y+
        -0.5, 0.5, -0.5, 0, 1, 0, 1, 0,
        0.5, 0.5, -0.5, 1, 1, 0, 1, 0,
        0.5, 0.5, 0.5, 1, 0, 0, 1, 0,
        -0.5, 0.5, 0.5, 0, 0, 0, 1, 0,
        # Y-
        -0.5, -0.5, -0.5, 0, 1, 0, -1, 0,
        0.5, -0.5, -0.5, 1, 1, 0, -1, 0,
        0.5, -0.5, 0.5, 1, 0, 0, -1, 0,
        -0.5, -0.5, 0.5, 0, 0, 0, -1, 0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices, image_filename)


def Esfera2(r,lats,longs,red,g,b): #Nuevo función esfera mejorada
    # toma lineas laterales, longitudinales, radio, y los colores
    dtheta = 2*np.pi/lats # paso 2pi
    dphi = np.pi/longs # paso pi
    vertices = []
    indices = []
    for i in range(lats+1): 
        theta = np.pi/2 - i*dtheta #doy la vuelta completa
        xy = r*np.cos(theta) # xy
        z = r*np.sin(theta) #z
        for j in range(longs+1): # por cada uno de estos circulos
            phi = j*dphi 
            x = xy*np.cos(phi) # hafo el x e y
            y = xy*np.sin(phi)
            vertices += [x,y,z,red,g,b] # añado el punto con color
    
    for i in range(longs): #empiezo a formar el orden de puntos
        k1 = i*(lats+1)
        k2 = k1 + lats + 1

        for j in range(lats):
            if i != 0:
                indices += [k1,k2,k1+1] # uno los puntos
            if i!= (longs-1):
                indices += [k1+1,k2,k2+1] # uno los puntos
            k1 += 1
            k2 += 1
    
    return Shape(vertices,indices)

def createTextureNormalsCube(image_filename):

    # Defining locations,texture coordinates and normals for each vertex of the shape  
    vertices = [
    #   positions            tex coords   normals
    # Z+
        -0.5, -0.5,  0.5,    0, 1,        0,0,1,
         0.5, -0.5,  0.5,    1, 1,        0,0,1,
         0.5,  0.5,  0.5,    1, 0,        0,0,1,
        -0.5,  0.5,  0.5,    0, 0,        0,0,1,   
    # Z-          
        -0.5, -0.5, -0.5,    0, 1,        0,0,-1,
         0.5, -0.5, -0.5,    1, 1,        0,0,-1,
         0.5,  0.5, -0.5,    1, 0,        0,0,-1,
        -0.5,  0.5, -0.5,    0, 0,        0,0,-1,
       
    # X+          
         0.5, -0.5, -0.5,    0, 1,        1,0,0,
         0.5,  0.5, -0.5,    1, 1,        1,0,0,
         0.5,  0.5,  0.5,    1, 0,        1,0,0,
         0.5, -0.5,  0.5,    0, 0,        1,0,0,   
    # X-          
        -0.5, -0.5, -0.5,    0, 1,        -1,0,0,
        -0.5,  0.5, -0.5,    1, 1,        -1,0,0,
        -0.5,  0.5,  0.5,    1, 0,        -1,0,0,
        -0.5, -0.5,  0.5,    0, 0,        -1,0,0,   
    # Y+          
        -0.5,  0.5, -0.5,    0, 1,        0,1,0,
         0.5,  0.5, -0.5,    1, 1,        0,1,0,
         0.5,  0.5,  0.5,    1, 0,        0,1,0,
        -0.5,  0.5,  0.5,    0, 0,        0,1,0,   
    # Y-          
        -0.5, -0.5, -0.5,    0, 1,        0,-1,0,
         0.5, -0.5, -0.5,    1, 1,        0,-1,0,
         0.5, -0.5,  0.5,    1, 0,        0,-1,0,
        -0.5, -0.5,  0.5,    0, 0,        0,-1,0
        ]   

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices, image_filename)

def createTextureQuadWithNormal(nx, ny):
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture  normal
        -0.5, -0.5, 0.0,  0, ny, 0.0, 0.0, 1.0,
         0.5, -0.5, 0.0, nx, ny, 0.0, 0.0, 1.0,
         0.5,  0.5, 0.0, nx, 0,  0.0, 0.0, 1.0,
        -0.5,  0.5, 0.0,  0, 0,  0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


#simples recraciones de otras figuras, pero añadi el componente de normales para este trabajo
def createColorNormalsCube(r, g, b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #   positions         colors   normals
    # Z+
        -0.5, -0.5,  0.5, r, g, b, 0,0,1,
         0.5, -0.5,  0.5, r, g, b, 0,0,1,
         0.5,  0.5,  0.5, r, g, b, 0,0,1,
        -0.5,  0.5,  0.5, r, g, b, 0,0,1,

    # Z-
        -0.5, -0.5, -0.5, r, g, b, 0,0,-1,
         0.5, -0.5, -0.5, r, g, b, 0,0,-1,
         0.5,  0.5, -0.5, r, g, b, 0,0,-1,
        -0.5,  0.5, -0.5, r, g, b, 0,0,-1,
        
    # X+
        0.5, -0.5, -0.5, r, g, b, 1,0,0,
        0.5,  0.5, -0.5, r, g, b, 1,0,0,
        0.5,  0.5,  0.5, r, g, b, 1,0,0,
        0.5, -0.5,  0.5, r, g, b, 1,0,0,
 
    # X-
        -0.5, -0.5, -0.5, r, g, b, -1,0,0,
        -0.5,  0.5, -0.5, r, g, b, -1,0,0,
        -0.5,  0.5,  0.5, r, g, b, -1,0,0,
        -0.5, -0.5,  0.5, r, g, b, -1,0,0,

    # Y+
        -0.5, 0.5, -0.5, r, g, b, 0,1,0,
         0.5, 0.5, -0.5, r, g, b, 0,1,0,
         0.5, 0.5,  0.5, r, g, b, 0,1,0,
        -0.5, 0.5,  0.5, r, g, b, 0,1,0,

    # Y-
        -0.5, -0.5, -0.5, r, g, b, 0,-1,0,
         0.5, -0.5, -0.5, r, g, b, 0,-1,0,
         0.5, -0.5,  0.5, r, g, b, 0,-1,0,
        -0.5, -0.5,  0.5, r, g, b, 0,-1,0
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices)

#simples recraciones de otras figuras, pero añadi el componente de normales para este trabajo
def createTextureTriWithNormal(nx, ny): # codigo para hacer un triangulo
    # este codigo es bastante simple, es solo el colored quad con un vertice borrado y los indices como corresponde
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions        texture
        -0.5, -0.5, 0.0, 0, ny, 0.0, 0.0, 1.0,
        0.5, -0.5, 0.0, nx, ny, 0.0, 0.0, 1.0,
        0.5, 0.5, 0.0, nx, 0,   0.0, 0.0, 1.0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2,0]

    return Shape(vertices, indices)

#simples recraciones de otras figuras, pero añadi el componente de normales para este trabajo
def createTextureTriangleWithNormal(image_filename): #piramide
    # codigo poco optimo hecho a partir del cubo
    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #   positions         texture coordinates
        # Z+
        -0.0, -0.0, 0.5, 0, 1, 0,0,1,               # cambio los z+ para ser la punto del triangulo (piramide)
        0.0, -0.0, 0.5, 1, 1, 0,0,1,
        0.0, 0.0, 0.5, 1, 0, 0,0,1,
        -0.0, 0.0, 0.5, 0, 0, 0,0,1,

        # Z-
        -0.5, -0.5, -0.5, 0, 1, 0,0,-1,
        0.5, -0.5, -0.5, 1, 1, 0,0,-1,
        0.5, 0.5, -0.5, 1, 0, 0,0,-1,
        -0.5, 0.5, -0.5, 0, 0, 0,0,-1,

        # X+
        0.5, -0.5, -0.5, 0, 1, 1,0,0,
        0.5, 0.5, -0.5, 1, 1, 1,0,0,
        0.5, 0.0, 0.5, 1, 0, 1,0,0,
        0.5, 0.0, 0.5, 0, 0, 1,0,0,

        # X-
        -0.5, -0.5, -0.5, 0, 1, -1,0,0,
        -0.5, 0.5, -0.5, 1, 1, -1,0,0,
        -0.5, 0.0, 0.5, 1, 0, -1,0,0,
        -0.5, 0.0, 0.5, 0, 0, -1,0,0,

        # Y+
        -0.5, 0.5, -0.5, 0, 1, 0,1,0,
        0.5, 0.5, -0.5, 1, 1, 0,1,0,
        0.5, 0.5, 0.5, 1, 0, 0,1,0,
        -0.5, 0.5, 0.5, 0, 0, 0,1,0,

        # Y-
        -0.5, -0.5, -0.5, 0, 1, 0,-1,0,
        0.5, -0.5, -0.5, 1, 1, 0,-1,0,
        0.5, -0.5, 0.5, 1, 0, 0,-1,0,
        -0.5, -0.5, 0.5, 0, 0, 0,-1,0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified4
    indices = [ 7,6,5,5,4,7, # uno los vertices normales y luego paso por la punto que es el vertice 2
               8,2,9,9,2,8,
               17,2,16,16,2,17,
               12,2,13,13,2,12,
               20,2,21,21,2,20
               ]
    return Shape(vertices, indices,image_filename)

#simples recraciones de otras figuras, pero añadi el componente de normales para este trabajo
# Aqui es digno de mencion que fue comveniente la normal, pq es simplemente el vector del punto desde el (0,0,0) haciendo sus normales triviales
def Esfera3(r,lats,longs,red,g,b): #Nuevo función esfera mejorada
    # toma lineas laterales, longitudinales, radio, y los colores
    dtheta = 2*np.pi/lats # paso 2pi
    dphi = np.pi/longs # paso pi
    vertices = []
    indices = []
    lengthInv = 1 / r
    for i in range(lats+1): 
        theta = np.pi/2 - i*dtheta #doy la vuelta completa
        xy = r*np.cos(theta) # xy
        z = r*np.sin(theta) #z
        for j in range(longs+1): # por cada uno de estos circulos
            phi = j*dphi 
            x = xy*np.cos(phi) # hafo el x e y
            y = xy*np.sin(phi) 
            nx = x * lengthInv
            ny = y * lengthInv
            nz = z * lengthInv
            vertices += [x,y,z,red,g,b,nx,ny,nz] # añado el punto con color y normales
    
    for i in range(longs): #empiezo a formar el orden de puntos
        k1 = i*(lats+1)
        k2 = k1 + lats + 1

        for j in range(lats):
            if i != 0:
                indices += [k1,k2,k1+1] # uno los puntos
            if i!= (longs-1):
                indices += [k1+1,k2,k2+1] # uno los puntos
            k1 += 1
            k2 += 1
    
    return Shape(vertices,indices)

    ############################################################ SPLINE #####################################################################
# Esta es la función spline que use, la conoci a traves de un video de youtube que encontre y funciona muy bien
# https://www.youtube.com/watch?v=9_aJGUTePYo&t=783s 
# le agregue lo de los colores y las shapes para el trabajo posterior de modelarlo para verlo en el trabajo para hacer más fácil de modificar
def CatmullRom(puntos, P,r,g,b): # puntos, son los puntos 
    # P: cantidad de particiones
    # CatmullRom esta googleado, es un tipo de spline bacan

    # Listas que voy a usar:
    vertices = []
    indices = []
    mov = [] # puntos
    angulo = [] # angulo

    # por cada uno en la particion
    for i in range(0,P):
        i = i/P
    # forma 4 puntos 
        p1 = int(i) 
        p2 = (p1 + 1)  %len(puntos)
        p3 = (p2 + 1)  %len(puntos) 
        p0 = p1 - 1 if p1 >= 1 else len(puntos) - 1

        i = i - int(i)

        i_2 = i*i 
        i_3 = i_2*i 

        #constantes
        q1 = -i_3 + 2 * i_2 - i
        q2 = 3 * i_3 - 5 * i_2 + 2
        q3 = -3 * i_3 + 4 * i_2 + i
        q4 = i_3 - i_2
        a = 0.5

        x = a*(puntos[p0][0]*q1 + puntos[p1][0]*q2 + puntos[p2][0]*q3 + puntos[p3][0]*q4)
        y = a*(puntos[p0][1]*q1 + puntos[p1][1]*q2 + puntos[p2][1]*q3 + puntos[p3][1]*q4) 

    # añade
        mov += [x,y]
        vertices += [x,y,0,r,g,b]
    # hago los indices
    for k in range(0,(P//2)-1):
        indices += [2*k,2*k+1,2*k+2]

    # veo los angulos 
    for j in range(len(mov)//2):
        # el angulo se hace viendo el arctan de la distancia entre el punto y el siguiente
        angulo += [np.arctan2(mov[(2*j+3)%len(mov)]-mov[(2*j+1)%len(mov)], mov[(2*j+2)%len(mov)] - mov[(2*j)%len(mov)])]
    #retorno 
    return Shape(vertices,indices), mov, angulo