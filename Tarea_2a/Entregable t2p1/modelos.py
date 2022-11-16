# Diego Echeverria
# MODELOS
import glfw
from OpenGL.GL import *
import numpy as np
import sys
import os.path
import transformations as tr
import basic_shapes as bs
import easy_shaders as es
import scene_graph as sg
from assets_path import getAssetPath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
############################################################### RESUMEN ##############################################################################
# FUNCION piso_floor para hacer todo el piso
# FUNCION calles para hacer calles
# FUNCION casa1 como casa de 1 piso
# FUNCION casa2 como casa de 2 piso
# FUNCION arbol1 como arbol de color
# FUNCION arbol2 como arbol de color 
# FUNCION arbol3 como arbol de color 
# FUNCION bosque1 como agrupación de los primeros 3 arboles
# FUNCION bosque2 como segunda agrupación de los primeros 3 arboles
######################################################################################################################################################


def piso_Floor(pipeline): # funcion que crea el piso del modelo
# el piso va a estar compuesto de un cuadrado de concreto y dos triangulos, uno de concreto y una de pasto
    
    piso_Floor1 = bs.createTextureQuad(10, 10) # el creador del quad con textura de concreto
    gpuFloor1 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor1)
    gpuFloor1.texture = es.textureSimpleSetup(
        getAssetPath("piso7.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor1.fillBuffers(piso_Floor1.vertices, piso_Floor1.indices, GL_STATIC_DRAW)

    piso_Floor2 = bs.createTextureTri(10, 10)  # el creador del triangulo con textura de concreto
    gpuFloor2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor2)
    gpuFloor2.texture = es.textureSimpleSetup(
        getAssetPath("piso7.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor2.fillBuffers(piso_Floor2.vertices, piso_Floor2.indices, GL_STATIC_DRAW)

    piso_PASTO = bs.createTextureTri(10, 10) # el creador del triangulo textura de pasto
    gpuPASTO = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPASTO)
    gpuPASTO.texture = es.textureSimpleSetup(
        getAssetPath("piso6.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuPASTO.fillBuffers(piso_PASTO.vertices, piso_PASTO.indices, GL_STATIC_DRAW)

    piso = sg.SceneGraphNode("piso") #cuadrado con su transform
    piso.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(1,1,1),tr.translate(0,0,0)])
    piso.childs += [gpuFloor1]

    piso2 = sg.SceneGraphNode("piso2") #triangulo con su transform
    piso2.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(1,1,1),tr.translate(0,1,0)])
    piso2.childs += [gpuFloor2]

    pasto = sg.SceneGraphNode("pasto") #triangulo con su transform
    pasto.transform = tr.matmul([tr.rotationX(np.pi),tr.rotationZ(np.pi),tr.scale(1,1,1),tr.translate(1,0,0)])
    pasto.childs += [gpuPASTO]

    floor = sg.SceneGraphNode("floor") # los uno todos
    floor.transform = tr.scale(4,4,1) #los escalo
    floor.childs += [piso,piso2,pasto] 

    return floor # retorno la figura final

def calles(pipeline):
    # Funcion que crea las calles, estas son 4, la curva, la de arriba, la de la derecha y la de abajo
    CALLE = bs.createTextureQuad(1, 10) # este crea el quad de calle para todos
    gpuCALLE = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCALLE)
    gpuCALLE.texture = es.textureSimpleSetup(
        getAssetPath("calle2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuCALLE.fillBuffers(CALLE.vertices, CALLE.indices, GL_STATIC_DRAW)

    # def shearing(xy, yx, xz, zx, yz, zy):
    calle_diagonal = sg.SceneGraphNode("calle_diagonal") # para la calle diagonal roto y hago shearing
    calle_diagonal.transform = tr.matmul([tr.shearing(-1,0,0,0,0,0),tr.scale(0.8,4,1),tr.translate(-4.5,0,0.01)])
    calle_diagonal.childs += [gpuCALLE]

    calle_arriba = sg.SceneGraphNode("calle_arriba") #calle de arriba
    calle_arriba.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.3,7.2,1),tr.translate(6.2,0.222,0.011)])
    calle_arriba.childs += [gpuCALLE]

    calle_lado = sg.SceneGraphNode("calle_lado") #calle de la derecha
    calle_lado.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.3,4,1),tr.translate(6.2,0,0.012)])
    calle_lado.childs += [gpuCALLE]

    calle_abajo = sg.SceneGraphNode("calle_abajo") #calle de abajo
    calle_abajo.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.35,3.55,1),tr.translate(-5.22,-0.065,0.011)])
    calle_abajo.childs += [gpuCALLE]

    calles = sg.SceneGraphNode("calles") # uno todas las calles 
    calles.transform = tr.matmul([tr.rotationZ(0),tr.scale(1,1,1),tr.translate(0,0,0)])
    calles.childs += [calle_diagonal,calle_arriba,calle_lado,calle_abajo]
    # [calle_diagonal,calle_arriba,calle_lado,calle_abajo]
    
    return calles # retorno las calles





