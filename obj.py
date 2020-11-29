def try_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val

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
                    self.faces.append([list(map(try_int, face.split('/'))) for face in value.split(' ')])