# coding=utf-8
import numpy as np
import glfw
from OpenGL.GL import *
from gpu_shape import GPUShape
from easy_shaders import SimpleTransformShader
import transformations as tr
from Figuras_practicas import *
import sys
# py t1p1.py sys.argv -- nombre, iniciales, rut
# Diego DE 20665865
# print(sys.argv[0]
iniciales = sys.argv[2]
theta = ord(iniciales[0]) * ord(iniciales[1])
#theta = np.pi//2
vx = 350*np.cos(theta)
vy = 350*np.sin(theta)
bool = 0

class Movement:
    def __init__(self):
    # la velocidad se me hace demasiado rápida, por ahora será 1
        self.logo = objecto(0,0,vx,vy,bool,1,0,sys.argv[1],0)

    def getPos1(self):
        return (self.logo.x, self.logo.y)

    def update(self,dt):
        self.logo.update(dt)

    pass
class objecto:
    def __init__(self,x,y,velx,vely, bool,size,rand,color,rot):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.bool = bool
        self.size = size
        self.rand = rand
        self.color = color
        self.rot = rot
    def update(self,dt):
        self.updatePos(dt)
        self.switch()
        self.colorchange()

    def updatePos(self, dt):
        self.x += self.velx*dt/800 
        self.y += self.vely*dt/600
        S1 = (int(sys.argv[3])/20000000)**3
        S0 = 1
        if self.size == S0: # si es chiquito
            if self.x > 0.75:
                if self.velx < 0:
                    pass
                else:
                    self.boolchange()
                    self.colorcheck()
                    self.rotchange()
            elif self.x < -0.75:
                if self.velx > 0:
                    pass
                else:
                    self.boolchange()
                    self.colorcheck()
                    self.rotchange() 
                      
            elif self.y > 0.8:
                if self.vely < 0:
                    pass
                else:
                    self.boolchange()
                    self.colorcheck()
                    self.rotchange()

            elif self.y < -0.8:
                if self.vely > 0:
                    pass
                else:
                    self.boolchange()
                    self.colorcheck()
                    self.rotchange()

        else:
            if self.x > 0.75*S1:
                self.boolchange()
                self.colorcheck()
                self.rotchange()

            elif self.x < -0.75*S1:
                self.boolchange()
                self.colorcheck()
                self.rotchange()

            elif self.y > 0.8*S1:
                self.boolchange()
                self.colorcheck()
                self.rotchange()

            elif self.y < -0.8*S1:
                self.boolchange()
                self.colorcheck()
                self.rotchange()


    def switch(self):
        S0 = 1
        S1 = (int(sys.argv[3])/20000000)**3 # en el foro pidieron que Fuera asi 
        if self.bool == 0:
            self.size = S0
        else:
            self.size = S1
    def boolchange(self):
        if self.bool == 0:
            self.bool = 1
        elif self.bool == 1:
            self.bool = 0
    def colorcheck(self):
        if self.rand == 0 and np.random.randint(10) == 1:
            self.rand = 1
        elif self.rand == 1:
            self.rand = 0
    def rotchange(self):
            self.rot += np.pi/2
            (self.x,self.y) = (self.y,-self.x)
    def colorchange(self):
        if  self.rand == 1:
            self.color = "DAY"
        else:
            self.color = sys.argv[1]


movement = Movement()