def casa1(pipeline,image_muro,image_techo): # defino la casa de 1 piso
    # ESTA CASA va a tener: 1puerta, 4muros, 3 ventanas, 3 marcos alrededor de la puerta, 1 techo y uno foto de gato

    ## defino muro
    Muro = bs.createTextureCube(image_muro)
    gpuMuro = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuMuro)
    gpuMuro.texture = es.textureSimpleSetup(
        getAssetPath(image_muro), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuMuro.fillBuffers(Muro.vertices, Muro.indices, GL_STATIC_DRAW)

    ## defino puerta
    Puerta = bs.createTextureCube("puerta6.jpg")
    gpuPuerta = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPuerta)
    gpuPuerta.texture = es.textureSimpleSetup(
        getAssetPath("puerta6.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuPuerta.fillBuffers(Puerta.vertices, Puerta.indices, GL_STATIC_DRAW)

    ## defino ventana
    Ventana = bs.createTextureCube("ventana2.jpg")
    gpuVentana = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuVentana)
    gpuVentana.texture = es.textureSimpleSetup(
        getAssetPath("ventana2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuVentana.fillBuffers(Ventana.vertices, Ventana.indices, GL_STATIC_DRAW)

    ## defino techo
    Techo = bs.createTextureTriangle(image_techo)
    gpuTecho = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTecho)
    gpuTecho.texture = es.textureSimpleSetup(
        getAssetPath(image_techo), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuTecho.fillBuffers(Techo.vertices, Techo.indices, GL_STATIC_DRAW)

    ## defino gato
    GATO = bs.createTextureQuad(1,1)
    gpuGATO = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGATO)
    gpuGATO.texture = es.textureSimpleSetup(
        getAssetPath("Gato_jaja.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuGATO.fillBuffers(GATO.vertices, GATO.indices, GL_STATIC_DRAW)

    # creo la imagen de gato 
    gato1 = sg.SceneGraphNode("gato1") #derecha
    gato1.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(1,1,1),tr.translate(0,0,0.01)])
    gato1.childs += [gpuGATO]

    #hago las 4 paredes y las traslado juntas 
    pared1_1 = sg.SceneGraphNode("pared1_1") #derecha
    pared1_1.transform = tr.matmul([tr.scale(0.1,0.9,0.75),tr.translate(-4.5,0,0.5)])
    pared1_1.childs += [gpuMuro]

    pared1_2 = sg.SceneGraphNode("pared1_2") # izquierda
    pared1_2.transform = tr.matmul([tr.scale(0.1,0.9,0.75),tr.translate(4.5,0,0.5)])
    pared1_2.childs += [gpuMuro]

    pared1_3 = sg.SceneGraphNode("pared1_3") # arriba
    pared1_3.transform = tr.matmul([tr.scale(1,0.1,0.75),tr.translate(0,5,0.5)])
    pared1_3.childs += [gpuMuro]

    pared1_4 = sg.SceneGraphNode("pared1_4") # abajo
    pared1_4.transform = tr.matmul([tr.scale(1,0.1,0.75),tr.translate(0,-5,0.5)])
    pared1_4.childs += [gpuMuro]

    # uno los 4 muros juntos 
    pared = sg.SceneGraphNode("pared")
    pared.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0.01)])
    pared.childs += [pared1_1,pared1_2,pared1_3,pared1_4]

    ## defino PUERTA
    # le voy a hacer un marco y finalmente un cubo con la textura

    #aqui estan los 3 marcos que van a ir alrededor de la puerta, usan la misma textura que el muro
    marco1_1 = sg.SceneGraphNode("marco1_1") # IZQUIERDA
    marco1_1.transform = tr.matmul([tr.scale(0.01,0.05,1),tr.translate(20,0,0)])
    marco1_1.childs += [gpuMuro] # lo añado a gpu muro pq es tmb material madera

    marco1_2 = sg.SceneGraphNode("marco1_2") # derecha
    marco1_2.transform = tr.matmul([tr.scale(0.01,0.05,1),tr.translate(-20,0,0)])
    marco1_2.childs += [gpuMuro] # lo añado a gpu muro pq es tmb material madera

    marco1_3 = sg.SceneGraphNode("marco1_3") # arriba
    marco1_3.transform = tr.matmul([tr.scale(0.4,0.05,0.01),tr.translate(0,0,50)])
    marco1_3.childs += [gpuMuro] # lo añado a gpu muro pq es tmb material madera

    # junto los 3 nodos de marco para hacer uno 
    marco1 = sg.SceneGraphNode("marco1") # los 3 marcos juntos
    marco1.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0)])
    marco1.childs += [marco1_1,marco1_2,marco1_3] # lo añado a gpu muro pq es tmb material madera

    #hago la puerta 
    puerta1 = sg.SceneGraphNode("puerta1") #la puerta
    puerta1.transform = tr.matmul([tr.scale(0.4,0.05,1),tr.translate(0,0,0)])
    puerta1.childs += [gpuPuerta] # lo añado a gpu muro pq es tmb material madera

    # uno el marco con la puerta
    puerta = sg.SceneGraphNode("puerta") # el conjunto
    puerta.transform = tr.matmul([tr.scale(0.4,0.3,0.3),tr.translate(0,1.85,0.5)])
    puerta.childs += [marco1,puerta1]


    # ventana, voy a hacer 3 ventanas. una arriba de la puerta y dos juntas en un muro de los lados
    ventana1 = sg.SceneGraphNode("ventana1")
    ventana1.transform = tr.matmul([tr.scale(0.75,0.01,0.2),tr.translate(0,55,2.2)])
    ventana1.childs += [gpuVentana] 

    ventana2 = sg.SceneGraphNode("ventana2")
    ventana2.transform = tr.matmul([tr.scale(0.01,0.2,0.4),tr.translate(50,-1.5,1)])
    ventana2.childs += [gpuVentana] 

    ventana3 = sg.SceneGraphNode("ventana3")
    ventana3.transform = tr.matmul([tr.scale(0.01,0.2,0.4),tr.translate(50,1.5,1)])
    ventana3.childs += [gpuVentana] 

    #aqui junto las ventanas
    ventana = sg.SceneGraphNode("ventana")
    ventana.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0)])
    ventana.childs += [ventana1,ventana2,ventana3]

    ## defino techo, este va a ser una piramide
    techo1 = sg.SceneGraphNode("techo1")
    techo1.transform = tr.matmul([tr.scale(1,1,0.5),tr.translate(0,0,2.02)])
    techo1.childs += [gpuTecho]

    # le hago un segundo nodo, por si quiero agregar algo, pero más que nada por orden y costumbre
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.scale(1.2,1.2,1),tr.translate(0,0,0)])
    techo.childs += [techo1]



    #casa completa
    # tomo todos los elementos de la casa y los junto 
    casa1 = sg.SceneGraphNode("casa1")
    casa1.transform = tr.matmul([tr.scale(0.5,0.5,0.5),tr.translate(0.5,0.5,0)])
    casa1.childs += [pared, puerta,ventana,techo,gato1]

    return casa1



