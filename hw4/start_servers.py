from server import Server
from coordinator import Coordinator


def start_servers():
    coord = Coordinator(('', 10000))
    coord.serve_forever()

    srv1 = Server(('', 10001))
    srv1.serve_forever()

    srv2 = Server(('', 10002))
    srv2.serve_forever()


if __name__ == '__main__':
    start_servers()
