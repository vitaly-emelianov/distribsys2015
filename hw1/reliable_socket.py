import os
import socket
from struct import pack, unpack


PACKET_TYPE = {"MSG": b'\x00', "ACK": b'\x01'}


class reliable_socket:
    """Reliable socket class."""

    def __init__(self, timeout=2.0, delay=0.1):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = timeout
        self.delay = delay

    def generate_id(self):
        return os.urandom(4);

    def sendto(self, msg, address):
        self.packet_id = self.generate_id()
        prefix = pack('c4s', PACKET_TYPE["MSG"], self.packet_id)
        packet = prefix + msg
        self.udp_socket.sendto(packet, address)
        delay = self.delay
        while True:
            self.udp_socket.settimeout(delay)
            try:
                data = self.udp_socket.recv(5)
                packet = unpack('c4s', data[0:5])
                packet_type = packet[0]
                packet_id = packet[1]
                if packet_type == PACKET_TYPE["ACK"] and packet_id == self.packet_id:
                    return
            except socket.timeout:
                delay *= 2
                if delay > self.timeout:
                    raise RuntimeError('Connection is lost')

    def recvfrom(self, buffsize):
        data, address = self.udp_socket.recvfrom(buffsize)
        prefix = unpack('c4s', data[0:5])
        packet_id = prefix[1]
        acknowledgment = pack('c4s', PACKET_TYPE["ACK"], packet_id)
        self.udp_socket.sendto(acknowledgment, address)
        return (data[5:], address)

    def bind(self, address):
        return self.udp_socket.bind(address)
