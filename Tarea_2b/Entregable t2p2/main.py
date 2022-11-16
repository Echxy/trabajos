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
import lighting_shaders as ls
from assets_path import getAssetPath
import Auxiliar_funciones as Ax
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import modelos

# VARIABLES AUXILIARES
PROJECTION_ORTHOGRAPHIC = 0
PROJECTION_PERSPECTIVE = 2
n = 0 # MUY IMPORTANTES
m = 0 # MUY IMPORTANTES
b = 0 # MUY IMPORTANTES
v = 0 # MUY IMPORTANTES
luces = 0 
contador = 0
angulo = 0
sol = [244/255, 233/255, 155/255]
luna = [79/255,105/255,155/255]

# DATO: N y M son variables auxiliares que puedo cambiar a tiempo real mientras corre el modelo, con esto puedo llegar al valor final de la translación de cada casa mucho más rápido
class Movement: #movimiento del tiempo 
    def __init__(self,luces,contador,angulo):
        self.contador = contador # contador para las luces
        self.angle = angulo # angulo del sol y luna
        self.luz = luces # cashea cuando es 0
        self.sol = sol # estado de luz del sol
        self.luna = [0,0,0] # estado de luz de la luna (inicial)
        self.hora = 12 # hora incial del dia
        self.reloj = 0 # un contador que suma horas

    def update(self,dt): # funcion para actualizar 
        self.counter(dt) # mueve el tiempo
        self.rotador() # rota los cuerpos 
        self.luces_changer(dt) # enciende y apaga luces

    def luces_changer(self,dt): # define las horas del dia donde se prenden y apagan luces
        if 46 > self.contador > 45:
            self.apagar(dt)
        if 16 > self.contador > 15:
            self.encender(dt)

    def apagar(self,dt): # apagar es: apagar los focos, desactivar el sol, activar la luna
        self.luz -= dt
        self.sol = sol
        self.luna = [0,0,0]
        if self.luz < 0: # para no pasarse, pq el cambio de los focos es gradual
            self.luz = 0

    def encender(self,dt): # encender es: encender los focos, activar el sol y desactivar la luna
        self.luz += dt
        self.sol = [0,0,0]
        self.luna = luna
        if self.luz > 1: # para no pasarse, pq el cambio de los focos es gradual
            self.luz = 1
        
    
    def counter(self,dt): # cuenta el tiempo que se tarda un ciclo, 
        self.contador += dt # avanzar
        self.reloj += dt # avanza el reloj
        self.contador = self.contador % 60 # este va a hacer el limite de tiempo
        if 61/24 > self.reloj> 60/24: # cuando pase una hora
            self.reloj = 0 # reinicia el reloj
            self.hora += 1 # cambia la hora
            print("son las " + str(self.hora) +":00") # y avisa por consola 
            if self.hora == 23: # loopea
                self.hora = -1
                
    def rotador(self):
        N = 2*np.pi/60 # separo el ciruclo en particion
        counter = self.contador # este va a ser la rotacion
        self.angle = N*counter

movement = Movement(luces,contador,angulo)

class Controller: # movimiento de la camara
    def __init__(self): 
        self.fillPolygon = True # este es auxiliar
        self.projection = PROJECTION_ORTHOGRAPHIC
        #self.projection = PROJECTION_PERSPECTIVE
        self.theta = np.pi # angulo de donde miras
        self.phi = np.pi/2
        self.eye = [0, 0, 0.12] # donde esta la camara
        self.at = [0, 1, 0.1] # vector mirar
        self.up = [0, 0, 1] # vector que define el arriba

# CLASE DE LUZ USADA POR EL AUXILIAR, TIENE TODAS SUS CARACTERISTICAS
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0

# ACTIVA EL CONTROLLER
controller = Controller()
# DEFINE EL POOL COMO UN DICCIONARIO
spotlightsPool = dict()



# LO DE LAS TECLAS, EL ESPACIO ESTA EN QUE LO TIENES QUE MANTENER
def on_key(window, key, scancode, action, mods): # cuando no se presione nada detenga los procesos
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    if action != glfw.PRESS and action != glfw.REPEAT:
        return