def arbol1(pipeline): # arbol amarillo
    #creo las esfera de colores que van a ser las hojas
    Hojas = bs.Esfera2(1,50,50,219/255,219/255,107/255)
    gpuHojas = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuHojas)
    gpuHojas.fillBuffers(Hojas.vertices, Hojas.indices, GL_STATIC_DRAW)

    # los cubos de madera que será el tronco y una pequeña ramita en el tronco
    Tronco = bs.createColorCube(87/255,51/255,4/255)
    gpuTronco = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTronco)
    gpuTronco.fillBuffers(Tronco.vertices,Tronco.indices, GL_STATIC_DRAW)


    # el tronco grande
    tronco1 = sg.SceneGraphNode("tronco1")
    tronco1.transform = tr.matmul([tr.scale(0.05,0.05,0.5),tr.translate(3.5,-1.8,0.6)])
    tronco1.childs += [gpuTronco]

    #el tronco chico (ramita)
    tronco2 = sg.SceneGraphNode("tronco2")
    tronco2.transform = tr.matmul([tr.rotationX(np.pi/4),tr.scale(0.02,0.02,0.1),tr.translate(9,10,4)])
    tronco2.childs += [gpuTronco]

    # la union de ambos
    madera = sg.SceneGraphNode("madera")
    madera.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0.32,0.15)])
    madera.childs += [tronco1,tronco2] 
    
    # siguen las 3 esfera que son las hojas
    #esfera 1
    hojas1 = sg.SceneGraphNode("hojas1")
    hojas1.transform = tr.matmul([tr.scale(0.15,0.15,0.15),tr.translate(1,1.6,1.5)])
    hojas1.childs += [gpuHojas] 
    #esfera 2
    hojas2 = sg.SceneGraphNode("hojas2")
    hojas2.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(1.1,1.5,2)])
    hojas2.childs += [gpuHojas] 
    #esfera 3
    hojas3 = sg.SceneGraphNode("hojas3")
    hojas3.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(1,0.5,1.6)])
    hojas3.childs += [gpuHojas]
    # la union de todas las hojas
    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0.5)])
    hojas.childs += [hojas1, hojas2, hojas3] 
    
    # la union de todos los elementos ya mencionados
    arbol1 = sg.SceneGraphNode("arbol1")
    arbol1.transform = tr.matmul([tr.scale(0.6,0.6,0.6),tr.translate(0,0,-0.2)])
    arbol1.childs += [hojas,madera]

    return arbol1 

