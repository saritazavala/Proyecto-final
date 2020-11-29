from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np
import pygame
from obj import Obj
import shaders

class Model(object):
    def __init__(self, filename, textureName, scale):
        self.model = Obj(filename)
        self.createVertBuffer()
        self.texture_surf = pygame.image.load(textureName)
        self.texture_data = pygame.image.tostring(self.texture_surf, "RGB", 1)
        self.texture = glGenTextures(1)

        self.position = glm.vec3(0,0,1)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(scale,scale,scale)
    
    def getMatrix(self):
        i = glm.mat4(1)
        trans = glm.translate(i, self.position)
        pitch = glm.rotate(i, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians(self.rotation.z), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, self.scale)
        return trans * rotate * scale

    def createVertBuffer(self):
        buffer = []
        for face in self.model.faces:
            for i in range(3):
                #verts
                buffer.append(self.model.vertices[face[i][0] - 1][0])
                buffer.append(self.model.vertices[face[i][0] - 1][1])
                buffer.append(self.model.vertices[face[i][0] - 1][2])
                buffer.append(1)

                #norms
                buffer.append(self.model.normales[face[i][2] - 1][0])
                buffer.append(self.model.normales[face[i][2] - 1][1])
                buffer.append(self.model.normales[face[i][2] - 1][2])
                buffer.append(0)

                #texcoords
                buffer.append(self.model.texcoords[face[i][1] - 1][0])
                buffer.append(self.model.texcoords[face[i][1] - 1][1])

        self.vertBuffer = np.array( buffer, dtype=np.float32)

    def renderInScene(self):
        
        VBO = glGenBuffers(1) #Vertex Buffer Object
        VAO = glGenVertexArrays(1) #Vertex Array Object

        glBindVertexArray(VAO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes, self.vertBuffer, GL_STATIC_DRAW)

        # Atributo de posicion de vertices
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Atributo de normal de vertices
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 4))
        glEnableVertexAttribArray(1)

        ## Atributo de uvs de vertices
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 8))
        glEnableVertexAttribArray(2)

        # Dar textura
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.texture_surf.get_width(), self.texture_surf.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3)

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        no, no, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.temp = 0

        self.eye = glm.vec3(0,0,-1)
        
        self.modelList = []
        self.active_model = 0

        self.camPos = glm.vec3(0,0,3)
        self.camRot = glm.vec3(0,0,0)

        self.pointLight = glm.vec4(0,0,0,0)

        self.projectionMatrix = glm.perspective(glm.radians(60), self.width/self.height, 0.1, 100)

    def render(self):
        glClearColor(0.5, 0.5, 0.5, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.active_shader:
            self.getViewMatrix()
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr(self.view))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform4f(glGetUniformLocation(self.active_shader, "light"),
                        self.pointLight.x, self.pointLight.y, self.pointLight.z, self.pointLight.w)

            glUniform4f(glGetUniformLocation(self.active_shader, "color"), 1, 1, 1, 1)

            # Para un modelo en especifico
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"), 1, GL_FALSE,
                               glm.value_ptr(self.modelList[self.active_model].getMatrix()))

        self.modelList[self.active_model].renderInScene()

    def getViewMatrix(self):
        i = glm.mat4(1)
        camTranslate = glm.translate(i, self.camPos - self.eye)
        camPitch = glm.rotate(i, glm.radians( self.camRot.x ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( self.camRot.y ), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( self.camRot.z ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll

        self.view = glm.inverse( camTranslate * camRotate )

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    #Activacion y asignacion de shaders
    def setShaders(self, vertexShader, fragShader):

        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)


