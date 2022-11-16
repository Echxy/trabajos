# Diego Echeverria
import glfw
from OpenGL.GL import *
import numpy as np

import basic_shapes as bs
import easy_shaders as es
import transformations as tr
from assets_path import getAssetPath #para la textura


# función auxiliar hecha para ahorrar lineas, crea la gpu shape
def createGPUShape(shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

#class Esfera:
#    def __init__(self,posicion,velocidad):
# el largo del cubo es 1, ya que fue hecho de -0.5 a 0.5
class Esfera:
    def __init__(self,x,y,z,vx,vy):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy 
        self.vz = 0  # inicia de el reposo vertical
        self.az = -9.8 # gravedad

    def update(self, dt): # funcion para actualizar 
        self.updatePos(dt)
        self.updateVel(dt)
        self.colisiones_borde()

    def updatePos(self, dt): # cambios en la posicion
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.z += self.vz*dt

    def updateVel(self, dt): # cambios en la velocidad
        self.vz += dt*self.az

    def colisiones_borde(self): # revisar si una pelota chocha con cualquier borde segun su radio
    # X AXIS
        if self.x + 0.1 > 0.5:
            self.vx = -abs(self.vx)
        if self.x < 0.1 -0.5:
            self.vx = abs(self.vx)
        # Y AXIS
        if self.y +0.1 > 0.5:
            self.vy = -abs(self.vy)
        if self.y < 0.1 -0.5:
            self.vy = abs(self.vy)
        # Z AXIS
        if self.z +0.1 > 0.5:
            self.z += -0.01 # sacarlo de la colision del techo
            self.vz = 0 # techo
        if self.z < 0.1 -0.5:
            self.vz = abs(self.vz)

class Controller: #esta clase hará el 90% del trabajo
    def __init__(self):
        self.camera = [4,0,0.5,0] # la dimension adiccional es para multiplicarlo con la rotacion luego, eliminar el valor de sobra
        self.theta = 0 #(2/15)*np.pi
        self.phi = 0 # valor vertical(2/15)*np.pi # funcion adicional creada para revisar las colisiones
        self.direccion = 0 #variables para iniciar y detener el movimiento de la camara
        self.direccion2 = 0
        self.e1 = Esfera(0,0,0.3*1,0.3,0.26) # ( uso wolfram para los valores)
        self.e2 = Esfera(0.3,0.1,0.3*1,0.15,0.37) # Segun el aux la posicion inicial es libre 
        self.zoom = 30
    
    def update(self,dt,): # funciones que se deben actualizar
        self.camera_rot()
        self.pointer(dt)
        self.pointer2(dt)
        self.e1.update(dt)
        self.e2.update(dt)
        self.colider(self.e1,self.e2)

    def camera_rot(self): # multiplicación para la rotacion de la camara
        return tr.matmul([tr.rotationY(self.phi),tr.rotationZ(self.theta),self.camera])
       
    def pointer(self,dt):  # funciones pointer que son afectadas con el toque de las teclas
        if self.direccion == -1:
           self.theta += -1*(2/15)*np.pi*dt
        if self.direccion == 1:
           self.theta += 1*(2/15)*np.pi*dt
        if self.direccion == 2:
            self.zoom += 10*dt
        if self.direccion == 3:
            self.zoom += -10*dt
    def pointer_change(self,point): # el "puente" entre la clase y el KEY_press
        self.direccion = point
    
    def pointer2(self,dt): # una segunda version redundante de la primera
        if self.direccion2 == -1:
            self.phi += -1*(2/15)*np.pi*dt
        if self.direccion2 == 1:
            self.phi += 1*(2/15)*np.pi*dt
        if self.direccion2 == 2:
            self.phi = 0
            self.theta = 0
        if self.direccion2 == 3:
            self.zoom = 30
    def pointer2_change(self,point): # el "puente" entre la clase y el KEY_press
        self.direccion2 = point

    def colision_check(self,es1,es2): #revisa cuando una colision es cierta entra las dos bolas
        dist = [es1.x-es2.x,es1.y-es2.y]
        norma = np.sqrt(dist[0]**2 + dist[1]**2)
        # siendo la suma de los radios 0.1 + 0.1 = 0.28
        return norma < 0.21
    
    def colision_obj(self,es1,es2): # colision entre las dos bolas, como deben reaccionar y su pega con el momentum
        dist = [es1.x-es2.x,es1.y-es2.y]
        norma = np.sqrt(dist[0]**2 + dist[1]**2)
        normal = dist/norma

        es1aNormal = np.dot([es2.vx,es2.vy],normal) < 0 # angulo de choque
        es2aNormal = np.dot([es1.vx,es1.vy],normal) < 0

        if not (es1aNormal and es2aNormal):
            tan = np.array([np.cos(np.pi/2)*normal[0] - np.sin(np.pi/2)*normal[1],
                    np.sin(np.pi/2)*normal[0] + np.cos(np.pi/2)*normal[1]])
            
            v1n = np.dot([es1.vx,es1.vy], normal) * normal
            v1t = np.dot([es1.vx,es1.vy], tan) * tan

            v2n = np.dot([es2.vx,es2.vy], normal) * normal
            v2t = np.dot([es2.vx,es2.vy], tan) * tan

            [es1.vx,es1.vy] = v2n + v1t # cambio de momentum
            [es2.vx,es2.vy] = v1n + v2t
    
    def colider(self,es1,es2):  # si hay colision, has el cambio de momemtum
        if self.colision_check(es1 , es2):
            self.colision_obj(es1 , es2)



controller = Controller() # activa la clase

def on_key(window, key, scancode, action, mods): # cuando no se presione nada detenga los procesos
    global controller

    if action != glfw.PRESS:
        controller.pointer_change(0)
        controller.pointer2_change(0)
        return 
    
  

if __name__ == "__main__":

    if not glfw.init():
        glfw.set_window_should_close(window, True) #ventana
        # proporcion 16:9
    width = 1600
    height = 900

    window = glfw.create_window(width, height, "Tarea 1 parte 2: Beach Ball", None, None) 

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    glfw.set_key_callback(window, on_key)

    pipeline = es.SimpleModelViewProjectionShaderProgram() #pipeline normal

    # Textura ####
    pipelinetextura = es.SimpleTextureTransformShaderProgram() #pipeline de las texturas
    ##############################

    glClearColor(0.15, 0.15, 0.15, 1.0)
    glEnable(GL_DEPTH_TEST)

    glUseProgram(pipeline.shaderProgram)
    #TODAS LAS FIGURAS
    Cubito = createGPUShape(bs.createRainbowCube())
    Arista1 = createGPUShape(bs.createRainbowCube())
    Arista2 = createGPUShape(bs.createRainbowCube())
    Arista3 = createGPUShape(bs.createRainbowCube())
    Arista4 = createGPUShape(bs.createRainbowCube())
    Arista5 = createGPUShape(bs.createRainbowCube())
    Arista6 = createGPUShape(bs.createRainbowCube())
    Arista7 = createGPUShape(bs.createRainbowCube())
    Arista8 = createGPUShape(bs.createRainbowCube())
    Arista9 = createGPUShape(bs.createRainbowCube())
    Arista10 = createGPUShape(bs.createRainbowCube())
    Arista11 = createGPUShape(bs.createRainbowCube())
    Arista12 = createGPUShape(bs.createRainbowCube())

    
    Esfera = createGPUShape(bs.Esfera(1,200,200))
    Esfera2 = createGPUShape(bs.Esfera(1,200,200))

    # textura ###############################
    gatito = bs.createTextureQuad(1,1)
    gpugatito= es.GPUShape().initBuffers()
    pipelinetextura.setupVAO(gpugatito)
    gpugatito.fillBuffers(gatito.vertices, gatito.indices, GL_STATIC_DRAW)
    gpugatito.texture = es.textureSimpleSetup(getAssetPath("gatitoo.jpg"),GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    gatito2 = bs.createTextureQuad(1,1)
    gpugatito2= es.GPUShape().initBuffers()
    pipelinetextura.setupVAO(gpugatito2)
    gpugatito2.fillBuffers(gatito2.vertices, gatito2.indices, GL_STATIC_DRAW)
    gpugatito2.texture = es.textureSimpleSetup(getAssetPath("Gato_jaja.jpg"),GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    gatito3 = bs.createTextureQuad(1,1)
    gpugatito3= es.GPUShape().initBuffers()
    pipelinetextura.setupVAO(gpugatito3)
    gpugatito3.fillBuffers(gatito3.vertices, gatito3.indices, GL_STATIC_DRAW)
    gpugatito3.texture = es.textureSimpleSetup(getAssetPath("el_gatoo.jpg"),GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

    gatito4 = bs.createTextureQuad(1,1)
    gpugatito4= es.GPUShape().initBuffers()
    pipelinetextura.setupVAO(gpugatito4)
    gpugatito4.fillBuffers(gatito3.vertices, gatito3.indices, GL_STATIC_DRAW)
    gpugatito4.texture = es.textureSimpleSetup(getAssetPath("aleli.jpeg"),GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)


    ######################################################





    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
 
        glfw.poll_events()

        #TIEMPO
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        controller.update(dt)
        #TODOS LOS KEY PRESS ####################
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            controller.pointer_change(-1)

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            controller.pointer_change(1)

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            controller.pointer2_change(-1)

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            controller.pointer2_change(1)

        if (glfw.get_key(window, glfw.KEY_P) == glfw.PRESS):
            controller.pointer2_change(2)
        
        if (glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS):
            controller.pointer_change(2)

        if (glfw.get_key(window, glfw.KEY_W) == glfw.PRESS):
            controller.pointer_change(3)
        
        if (glfw.get_key(window, glfw.KEY_O) == glfw.PRESS):
            controller.pointer2_change(3)
        ####################################################
        # la proyección
        projection = tr.perspective(controller.zoom, float(width) / float(height), 0.1, 100)
        # la camara
        view = tr.lookAt(controller.camera_rot()[:-1],np.array([0, 0, 0]),np.array([0, 0, 1]))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # usando el pipeline normal hago todo esto
        glUseProgram(pipeline.shaderProgram)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)


        # LOS EJES X ############################################################################################################################
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0,-0.5,-0.5),tr.scale(1,0.05,0.05)]))
        pipeline.drawCall(Arista1)
        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0.5,-0.5),tr.scale(1,0.05,0.05)]))
        pipeline.drawCall(Arista2)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0,-0.5,0.5),tr.scale(1,0.05,0.05)]))
        pipeline.drawCall(Arista3)
    
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0,0.5,0.5),tr.scale(1,0.05,0.05)]))
        pipeline.drawCall(Arista4)
        # lOS EJES Y #####################################################################################################################
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0.5,0,0.5),tr.scale(0.05,1,0.05)]))
        pipeline.drawCall(Arista5)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-0.5,0,0.5),tr.scale(0.05,1,0.05)]))
        pipeline.drawCall(Arista6)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0.5,0,-0.5),tr.scale(0.05,1,0.05)]))
        pipeline.drawCall(Arista7)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-0.5,0,-0.5),tr.scale(0.05,1,0.05)]))
        pipeline.drawCall(Arista8)
        #  LOS EJES Z #################################################################################################################################
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0.5,-0.5,0),tr.scale(0.05,0.05,1)]))
        pipeline.drawCall(Arista9)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-0.5,-0.5,0),tr.scale(0.05,0.05,1)]))
        pipeline.drawCall(Arista10)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0.5,0.5,0),tr.scale(0.05,0.05,1)]))
        pipeline.drawCall(Arista11)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(-0.5,0.5,0),tr.scale(0.05,0.05,1)]))
        pipeline.drawCall(Arista12)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.scale(1,1,1))
        pipeline.drawCall(Cubito, GL_LINES)
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(controller.e1.x,controller.e1.y,controller.e1.z), 
        tr.scale(0.1,0.1,0.1)]))
        pipeline.drawCall(Esfera)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(controller.e2.x,controller.e2.y,controller.e2.z), 
        tr.scale(0.1,0.1,0.1)]))
        pipeline.drawCall(Esfera2)

        glClear(GL_DEPTH_BUFFER_BIT)

        ################################## INICIIO DE LAS TEXTURAS
        zgato = controller.zoom/30
        # uso el otro pipeline
        glUseProgram(pipelinetextura.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipelinetextura.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
             tr.translate(-0.7, -0.5, 0),
             tr.scale(0.5*zgato, 0.5*zgato, 1.0)]))

        pipelinetextura.drawCall(gpugatito)

        glUseProgram(pipelinetextura.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipelinetextura.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
             tr.translate(0.7, -0.5, 0),
             tr.scale(0.5*zgato, 0.5*zgato, 1.0)]))
        pipelinetextura.drawCall(gpugatito2)

        glUseProgram(pipelinetextura.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipelinetextura.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
             tr.translate(0.7, 0.5, 0),
             tr.scale(0.5*zgato, 0.5*zgato, 1.0)]))
        pipelinetextura.drawCall(gpugatito3)

        glUseProgram(pipelinetextura.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipelinetextura.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
             tr.translate(-0.7, 0.5, 0),
             tr.scale(0.5*zgato, 0.5*zgato, 1.0)]))
        pipelinetextura.drawCall(gpugatito4)

        glfw.swap_buffers(window)

gpugatito.clear()
gpugatito2.clear()
gpugatito3.clear()
gpugatito4.clear()
Cubito.clear()
Esfera.clear()
glfw.terminate()