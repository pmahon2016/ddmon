class Paul:

    def __init__(self):
        self.data = [1,2,4,5]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        reslt = self.data[self.index]
        self.index +=1

        return reslt