def arbol2(pipeline): # mismo arbol pero ahora verde claro, 
    # Toda la documentoción es igual a la anterior 

    Hojas2 = bs.Esfera2(1,50,50,136/255,180/255,101/255)
    gpuHojas2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuHojas2)
    gpuHojas2.fillBuffers(Hojas2.vertices, Hojas2.indices, GL_STATIC_DRAW)

    Tronco = bs.createColorCube(87/255,51/255,4/255)
    gpuTronco = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTronco)
    gpuTronco.fillBuffers(Tronco.vertices,Tronco.indices, GL_STATIC_DRAW)



    tronco1 = sg.SceneGraphNode("tronco1")
    tronco1.transform = tr.matmul([tr.scale(0.05,0.05,0.5),tr.translate(3.5,-1.8,0.6)])
    tronco1.childs += [gpuTronco]

    tronco2 = sg.SceneGraphNode("tronco2")
    tronco2.transform = tr.matmul([tr.rotationX(np.pi/4),tr.scale(0.02,0.02,0.1),tr.translate(9,10,4)])
    tronco2.childs += [gpuTronco]

    madera = sg.SceneGraphNode("madera")
    madera.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0.32,0.15)])
    madera.childs += [tronco1,tronco2] 

    hojas1 = sg.SceneGraphNode("hojas1")
    hojas1.transform = tr.matmul([tr.scale(0.15,0.15,0.15),tr.translate(1,1.6,1.5)])
    hojas1.childs += [gpuHojas2] 

    hojas2 = sg.SceneGraphNode("hojas2")
    hojas2.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(1.1,1.5,2)])
    hojas2.childs += [gpuHojas2] 

    hojas3 = sg.SceneGraphNode("hojas3")
    hojas3.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(1,0.5,1.6)])
    hojas3.childs += [gpuHojas2]

    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0.5)])
    hojas.childs += [hojas1, hojas2, hojas3] 

    arbol2 = sg.SceneGraphNode("arbol2")
    arbol2.transform = tr.matmul([tr.scale(0.6,0.6,0.6),tr.translate(0.4,0,-0.2)])
    arbol2.childs += [hojas,madera]

    return arbol2

