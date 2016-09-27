#def return_requested_string(input):

class Foo:
    def __init__(self, uri):
        self.uri = uri
        #print(self.uri)


    def cutContent(self):
        out = self.uri[22:]
        print(out)
        return out
