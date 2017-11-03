class Requests:

    def __init__(self, in_time, out_time, source, des, index):
        self.inTime = in_time
        self.outTime = out_time
        self.source = source
        self.des = des
        self.index = index
        self.isCall = 0
        self.path = []

    def printDetails(self):
        print("Index: ", self.index)
        print("Incoming time: ", self.inTime)
        print("Outgoing time: ", self.outTime)
        print("Source: ", self.source)
        print("Des: ", self.des)
        print("IsCall = ", self.isCall)
        if self.path:
            print("Path: ", self.path)