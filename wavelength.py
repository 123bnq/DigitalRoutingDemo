# wavelength.py
# provide a several methods to manipulate the wavelength of optical fiber


class Wavelength:
    def __init__(self):
        self.w = [2]*8

    def get_data(self):
        return self.w

    def get_wavelength(self, index):
        return self.w[index]

    def use_wavelength(self, index):
        if self.w[index] > 0:
            self.w[index] -= 1

    def release_wavelength(self, index):
        if self.w[index] < 2:
            self.w[index] += 1