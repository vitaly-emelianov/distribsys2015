import argparse
from xmlrpc.server import SimpleXMLRPCServer


class Server:

    def __init__(self, address):
        self._rpc_methods_ = ['get', 'put', 'put_back', 'tick', 'keys']
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

    def get(self, key):
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value

    def put_back(self, key, value):
        pass

    def tick(self):
        pass

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._serv.serve_forever()

# Example
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int, help='port on localhost')
    port = parser.parse_args().port
    kvserv = Server(('', port))
    kvserv.serve_forever()