def arbol3(pipeline): # tercer arbol que ahora es un verde más oscuro
    # toda la documentación de esta funcion se puede ver en arbol1

    Hojas3 = bs.Esfera2(1,50,50,41/255,129/255,56/255)
    gpuHojas3 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuHojas3)
    gpuHojas3.fillBuffers(Hojas3.vertices, Hojas3.indices, GL_STATIC_DRAW)

    Tronco = bs.createColorCube(87/255,51/255,4/255)
    gpuTronco = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTronco)
    gpuTronco.fillBuffers(Tronco.vertices,Tronco.indices, GL_STATIC_DRAW)



    tronco1 = sg.SceneGraphNode("tronco1")
    tronco1.transform = tr.matmul([tr.scale(0.05,0.05,0.5),tr.translate(3.5,-1.8,0.6)])
    tronco1.childs += [gpuTronco]

    tronco2 = sg.SceneGraphNode("tronco2")
    tronco2.transform = tr.matmul([tr.rotationX(np.pi/4),tr.scale(0.02,0.02,0.1),tr.translate(9,10,4)])
    tronco2.childs += [gpuTronco]

    madera = sg.SceneGraphNode("madera")
    madera.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0.32,0.15)])
    madera.childs += [tronco1,tronco2] 

    hojas1 = sg.SceneGraphNode("hojas1")
    hojas1.transform = tr.matmul([tr.scale(0.15,0.15,0.15),tr.translate(1,1.6,1.5)])
    hojas1.childs += [gpuHojas3] 

    hojas2 = sg.SceneGraphNode("hojas2")
    hojas2.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(1.1,1.5,2)])
    hojas2.childs += [gpuHojas3] 

    hojas3 = sg.SceneGraphNode("hojas3")
    hojas3.transform = tr.matmul([tr.scale(0.2,0.2,0.2),tr.translate(1,0.5,1.6)])
    hojas3.childs += [gpuHojas3]

    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0.5)])
    hojas.childs += [hojas1, hojas2, hojas3] 

    arbol3 = sg.SceneGraphNode("arbol2")
    arbol3.transform = tr.matmul([tr.scale(0.6,0.6,0.6),tr.translate(0.4,0.4,-0.2)])
    arbol3.childs += [hojas,madera]

    return arbol3

def bosque1(pipeline): # agrupacion de los 3 arboles previos en una configuracion

    # aqui tomo los 3 arboles
    arbol1_1 = arbol1(pipeline)
    arbol1_2 = arbol2(pipeline)
    arbol1_3 = arbol3(pipeline)

    #  los muevo los 3 arboles, los roto y los agrando/achico segun como me cante
    arbol1_1.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(1,1,0.8),tr.translate(0.15,0.15,0.04)]) #amarillo
    arbol1_2.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(1,1,1),tr.translate(0,0,0)]) # verde claro
    arbol1_3.transform = tr.matmul([tr.rotationZ(0),tr.scale(1,1,1.1),tr.translate(-0.1,-0.3,-0.02)]) # verde 
    
    #los uno a los 3 
    bosque1 = sg.SceneGraphNode("bosque1")
    bosque1.transform = tr.matmul([tr.scale(1.3,1.3,1.7),tr.translate(-3.8,-1,-0.2)])
    bosque1.childs += [arbol1_1,arbol1_2,arbol1_3]

    return bosque1

def bosque2(pipeline): # otra agrupacion de los 3 arboles previos en OTRA configuracion

    #aqui tomo los 3 arboles
    arbol1_1 = arbol1(pipeline)
    arbol1_2 = arbol2(pipeline)
    arbol1_3 = arbol3(pipeline)

    # les hago transformaciones arbitrarias
    arbol1_1.transform = tr.matmul([tr.rotationZ(0),tr.scale(1,1,1),tr.translate(0,0.1,0)]) #amarillo
    arbol1_2.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(1,1,1.2),tr.translate(-0.1,-0.05,-0.05)]) # verde claro
    arbol1_3.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(1,1,0.6),tr.translate(0.1,0,0.1)]) # verde 
    
    #los vuelvo a unir 
    bosque2 = sg.SceneGraphNode("bosque2")
    bosque2.transform = tr.matmul([tr.scale(1.2,1.15,1.4),tr.translate(-3,-1.2,-0.2)])
    bosque2.childs += [arbol1_1,arbol1_2,arbol1_3]

    return bosque2

