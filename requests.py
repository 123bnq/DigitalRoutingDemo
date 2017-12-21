# request.py
# Request object


class Requests:

    def __init__(self, in_time, out_time, source, des, index):
        self.inTime = in_time
        self.outTime = out_time
        self.source = source
        self.des = des
        self.index = index
        self.isCall = 0
        self.__path = []
        self.__wl = 0

    def print_details(self):
        print("Index: ", self.index)
        # print("Incoming time: ", self.inTime)
        # print("Outgoing time: ", self.outTime)
        print("Source: ", self.source)
        print("Des: ", self.des)
        print("IsCall = ", self.isCall)
        if self.__path:
            print("Path: ", self.__path)

    def set_path(self, path):
        self.__path = path

    def get_path(self):
        return self.__path

    def set_wavelength(self, wl):
        self.__wl = wl

    def get_wavelength(self):
        return self.__wl