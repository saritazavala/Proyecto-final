class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines = file.read().splitlines()
        
        self.vertices = []
        self.normales = []
        self.texcoords = []
        self.faces = []
        self.read()
    
    def read(self):
        for line in self.lines:
            if line:
                prefix, value = line.split(' ', 1)
                if prefix == 'v':
                    self.vertices.append(list(map(float, value.split(' '))))
                elif prefix == 'vn':
                    self.normales.append(list(map(float, value.split(' '))))
                elif prefix == 'vt':
                    self.texcoords.append(list(map(float, value.split(' '))))
                elif prefix == 'f':
                    vertices = value.split(' ')
                    if vertices[len(vertices)-1] == '':
                        vertices.pop()
                    self.faces.append([list(map(int, vert.split('/'))) for vert  in vertices])