def main():

    if not glfw.init():
        glfw.set_window_should_close(window, True)
        return -1

    width = 800
    height = 600
    window = glfw.create_window(width, height, "Tarea 1 parte 1: Salvapantallas DVD", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
        return -1

    glfw.make_context_current(window)

    pipeline = SimpleTransformShader()
    glUseProgram(pipeline.shaderProgram)

    t0 = glfw.get_time()
    while not glfw.window_should_close(window):
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        tuNombre = movement.logo.color
        lar = len(tuNombre)
        r = (ord(tuNombre[0%lar]) * ord(tuNombre[1%lar]) % 255) /255 # r: 
        g = (ord(tuNombre[2%lar]) * ord(tuNombre[3%lar]) % 255) /255 # g:
        b = (ord(tuNombre[4%lar]) * ord(tuNombre[5%lar]) % 255) /255 # b: 
        
        c1 = Cuadrilatero(10/255,10/255,10/255)
        gpuC1 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC1)
        gpuC1.fillBuffers(c1.vertexData, c1.indexData)

        c2 = Rectangulo(r,g,b)
        gpuC2 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC2)
        gpuC2.fillBuffers(c2.vertexData, c2.indexData)

        c3 = Letra_C(26,r,g,b)
        gpuC3 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC3)
        gpuC3.fillBuffers(c3.vertexData, c3.indexData)

        c4 = Letra_C(26,r,g,b)
        gpuC4 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC4)
        gpuC4.fillBuffers(c4.vertexData, c4.indexData)

        c5 = Rectangulo(r,g,b)
        gpuC5 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC5)
        gpuC5.fillBuffers(c5.vertexData, c5.indexData)

        c6 = Letra_C(26,r,g,b)
        gpuC6 = GPUShape().initBuffers()
        pipeline.setupVAO(gpuC6)
        gpuC6.fillBuffers(c6.vertexData, c6.indexData)
        
        glClearColor(0, 0, 0, 1.0)        
        glfw.poll_events()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glClear(GL_COLOR_BUFFER_BIT)
        # cuadrado
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.rotationZ(movement.logo.rot),
            tr.translate(movement.logo.x,movement.logo.y,0),
            tr.scale(movement.logo.size,movement.logo.size,0)
        ]))
        pipeline.drawCall(gpuC1)

        
        # el rectagulo de la D
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.scale(0.2, 0.2, 0.2),
            tr.rotationZ(movement.logo.rot),
            tr.rotationZ(-np.pi/2),
            tr.translate(0.0,-0.7,0.0),
            tr.translate(-5*movement.logo.y,5*movement.logo.x,0),
            tr.scale(movement.logo.size,movement.logo.size,0)
        ]))
        pipeline.drawCall(gpuC2)

        # La C más cercana
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.scale(0.2, 0.2, 0.2),
            tr.rotationZ(movement.logo.rot),
            tr.rotationZ(np.pi/2),
            tr.translate(0.0,-0.35,0.0),
            tr.translate(5*movement.logo.y,-5*movement.logo.x,0),
            tr.scale(movement.logo.size,movement.logo.size,0)
        ]))
        pipeline.drawCall(gpuC3)

        # la C más lejana
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.scale(0.2, 0.2, 0.2),
            tr.rotationZ(movement.logo.rot),
            tr.rotationZ(np.pi/2),
            tr.translate(0.0,-0.9,0.0),
            tr.translate(5*movement.logo.y,-5*movement.logo.x,0),
            tr.scale(movement.logo.size,movement.logo.size,0)
        ]))
        pipeline.drawCall(gpuC4)

        # el ractangulo de abajo
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.rotationZ(movement.logo.rot),
            tr.scale(0.4, 0.2, 0.2),
            tr.translate(0.0,-0.5,0.0),
            tr.translate(2.5*movement.logo.x,5*movement.logo.y,0),
            tr.scale(movement.logo.size,movement.logo.size,0)
        ]))
        pipeline.drawCall(gpuC5)

        # La C de la D
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.scale(0.2, 0.2, 0.2),
            tr.rotationZ(movement.logo.rot),
            tr.rotationZ(-np.pi/2),
            tr.translate(0.0,-0.7,0.0),
            tr.translate(-5*movement.logo.y,5*movement.logo.x,0),
            tr.scale(movement.logo.size,movement.logo.size,0)
        ]))
        pipeline.drawCall(gpuC6)
        glfw.swap_buffers(window)
        movement.update(dt)

    gpuC1.clear()
    gpuC2.clear()
    gpuC3.clear()
    gpuC4.clear()
    gpuC5.clear()
    gpuC6.clear()
    

    glfw.terminate()

    return 0

if __name__ == "__main__":
    main()
