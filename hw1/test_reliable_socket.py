import os
from reliable_socket import reliable_socket
import sys
import argparse
from struct import pack, unpack


def client(host, port):
    sock = reliable_socket()
    msg = sys.stdin.readline().strip()
    try:
        sock.sendto(msg.encode('utf-8'), (host, port))
    except RuntimeError:
        print("Didn't get acknowledgment.")


def server(host, port):
    sock = reliable_socket()
    sock.bind((host, port))
    print("listening on port %s" % port)
    while True:
        data, addr = sock.recvfrom(1024)
        print("received \"%s\" from %s" % (data.decode('utf-8'), addr))


if __name__ == '__main__':

    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser()
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('-i', type=str, default="",
                        help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', type=int, default=1060,
                        help='port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.i, args.p)
