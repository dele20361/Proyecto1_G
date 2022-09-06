import struct

class Texture(object):
    def __init__(self, filename):

        #Open file 
        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            #Convertions to make it leible to python 
            image.seek(18)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            #List to save data of every color 
            self.pixels = []

            for y in range(self.height):
                pixelRow = []

                #Cycle to convert data to a type aceptable 
                #cycle to read image 
                for x in range(self.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    pixelRow.append([r,g,b])

                self.pixels.append(pixelRow)

    def getColor(self, u, v):
        if 0 <= u < 1 and 0 <= v < 1:
            return self.pixels[int(v * self.height)][int(u * self.width)]
        else:
            return None