# DEFINE DOLOROSAMENTE CADA LUZ DE LAS 8 INDIVIDUALMENTE
# AMBIENT SIEMPRE 0, PQ AFECTA DEMASIADO
# DIFFUSE LO VARIO HARTO, PERO EL VALOR INICIAL NO IMPORTA
# AFECTO LAS POSICIONES INICIALES Y DIRECCION NOMAS
# PARA SOL Y LUNA LOS ANGULOS DE LUZ SON MÁS GRANDES 60 RAD
def setLights():
    #TAREA4: Primera luz spotlight # SOL
    spot1 = Spotlight()
    spot1.ambient = np.array([0.0, 0.0, 0.0])
    spot1.diffuse = np.array([1,0,0])  #valores googleados 244/255, 233/255, 155/255
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = 1.0
    spot1.linear = 0.09
    spot1.quadratic = 0.032
    spot1.position = np.array([0, 0, 7]) #TAREA4: esta ubicada en esta posición
    spot1.direction = np.array([0, 0, -1]) #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot1.cutOff = np.cos(np.radians(60)) #TAREA4: corte del ángulo para la luz
    spot1.outerCutOff = np.cos(np.radians(60)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['spot1'] = spot1 #TAREA4: almacenamos la luz en el diccionario, con una clave única

    #TAREA4: Segunda luz spotlight #LUNA
    spot2 = Spotlight()
    spot2.ambient = np.array([0.0, 0.0, 0.0])
    spot2.diffuse = np.array([0,0,1]) #valores googleados 79/255, 105/255, 136/255
    spot2.specular = np.array([1.0, 1.0, 1.0])
    spot2.constant = 1.0
    spot2.linear = 0.09
    spot2.quadratic = 0.032
    spot2.position = np.array([0, 0, -7]) #TAREA4: Está ubicada en esta posición
    spot2.direction = np.array([0, 0, 1]) #TAREA4: también apunta hacia abajo
    spot2.cutOff = np.cos(np.radians(60))
    spot2.outerCutOff = np.cos(np.radians(60)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot2'] = spot2 #TAREA4: almacenamos la luz en el diccionario

    #TAREA5: Luces spotlights para los faros de los autos AUTO IZQ
    # tr.translate(1.798,-0.902,0)
    spot3 = Spotlight()
    spot3.ambient = np.array([0, 0, 0])
    spot3.diffuse = np.array([1, 0, 0])
    spot3.specular = np.array([1.0, 1.0, 1.0])
    spot3.constant = 1.0
    spot3.linear = 0.09
    spot3.quadratic = 0.032
    spot3.position = np.array([-0.55,-0.08,0.5]) # posición inicial b,n,m
    spot3.direction = np.array([1, 0, 0]) # dirección inicial
    spot3.cutOff = np.cos(np.radians(12.5)) 
    spot3.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot3'] = spot3 #TAREA4: almacenamos la luz en el diccionario
  
    spot4 = Spotlight()  # LUZ AUTO DERECHA
    spot4.ambient = np.array([0, 0, 0])
    spot4.diffuse = np.array([0, 1, 0])
    spot4.specular = np.array([1.0, 1.0, 1.0])
    spot4.constant = 1.0
    spot4.linear = 0.09
    spot4.quadratic = 0.032
    spot4.position = np.array([-0.55,0.12,0.5])
    spot4.direction = np.array([1, 0, 0])
    spot4.cutOff = np.cos(np.radians(12.5))
    spot4.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot4'] = spot4 #TAREA4: almacenamos la luz en el diccionario   

    spot5 = Spotlight() # POSTE 1 izq arriba
    spot5.ambient = np.array([0, 0, 0])
    spot5.diffuse = np.array([0,0,0])
    spot5.specular = np.array([1.0, 1.0, 1.0])
    spot5.constant = 1.0
    spot5.linear = 0.09
    spot5.quadratic = 0.032
    spot5.position = np.array([0,0,2]) #2.10, 0.15, 4.8
    spot5.direction = np.array([0, 0, -1]) 
    spot5.cutOff = np.cos(np.radians(12.5)) 
    spot5.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot5'] = spot5 #TAREA4: almacenamos la luz en el diccionario

    spot6 = Spotlight() # POSTE 2
    spot6.ambient = np.array([0, 0, 0])
    spot6.diffuse = np.array([0,0,0])
    spot6.specular = np.array([1.0, 1.0, 1.0])
    spot6.constant = 1.0
    spot6.linear = 0.09
    spot6.quadratic = 0.032
    spot6.position = np.array([0, 0, 2]) 
    spot6.direction = np.array([0, 0, -1]) 
    spot6.cutOff = np.cos(np.radians(12.5))
    spot6.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot6'] = spot6 #TAREA4: almacenamos la luz en el diccionario

    spot7 = Spotlight() # POSTE 3
    spot7.ambient = np.array([0, 0, 0])
    spot7.diffuse = np.array([0,0,0])
    spot7.specular = np.array([1.0, 1.0, 1.0])
    spot7.constant = 1.0
    spot7.linear = 0.09
    spot7.quadratic = 0.032
    spot7.position = np.array([0, 0, 2])
    spot7.direction = np.array([0, 0, -1]) 
    spot7.cutOff = np.cos(np.radians(12.5)) 
    spot7.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot7'] = spot7 #TAREA4: almacenamos la luz en el diccionario

    spot8 = Spotlight() # POSTE 4
    spot8.ambient = np.array([0, 0, 0])
    spot8.diffuse = np.array([0,0,0])
    spot8.specular = np.array([1.0, 1.0, 1.0])
    spot8.constant = 1.0
    spot8.linear = 0.09
    spot8.quadratic = 0.032
    spot8.position = np.array([0, 0, 2]) 
    spot8.direction = np.array([0, 0, -1]) 
    spot8.cutOff = np.cos(np.radians(12.5))
    spot8.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot8'] = spot8 #TAREA4: almacenamos la luz en el diccionario 


#TAREA4: modificamos esta función para poder configurar todas las luces del pool
# ESTO SETEA LAS LUCES CON LAS PROYECCIONES, ESTA CASI SIN TOCAR 
# HACE FUNCIONAR LAS LUCES CON LOS MATERIALES EN LOS 2 PIPELINE QUE OCUPAN LUCES
def setPlot(texPipeline,pipeline,lightPipeline):
  
    glUseProgram(pipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    #TAREA4: Como tenemos 2 shaders con múltiples luces, tenemos que enviar toda esa información a cada shader
    #TAREA4: Primero al shader de color
    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    #TAREA4: Enviamos la información de la luz puntual y del material
    #TAREA4: La luz puntual está desactivada por defecto (ya que su componente ambiente es 0.0, 0.0, 0.0), pero pueden usarla
    # para añadir más realismo a la escena
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "material.shininess"), 32)

    #TAREA4: Aprovechamos que las luces spotlight están almacenadas en el diccionario para mandarlas al shader
    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), 0.09)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), 0.032)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    #TAREA4: Ahora repetimos todo el proceso para el shader de texturas con mútiples luces
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

    for i, (k,v) in enumerate(spotlightsPool.items()):
        baseString = "spotLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), 0.09)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), 0.032)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)