def casa2(pipeline,image_muro,image_techo): # otra funcion de casa, pero ahora tiene 2 pisos en vez de 1
     # ESTA CASA va a tener: 1puerta, 4muros, 5 ventanas, 3 marcos alrededor de la puerta, 1 techo y uno foto de gato
    
    ## defino muro
    Muro = bs.createTextureCube(image_muro)
    gpuMuro = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuMuro)
    gpuMuro.texture = es.textureSimpleSetup(
        getAssetPath(image_muro), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuMuro.fillBuffers(Muro.vertices, Muro.indices, GL_STATIC_DRAW)

    ## defino puerta
    Puerta = bs.createTextureCube("puerta6.jpg")
    gpuPuerta = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPuerta)
    gpuPuerta.texture = es.textureSimpleSetup(
        getAssetPath("puerta6.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuPuerta.fillBuffers(Puerta.vertices, Puerta.indices, GL_STATIC_DRAW)

    ## defino ventana
    Ventana = bs.createTextureCube("ventana2.jpg")
    gpuVentana = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuVentana)
    gpuVentana.texture = es.textureSimpleSetup(
        getAssetPath("ventana2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuVentana.fillBuffers(Ventana.vertices, Ventana.indices, GL_STATIC_DRAW)

    ##defino techo
    Techo = bs.createTextureTriangle(image_techo)
    gpuTecho = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTecho)
    gpuTecho.texture = es.textureSimpleSetup(
        getAssetPath(image_techo), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuTecho.fillBuffers(Techo.vertices, Techo.indices, GL_STATIC_DRAW)

    ## defino foto de gato
    GATO = bs.createTextureQuad(1,1)
    gpuGATO = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGATO)
    gpuGATO.texture = es.textureSimpleSetup(
        getAssetPath("aleli.jpeg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuGATO.fillBuffers(GATO.vertices, GATO.indices, GL_STATIC_DRAW)

    gato1 = sg.SceneGraphNode("gato1") #derecha
    gato1.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(1,1,1),tr.translate(0,0,0.01)])
    gato1.childs += [gpuGATO]

    #paredes ( las primeras 4)
    pared1_1 = sg.SceneGraphNode("pared1_1") #derecha
    pared1_1.transform = tr.matmul([tr.scale(0.1,0.9,0.75),tr.translate(-4.5,0,0.5)])
    pared1_1.childs += [gpuMuro]

    pared1_2 = sg.SceneGraphNode("pared1_2") # izquierda
    pared1_2.transform = tr.matmul([tr.scale(0.1,0.9,0.75),tr.translate(4.5,0,0.5)])
    pared1_2.childs += [gpuMuro]

    pared1_3 = sg.SceneGraphNode("pared1_3") # arriba
    pared1_3.transform = tr.matmul([tr.scale(1,0.1,0.75),tr.translate(0,5,0.5)])
    pared1_3.childs += [gpuMuro]

    pared1_4 = sg.SceneGraphNode("pared1_4") # abajo
    pared1_4.transform = tr.matmul([tr.scale(1,0.1,0.75),tr.translate(0,-5,0.5)])
    pared1_4.childs += [gpuMuro]

    # uno las paredes del primer piso
    pared = sg.SceneGraphNode("pared")
    pared.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0.01)])
    pared.childs += [pared1_1,pared1_2,pared1_3,pared1_4]

    # las siguientes 4 paredes
    pared2_1 = sg.SceneGraphNode("pared2_1") #derecha
    pared2_1.transform = tr.matmul([tr.scale(0.1,0.9,0.75),tr.translate(-4.5,0,0.5)])
    pared2_1.childs += [gpuMuro]

    pared2_2 = sg.SceneGraphNode("pared2_2") # izquierda
    pared2_2.transform = tr.matmul([tr.scale(0.1,0.9,0.75),tr.translate(4.5,0,0.5)])
    pared2_2.childs += [gpuMuro]

    pared2_3 = sg.SceneGraphNode("pared2_3") # arriba
    pared2_3.transform = tr.matmul([tr.scale(1,0.1,0.75),tr.translate(0,5,0.5)])
    pared2_3.childs += [gpuMuro]

    pared2_4 = sg.SceneGraphNode("pared2_4") # abajo
    pared2_4.transform = tr.matmul([tr.scale(1,0.1,0.75),tr.translate(0,-5,0.5)])
    pared2_4.childs += [gpuMuro]

    # las uno y hago el segundo piso
    pared2 = sg.SceneGraphNode("pared")
    pared2.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0.76)])
    pared2.childs += [pared2_1,pared2_2,pared2_3,pared2_4]

    ## defino PUERTA
    # le voy a hacer un marco y finalmente un cubo con la textura

    marco1_1 = sg.SceneGraphNode("marco1_1") # IZQUIERDA
    marco1_1.transform = tr.matmul([tr.scale(0.01,0.05,1),tr.translate(20,0,0)])
    marco1_1.childs += [gpuMuro] # lo añado a gpu muro pq es tmb material madera

    marco1_2 = sg.SceneGraphNode("marco1_2") # derecha
    marco1_2.transform = tr.matmul([tr.scale(0.01,0.05,1),tr.translate(-20,0,0)])
    marco1_2.childs += [gpuMuro] # lo añado a gpu muro pq es tmb material madera

    marco1_3 = sg.SceneGraphNode("marco1_3") # arriba
    marco1_3.transform = tr.matmul([tr.scale(0.4,0.05,0.01),tr.translate(0,0,50)])
    marco1_3.childs += [gpuMuro] # lo añado a gpu muro pq es tmb material madera


    marco1 = sg.SceneGraphNode("marco1") # los 3 marcos juntos
    marco1.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0)])
    marco1.childs += [marco1_1,marco1_2,marco1_3] # lo añado a gpu muro pq es tmb material madera

    puerta1 = sg.SceneGraphNode("puerta1") #la puerta
    puerta1.transform = tr.matmul([tr.scale(0.4,0.05,1),tr.translate(0,0,0)])
    puerta1.childs += [gpuPuerta] # lo añado a gpu muro pq es tmb material madera

    puerta = sg.SceneGraphNode("puerta") # el conjunto
    puerta.transform = tr.matmul([tr.scale(0.4,0.3,0.3),tr.translate(0,1.85,0.5)])
    puerta.childs += [marco1,puerta1]


    # ventana 

    # 5 ventas, 1 arriba de la puerta, 2 juntos en el piso 1 y 2 juntas más en psio 2
    ventana1 = sg.SceneGraphNode("ventana1")
    ventana1.transform = tr.matmul([tr.scale(0.75,0.01,0.2),tr.translate(0,55,2.2)])
    ventana1.childs += [gpuVentana] 

    ventana2 = sg.SceneGraphNode("ventana2")
    ventana2.transform = tr.matmul([tr.scale(0.01,0.2,0.4),tr.translate(50,-1.5,1)])
    ventana2.childs += [gpuVentana] 

    ventana3 = sg.SceneGraphNode("ventana3")
    ventana3.transform = tr.matmul([tr.scale(0.01,0.2,0.4),tr.translate(50,1.5,1)])
    ventana3.childs += [gpuVentana] 

    ventana4 = sg.SceneGraphNode("ventana4")
    ventana4.transform = tr.matmul([tr.scale(0.01,0.2,0.4),tr.translate(-50,1.5,3)])
    ventana4.childs += [gpuVentana] 

    ventana5 = sg.SceneGraphNode("ventana5")
    ventana5.transform = tr.matmul([tr.scale(0.01,0.2,0.4),tr.translate(-50,-1.5,3)])
    ventana5.childs += [gpuVentana] 
    
    # uno todas las ventanas
    ventana = sg.SceneGraphNode("ventana")
    ventana.transform = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0)])
    ventana.childs += [ventana1,ventana2,ventana3,ventana4,ventana5]

    ## defino techo 
    # techo (piramide)
    techo1 = sg.SceneGraphNode("techo1")
    techo1.transform = tr.matmul([tr.scale(1,1,0.5),tr.translate(0,0,2.02)])
    techo1.childs += [gpuTecho]

    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.scale(1.2,1.2,1),tr.translate(0,0,0.75)])
    techo.childs += [techo1]



    #casa completa
    casa2 = sg.SceneGraphNode("casa2")
    casa2.transform = tr.matmul([tr.scale(0.5,0.5,0.5),tr.translate(0.5,0.5,0)])
    casa2.childs += [pared,pared2,puerta,ventana,techo,gato1]

    return casa2