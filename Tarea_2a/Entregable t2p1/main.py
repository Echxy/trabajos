# Diego Echeverria 

# IMPORTACIONES VARIAS
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
import modelos

# VARIABLES AUXILIARES
PROJECTION_ORTHOGRAPHIC = 0
PROJECTION_PERSPECTIVE = 2
n = 0 # MUY IMPORTANTES
m = 0 # MUY IMPORTANTES

# DATO: N y M son variables auxiliares que puedo cambiar a tiempo real mientras corre el modelo, con esto puedo llegar al valor final de la translación de cada casa mucho más rápido

class Controller: # movimiento de la camara
    def __init__(self): 
        self.projection = PROJECTION_ORTHOGRAPHIC
        #self.projection = PROJECTION_PERSPECTIVE
        self.theta = np.pi # angulo de donde miras
        self.phi = np.pi/2
        self.eye = [0, 0, 0.12] # donde esta la camara
        self.at = [0, 1, 0.1] # vector mirar
        self.up = [0, 0, 1] # vector que define el arriba

controller = Controller()

def on_key(window, key, scancode, action, mods): # cuando no se presione nada detenga los procesos
    global controller

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    


if __name__ == "__main__":

    if not glfw.init():
        glfw.set_window_should_close(window, True) #ventana
        # proporcion 16:9
    width = 1600
    height = 900

    window = glfw.create_window(width, height, "Tarea 2 parte 1: Suburbio nipon", None, None) 

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window) # recoger los inputs
    glfw.set_key_callback(window, on_key)

    pipeline = es.SimpleModelViewProjectionShaderProgram() #pipeline normal
    pipeline_tex = es.SimpleTextureModelViewProjectionShaderProgram() #pipeline tex

    # AQUI ESTAN TODOS LOS MODELOS 
    piso = modelos.piso_Floor(pipeline_tex)
    Calles = modelos.calles(pipeline_tex)
    Bosque1 = modelos.bosque1(pipeline)
    Bosque2 = modelos.bosque2(pipeline)
    Bosque3 = modelos.bosque1(pipeline)
    Bosque4 = modelos.bosque2(pipeline)
    Bosque5 = modelos.bosque1(pipeline)
    #PARA EL TEMA DE LAS CASAS VAMOS A CONTAR DE IZQUIERDA A DERECHA, ARRIBA A ABAJO SEGUN LA IMAGEN DE GOOGLE MAPS
    Casita = modelos.casa1(pipeline_tex,"casa1.jpg","techo2.jpg")
    Casita2 = modelos.casa2(pipeline_tex,"casa2.jpg","techo3.jpg")
    Casita3 = modelos.casa2(pipeline_tex,"casa3.jpg","techo4.jpg")
    Casita4 = modelos.casa2(pipeline_tex,"casa3.jpg","techo4.jpg")
    Casita5 = modelos.casa1(pipeline_tex,"casa4.jpg","techo5.jpg")
    Casita6 = modelos.casa2(pipeline_tex,"casa5.jpg","techo6.jpg")
    Casita7 = modelos.casa2(pipeline_tex,"casa6.jpg","techo10.jpg")
    Casita8 = modelos.casa2(pipeline_tex,"casa7.jpg","techo8.jpg")
    Casita9 = modelos.casa2(pipeline_tex,"casa8.jpg","techo9.jpg")
    Casita10 = modelos.casa2(pipeline_tex,"casa9.jpg","techo9.jpg")
    Casita11 = modelos.casa2(pipeline_tex,"casa9.jpg","techo9.jpg")
    Casita12 = modelos.casa2(pipeline_tex,"casa9.jpg","techo9.jpg")
    Casita13 = modelos.casa1(pipeline_tex,"casa3.jpg","techo10.jpg")
    Casita14 = modelos.casa2(pipeline_tex,"casa3.jpg","techo11.jpg") 
    Casita15 = modelos.casa2(pipeline_tex,"casa3.jpg","techo9.jpg") 
    Casita16 = modelos.casa2(pipeline_tex,"casa1.jpg","techo8.jpg") #
    Casita17 = modelos.casa2(pipeline_tex,"casa1.jpg","techo9.jpg") #
    Casita18 = modelos.casa2(pipeline_tex,"casa2.jpg","techo9.jpg") #
    Casita19 = modelos.casa2(pipeline_tex,"casa10.jpg","techo9.jpg") #
    Casita20 = modelos.casa2(pipeline_tex,"casa10.jpg","techo12.jpg") #
    Casita21 = modelos.casa2(pipeline_tex,"casa3.jpg","techo8.jpg") #
    Casita22 = modelos.casa2(pipeline_tex,"casa3.jpg","techo9.jpg") #

    

    

    glClearColor(0.85, 0.85, 0.85, 1.0)
    glEnable(GL_DEPTH_TEST)



    #TOMAR EL TIEMPO
    t0 = glfw.get_time()
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # TODAS LAS TECLAS QUE HACEN ALGO

        # PROJECCIONES ORTO A PERSPECTIVA CON 1 Y 2
        if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS:
            controller.projection = PROJECTION_ORTHOGRAPHIC
        
        if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS:
            controller.projection = PROJECTION_PERSPECTIVE
        
        # N Y M PARA SUBIR Y BAJAR N  
        #if glfw.get_key(window, glfw.KEY_N) == glfw.PRESS:
        #    n+= 1*dt
        #if glfw.get_key(window, glfw.KEY_M) == glfw.PRESS:
        #    n-= 1*dt
        
        # K Y L para subir y bajar M
        #if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
        #    m+= 1*dt
        #if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
        #    m-= 1*dt

        # A y D hacen rotan la camara en el plano xy
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            controller.theta += 3 * dt

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            controller.theta -= 3 * dt

        # W Y s HACEN AVANZAR Y RETROCEDER en la direccion donde estas mirando ( tmb  mueve donde miras para no darte vuelta)
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            controller.eye += (controller.at - controller.eye) * 2*dt
            controller.at += (controller.at - controller.eye) * 2*dt

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            controller.eye -= (controller.at - controller.eye) * 2*dt
            controller.at -= (controller.at - controller.eye) * 2*dt
        
        # R y T suben y bajan en el eje Z ( tmb  mueve donde miras para no darte vuelta)
        if glfw.get_key(window, glfw.KEY_R) == glfw.PRESS:
           controller.eye[2] += controller.up[2] * dt
           controller.at[2]  += controller.up[2] * dt

        if glfw.get_key(window, glfw.KEY_T) == glfw.PRESS:
           controller.eye[2] -= controller.up[2] * dt
           controller.at[2]  -= controller.up[2] * dt

        # Z y X rotan el plano xy sobre Z 
        if glfw.get_key(window, glfw.KEY_Z) == glfw.PRESS:
            controller.phi += 2 * dt
        
        if glfw.get_key(window, glfw.KEY_X) == glfw.PRESS:
            controller.phi -= 2 * dt

        # esto evita que me salga de los bordes
        if controller.eye[2] < 0.12:
            controller.eye[2] = 0.12
        if controller.eye[1] > 2:
            controller.eye[1] =2
        if controller.eye[1] < -2:
            controller.eye[1] = -2
        if controller.eye[0] > 2:
            controller.eye[0] =2
        if controller.eye[0] < -6:
            controller.eye[0] = -6

        # las coordenadas de la posicion de la camara
        at_x = controller.eye[0] + np.cos(controller.theta) *np.sin(controller.phi)
        at_y = controller.eye[1] + np.sin(controller.theta) *np.sin(controller.phi)
        at_z = controller.eye[2] + np.cos(controller.phi)
        
        controller.at = np.array([at_x, at_y, at_z])

        # dependiendo de la projeccion me dice que view y projection usar
        if controller.projection == PROJECTION_PERSPECTIVE: 
            projection = tr.perspective(60, float(width)/float(height), 0.1, 100)
            view = tr.lookAt(controller.eye, controller.at, controller.up)

        elif controller.projection == PROJECTION_ORTHOGRAPHIC:
            projection = tr.ortho(-7.4,3.1,-4,2,0.1,100) #izq, der, arriba, abajo, near, far
            view = tr.lookAt(
            np.array([0,0.9,3]), #eye
            np.array([0, 1, 0]), # at
            np.array([0, 0, 1])  # up
            )

        # hacer print a estos valores para saber al final cual es la posicion final donde quieres dejar el modelo
        #print(n,"n")
        #print(m,"m")
        glUseProgram(pipeline.shaderProgram)
       
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)


        
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # todos los moviemientos de los bosques
        Bosque2.transform = tr.translate(-3.25,-1.55,-0.18)
        Bosque5.transform = tr.matmul([tr.rotationZ(np.pi/40),tr.scale(1.1,1.05,1.3),tr.translate(-4.75,-0.1,-0.2)]) # viene de bosque 1
        Bosque4.transform = tr.matmul([tr.rotationZ(np.pi/40),tr.scale(1.05,1.1,1.2),tr.translate(-4.6,0.4,-0.2)]) # viene de bosque 2
        Bosque3.transform = tr.matmul([tr.rotationZ(np.pi/40),tr.scale(1.05,1.01,1.4),tr.translate(-5.0,1.6,-0.2)]) # viene de bosque 1
        # orden a dibujarlos todos
        sg.drawSceneGraphNode(Bosque1, pipeline, "model")
        sg.drawSceneGraphNode(Bosque2, pipeline, "model")
        sg.drawSceneGraphNode(Bosque3, pipeline, "model")
        sg.drawSceneGraphNode(Bosque4, pipeline, "model")
        sg.drawSceneGraphNode(Bosque5, pipeline, "model")
        
        #cambio a las texturas
        glUseProgram(pipeline_tex.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_tex.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(pipeline_tex.shaderProgram, "view"), 1, GL_TRUE, view)   

        #Casita.transform = tr.matmul([tr.rotationZ(0),tr.scale(1,1,1),tr.translate(0,0,0)])   
        # las 22 transformaciones para dejar las casas similarmente a las del google mpas
        Casita.transform = tr.matmul([tr.rotationZ(np.pi*-0.24),tr.scale(1.03,0.645,0.6),tr.translate(-2.55,-4.93,0)])
        Casita2.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.6,0.45,0.4),tr.translate(-6.81,3.167,0)])
        Casita3.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.4,0.4,0.4),tr.translate(3.65,8.25,0)])   
        Casita4.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.4,0.6,0.4),tr.translate(-6.94,2.23,0)])   
        Casita5.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.6,0.4,0.4),tr.translate(2.26,5.693,0)])   
        Casita6.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.6,0.6,0.6),tr.translate(-2.72,1.72,0)])  
        Casita7.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.4,0.65,0.4),tr.translate(2.31,5.31,0)])  
        Casita8.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(0.8,0.6,0.4),tr.translate(3.13,-0.727,0)])   
        Casita9.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(0.6,0.6,0.4),tr.translate(2.7,0.23,0)]) 
        Casita10.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.6,0.5,0.4),tr.translate(-1.09,2.53,0)])
        Casita11.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.6,0.6,0.4),tr.translate(0.14,1.09,0)])
        Casita12.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(0.8,0.8,0.5),tr.translate(1.15,1.37,0)]) 
        Casita13.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.5,0.5,0.5),tr.translate(0.08,2.54,0)])   
        Casita14.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.5,0.7,0.4),tr.translate(1.38,1.34,0)])   
        Casita15.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.5,0.5,0.4),tr.translate(2.71,2.50,0)])   
        Casita16.transform = tr.matmul([tr.rotationZ(np.pi/2),tr.scale(0.6,0.5,0.4),tr.translate(0.31,-0.12,0)])   
        Casita17.transform = tr.matmul([tr.rotationZ(0),tr.scale(0.5,0.5,0.4),tr.translate(1.44,-0.212,0)])   
        Casita18.transform = tr.matmul([tr.rotationZ(-np.pi/2),tr.scale(0.5,0.5,0.4),tr.translate(-0.95,2.69,0)])   
        Casita19.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(0.6,0.6,0.4),tr.translate(-0.01,1.62,0)])   
        Casita20.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(0.5,0.5,0.4),tr.translate(-1.4,2.23,0)])   
        Casita21.transform = tr.matmul([tr.rotationZ(-np.pi/2),tr.scale(0.5,0.5,0.4),tr.translate(0.567,2.7,0)])   
        Casita22.transform = tr.matmul([tr.rotationZ(-np.pi/2),tr.scale(0.5,0.5,0.4),tr.translate(2.1,2.7,0)])   

        # oden a dibujar las 22 casas
        sg.drawSceneGraphNode(piso, pipeline_tex, "model")
        sg.drawSceneGraphNode(Calles, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita2, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita3, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita4, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita5, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita6, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita7, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita8, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita9, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita10, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita11, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita12, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita13, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita14, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita15, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita16, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita17, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita18, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita19, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita20, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita21, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita22, pipeline_tex, "model")


        glfw.swap_buffers(window)
    glfw.terminate()