if __name__ == "__main__":

    if not glfw.init():
        glfw.set_window_should_close(window, True) #ventana
        # proporcion 16:9
    width = 1600
    height = 900

    window = glfw.create_window(width, height, "Tarea 2 parte 2: Toyko drift", None, None) 

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window) # recoger los inputs
    glfw.set_key_callback(window, on_key)

    # NUEVOS PIPELINES
    pipeline = es.SimpleModelViewProjectionShaderProgram() #pipeline normal
    pipeline_tex = ls.MultipleLightTexturePhongShaderProgram() #pipeline tex
    lightPipeline = ls.MultipleLightPhongShaderProgram() #pipeline de luces

    
    setLights()
    # AQUI ESTAN TODOS LOS MODELOS 
    piso = modelos.piso_Floor(pipeline_tex)
    Calles = modelos.calles(pipeline_tex)
    Bosque1 = modelos.bosque1(lightPipeline)
    Bosque2 = modelos.bosque2(lightPipeline)
    Bosque3 = modelos.bosque1(lightPipeline)
    Bosque4 = modelos.bosque2(lightPipeline)
    Bosque5 = modelos.bosque1(lightPipeline)
    Cubito = modelos.cubo_coord(lightPipeline)

    # Modelos Nuevos########################
    Floppa = modelos.floppita(pipeline_tex)
    Car = modelos.createCarScene(lightPipeline)
    poste1 = modelos.poste(pipeline_tex) #ARRIBA IZQ
    poste2 = modelos.poste(pipeline_tex) #ARRIBA DER
    poste3 = modelos.poste(pipeline_tex) #ABAJO IZQ
    poste4 = modelos.poste(pipeline_tex) #ABAJO DER
    ##################################
    
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


    glClearColor(0.1, 0.1, 0.1, 1.0) # LO HICE OSCURO PARA QUE SE NOTEN LAS LUCES, ME GUSTA MÁS ASI
    glEnable(GL_DEPTH_TEST)
    #TOMAR EL TIEMPO
    t0 = glfw.get_time()
    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    #LUCES  # ANOTO TODAS SUS POSICIONES 
    light1pos = np.append(spotlightsPool['spot1'].position, 1)
    light2pos = np.append(spotlightsPool['spot2'].position, 1)
    light3pos = np.append(spotlightsPool['spot3'].position, 1)
    light4pos = np.append(spotlightsPool['spot4'].position, 1)
    light5pos = np.append(spotlightsPool['spot5'].position, 1)
    light6pos = np.append(spotlightsPool['spot6'].position, 1)
    light7pos = np.append(spotlightsPool['spot7'].position, 1)
    light8pos = np.append(spotlightsPool['spot8'].position, 1)

    # ANOTO LAS DIRECCIONES DE LAS LUCES QUE VOY A CAMBIAR: SOL,LUNA Y LOS 2 FOCOS DEL AUTO
    dir_inicial1 = np.append(spotlightsPool['spot1'].direction, 1)
    dir_inicial2 = np.append(spotlightsPool['spot2'].direction, 1)
    dir_inicial3 = np.append(spotlightsPool['spot3'].direction, 1)
    dir_inicial4 = np.append(spotlightsPool['spot4'].direction, 1)

    ###################################
    # STEP HACE AVANZAR LOS DATOS EN EL SPLINE
    # LOOPS HACE QUE SE NECESITEN VARIAS VUELTAS AL WHILE PARA UN CAMBIO DE STEP
    step = 0
    loops = 0
    while not glfw.window_should_close(window):
        # DATOS DEL SPLINE ##########################################################################################
        # EL FORMATO ES:
        # PUNTOS = [INICIAL,FINAL,PUNTO DE CONTROL DEL FINAL, PUNTO DE CONTROL DEL INICIAL]
        # LOS PUNTOS DE CONTROL SON TANGENTES AL FINAL, SIRVEN COMO "LA DIRECCION FINAL QUE MIRA EL AUTO EN EL SPLINE"
        puntos_arriba = [[1.28,1.84,1],[-5.192,1.53,1],[6.25,-1.847,1],[10.36,1.429,1]]
        puntos_izq = [[-5.192,1.52,1],[-1.5,-1.85,1],[1.32,0.189,1],[-15.314,11.812,1]]
        puntos_der = [[1.872,-1.45,1],[1.3,1.84,1],[-2.83,-0.786,1],[1.143,-18.346,1]]
        puntos_abajo = [[-1.5,-1.85,1],[1.872,-1.5,1],[-1.25,1.08,1],[-19.77,-2.44,1]] 
        # JUNTO LOS 4 SPLINE
        puntos = [puntos_abajo,puntos_der,puntos_arriba,puntos_izq]
        spline_mov = []
        spline_angle = []
        N = 100 # 100 PARTICIONES
        # CREO LOS MODELOS PARA VERLOS (ESTA DESACTIVADO)
        spline_ver = modelos.VerSpline(puntos_abajo,pipeline,1,0,0)
        spline_ver2 = modelos.VerSpline(puntos_der,pipeline,0,1,0)
        spline_ver3 = modelos.VerSpline(puntos_arriba,pipeline,0,0,1)
        spline_ver4 = modelos.VerSpline(puntos_izq,pipeline,1,1,1)
        # CON EL FOR LOS UNO
        for i in range(4):
            #print(puntos[i])
            spline, move,angle = bs.CatmullRom(puntos[i], N,0,0,0)
            for j in range(2*(N-1)): # EL -1 ES PQ EL ULTIMO DATO DEL SPLINE CON EL PRIMERO DE SIGUIENTE EXPLOTAN TONTO
                spline_mov.append(move[j])
            for k in range(N-1): # EL -1 ES PQ EL ULTIMO DATO DEL SPLINE CON EL PRIMERO DE SIGUIENTE EXPLOTAN TONTO
                spline_angle.append(angle[k])

        ###############################################################################################################################
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        movement.update(dt) # ACTIVAR EL TIEMPO
        loops += 1 # DI UNA VUELTA

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # TODAS LAS TECLAS QUE HACEN ALGO

        # PROJECCIONES ORTO A PERSPECTIVA CON 1 Y 2
        if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS:
            controller.projection = PROJECTION_ORTHOGRAPHIC
        
        if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS:
            controller.projection = PROJECTION_PERSPECTIVE
        
        # N Y M PARA SUBIR Y BAJAR N  
        if glfw.get_key(window, glfw.KEY_N) == glfw.PRESS:
            n+= 1*dt
        if glfw.get_key(window, glfw.KEY_M) == glfw.PRESS:
            n-= 1*dt
        
        # K Y L para subir y bajar M
        if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
            m+= 1*dt
        if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
            m-= 1*dt

        # O y P PARA MOVER B
        if glfw.get_key(window, glfw.KEY_O) == glfw.PRESS:
            b+= 1*dt
        if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
            b-= 1*dt
        # OTRA VARIABLE AUXILIAR
        if glfw.get_key(window, glfw.KEY_H) == glfw.PRESS:
            v+= 1*dt
        if glfw.get_key(window, glfw.KEY_G) == glfw.PRESS:
            v-= 1*dt
        # CON LAS 4 VARIABLES AUXILIARES PUDE CAMBIAR EN VIVO LOS DOS PUNTOS DE CONTROL DEL SPLINE

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
        #print(b,"b")
        #print(b,"b:x",n,"n:y","ini")
        #print(v,"v:x",m,"m:y","fin")
        #print(step)
        #print(movement.contador)
        setPlot(pipeline_tex,pipeline,lightPipeline)

        # AQUI DEBERIA VER EL SPLINE QUE HICE #############################################################################
        glUseProgram(pipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        # VISION DE LOS SPLINES Y SUS MATMUL PARA LEVANTARLOS DEL PISO (DESACTIVADOS)

        # spline_ver.transform = tr.matmul([tr.translate(0,0,0.1)])
        # spline_ver2.transform = tr.matmul([tr.translate(0,0,0.1)])
        # spline_ver3.transform = tr.matmul([tr.translate(0,0,0.1)])
        # spline_ver4.transform = tr.matmul([tr.translate(0,0,0.1)])
        # sg.drawSceneGraphNode(spline_ver, pipeline, "model")
        # sg.drawSceneGraphNode(spline_ver2, pipeline, "model")
        # sg.drawSceneGraphNode(spline_ver3, pipeline, "model")
        # sg.drawSceneGraphNode(spline_ver4, pipeline, "model")
        

        # ###########################################################################################



        glUseProgram(lightPipeline.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        # ESTO ESTABA SOLO PARA VER MÁS FACILMENTE LAS SPLINES
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # todos los moviemientos de los bosques
        Bosque2.transform = tr.translate(-3.25,-1.55,-0.18)
        Bosque5.transform = tr.matmul([tr.rotationZ(np.pi/40),tr.scale(1.1,1.05,1.3),tr.translate(-4.75,-0.1,-0.2)]) # viene de bosque 1
        Bosque4.transform = tr.matmul([tr.rotationZ(np.pi/40),tr.scale(1.05,1.1,1.2),tr.translate(-4.6,0.4,-0.2)]) # viene de bosque 2
        Bosque3.transform = tr.matmul([tr.rotationZ(np.pi/40),tr.scale(1.05,1.01,1.4),tr.translate(-5.0,1.6,-0.2)]) # viene de bosque 1
        # CUBITO ES UN HEROES, ES UN TRABAJADOR DE MEDIO TIEMPO QUE ME AYUDO A ENCONTRAR TODAS LAS COORDENADAS DE LOS PUNTOS DE LAS SPLINES
        #Cubito.transform = tr.matmul([tr.translate(b,n,0)])
        
        # orden a dibujarlos todos
        sg.drawSceneGraphNode(Bosque1, lightPipeline, "model")
        sg.drawSceneGraphNode(Bosque2, lightPipeline, "model")
        sg.drawSceneGraphNode(Bosque3, lightPipeline, "model")
        sg.drawSceneGraphNode(Bosque4, lightPipeline, "model")
        sg.drawSceneGraphNode(Bosque5, lightPipeline, "model")
        #sg.drawSceneGraphNode(Cubito,  lightPipeline, "model")
        
        

        # INVOCO AL ALUTO Y LE HAGO FIND NODE PARA TRANSFORMARLO
        sg.drawSceneGraphNode(Car, lightPipeline, "model")
        Auto = sg.findNode(Car,'system-car')

        # ESTO ES UN TRANSLATE DEL SPLINE, LA DIRECCION DEL SPLINE, Y UNA ROTACION INICIAL PARA ORIENTARLO
        Auto.transform = tr.matmul([tr.translate(spline_mov[step], spline_mov[step+1], 0), 
        tr.rotationZ(spline_angle[step//2]),tr.rotationZ(np.pi/2)]) # -1.834,0.983,-0.015

        # matmul de las luces del auto 
        # ESTO TAMBIEN ES TRANSLACION Y ROTACION DEL SPLINE Y LA ROTACION 0 ES PQ POR EL AUTO SE ROTO NP.PI/2 Y POR LAS LUCES SE ROTO -NP.PI/2
        # DEJE EL 0 PARA ACORDARME DE ESTE HECHO
        posicion_transform = tr.matmul([tr.translate(spline_mov[step],spline_mov[step+1] ,0),
                                        tr.rotationZ(spline_angle[step//2]),    
                                        tr.rotationZ(0)])
        # APLICO LAS TRANSFORMACIONES A LA POSICION                               
        posicion3 = tr.matmul([posicion_transform, light3pos])
        posicion4 = tr.matmul([posicion_transform, light4pos])
        spotlightsPool['spot3'].position = posicion3
        spotlightsPool['spot4'].position = posicion4

        # CAMBIO LA DIRECCION A LA QUE MIRAN LOS FOCOS
        direccion3 = tr.matmul([tr.rotationZ(spline_angle[step//2]),tr.rotationZ(0), dir_inicial3])
        direccion4 = tr.matmul([tr.rotationZ(spline_angle[step//2]),tr.rotationZ(0), dir_inicial4])
        spotlightsPool['spot3'].direction = direccion3
        spotlightsPool['spot4'].direction = direccion4

        # Esto hace que cada 3 while se avanza un step
        if loops > 3:
            step = step + 2
            loops = 0
            if step >= 8*N-8:
                step = 0
        
        ######################################################################################################################################
        ###################################################### SOL Y LUNA ####################################################################
        # DATOS DE MOVIMIENTO DEL SOL Y LA  LUNA
        posicion1 = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0),tr.rotationY(movement.angle),light1pos])
        posicion2 = tr.matmul([tr.scale(1,1,1),tr.translate(0,0,0),tr.rotationY(movement.angle),light2pos])
        direccion1 = tr.matmul([tr.rotationY(movement.angle), dir_inicial1])
        direccion2 = tr.matmul([tr.rotationY(movement.angle), dir_inicial2])
        spotlightsPool['spot1'].direction = direccion1
        spotlightsPool['spot2'].direction = direccion2
        spotlightsPool['spot1'].position = posicion1
        spotlightsPool['spot2'].position = posicion2
        # COLOR DE LA LUZ
        diff_sol = movement.sol
        diff_luna = movement.luna
        diffuse_off = np.array([0,0,0]) # DIFFUSE AUXILIARES DE CUANDO ALGO SALE ALGO MAL
        diffusered = np.array([1,0,0]) # lo uso para ver que luz es cual
        diffusergreen = np.array([0,1,0]) # lo uso para ver que luz es cual
        # CAMBIO EL COLOR
        spotlightsPool['spot1'].diffuse = diff_sol
        spotlightsPool['spot2'].diffuse = diff_luna
        
        ######################################## TRANSFORMACIONES DE LAS LUCES (QUE NO SON DEL AUTO)##########################################
        posicion5 = tr.matmul([tr.scale(1,1,1),tr.translate(-5.106,1.7,-0.7368),light5pos]) #POSTE 1
        posicion6 = tr.matmul([tr.scale(1,1,1),tr.translate(1.822,1.7,-1.116),light6pos]) #POSTE 2  
        posicion7 = tr.matmul([tr.scale(1,1,1),tr.translate(-1.728,-1.541,-1),light7pos]) #POSTE 3  
        posicion8 = tr.matmul([tr.scale(1,1,1),tr.translate(1.851,-1.562,-1),light8pos]) #POSTE 4
        # COLOR DEL AUTO Y LOS FOCOS 
        diffuser_auto = np.array([movement.luz,movement.luz,0])
        diffuser = np.array([movement.luz,movement.luz,movement.luz])

        # LES DOY LOS VALORES 
        spotlightsPool['spot5'].position = posicion5
        spotlightsPool['spot6'].position = posicion6
        spotlightsPool['spot7'].position = posicion7
        spotlightsPool['spot8'].position = posicion8

        # LES DOY LOS COLORES
        spotlightsPool['spot3'].diffuse = diffuser_auto
        spotlightsPool['spot4'].diffuse = diffuser_auto
        spotlightsPool['spot5'].diffuse = diffuser
        spotlightsPool['spot6'].diffuse = diffuser
        spotlightsPool['spot7'].diffuse = diffuser
        spotlightsPool['spot8'].diffuse = diffuser

        ######################################################################################################################################
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
        # POSTES 
        poste1.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(1,1,1),tr.translate(4.723,-1.633,0)]) # ARRIBA IZQ
        poste2.transform = tr.matmul([tr.rotationZ(0),tr.scale(1,1,1),tr.translate(1.617,1.638,0)]) # ARRIBA DER
        poste3.transform = tr.matmul([tr.rotationZ(np.pi),tr.scale(1,1,1),tr.translate(1.502,1.534,0)]) # ABAJO IZQ
        poste4.transform = tr.matmul([tr.rotationZ(0),tr.scale(1,1,1),tr.translate(1.620,-1.568,0)]) # ABAJO DER

        # oden a dibujar las 22 casas
        #sg.drawSceneGraphNode(Floppa, pipeline_tex, "model")
        sg.drawSceneGraphNode(piso, pipeline_tex, "model")
        sg.drawSceneGraphNode(Calles, pipeline_tex, "model")
        sg.drawSceneGraphNode(Casita, pipeline_tex, "model")
        sg.drawSceneGraphNode(poste1, pipeline_tex, "model") #ARRIBA IZQ
        sg.drawSceneGraphNode(poste2, pipeline_tex, "model") #ARRIBA DER
        sg.drawSceneGraphNode(poste3, pipeline_tex, "model") #ABAJO IZQ
        sg.drawSceneGraphNode(poste4, pipeline_tex, "model") #ABAJO DER
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

#
        glfw.swap_buffers(window)
    glfw.terminate()