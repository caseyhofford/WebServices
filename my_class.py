#!/usr/bin/python3
import pprint
#def return_requested_string(input):

#class Foo:
#def __init__(self, uri):
#    self.uri = uri
#    #print(self.uri)


def cutContent(uri):
    print('[my_class:12] ' + uri + '[/]')
    out = uri[22:]
    print('[my_class:14] ' + out + '[/]')
    return out
