class Wavelength:
    def __init__(self):
        self.w = [2]*8

    def getWavelength(self, index):
        return self.w[index]

    def setWavelength(self, index):
        if self.w[index] == 0:
            return -1
        else:
            self.w[index] -= 1

