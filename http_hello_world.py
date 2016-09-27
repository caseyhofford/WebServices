from wsgiref.simple_server import make_server
from wsgiref.util import request_uri
from my_class import *

def hello_world_app(environ, start_response):
    foo = Foo(request_uri(environ))
    uri = foo.cutContent()
    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')]  # HTTP Headers
    start_response(status, headers)

    return [b"Hello World, I also love " + uri.encode("utf-8")]

httpd = make_server('', 8000, hello_world_app)
print("Serving on port 8000...")
Foo(2)

# Serve until process is killed
httpd.serve_forever()
