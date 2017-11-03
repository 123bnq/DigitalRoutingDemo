class Wavelength:
    def __init__(self):
        self.w = [2]*8

    def get_wavelength(self, index):
        return self.w[index]

    def use_wavelength(self, index):
        if self.w[index] == 0:
            return -1
        else:
            self.w[index] -= 1

    def release_wavelength(self, index):
        if self.w[index] < 2:
            self.w[index] += 1