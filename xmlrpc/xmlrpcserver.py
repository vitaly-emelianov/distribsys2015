from SimpleXMLRPCServer import SimpleXMLRPCServer

def div(a, b):
    return a // b

server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")
server.register_function(div, "div")
server.serve_forever()