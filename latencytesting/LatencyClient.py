import json
import socket
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


def encode_and_timestamp(message):
    message['sent_t'] = time.time()
    return json.dumps(message)


class LatencyClient:
    def __init__(self, server_addresses, port, c_id, n_messages=1000, delta=0.5):
        self.connections = []
        self.server_addresses = server_addresses
        self.port = port
        self.client_id = c_id
        self.n_messages = n_messages
        self.delta = delta
        self.logger = logging.getLogger('LatencyClient')

    def make_connections(self, server_addresses, port):
        sockets = []
        for address in server_addresses:
            connected = False
            while not connected:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((address, port))
                    sockets.append(s)
                    connected = True
                except Exception as e:
                    self.logger.debug(f"Client {self.client_id}: {e}")
                    self.logger.warning(f"Client {self.client_id}: failed to connect with {address}, retrying")
                    time.sleep(self.delta)
        return sockets

    def broadcast(self, message: dict):
        for connection in self.connections:
            m = encode_and_timestamp(message).encode()
            connection.send(m)

    def start(self):
        for i in range(self.n_messages):
            self.connections = self.make_connections(self.server_addresses, self.port)
            message = {
                'c_id': self.client_id,
                'm_id': i,
            }
            self.broadcast(message)
            self.cleanup()
            time.sleep(self.delta)
        self.cleanup()

    def cleanup(self):
        for connection in self.connections:
            try:
                connection.close()
            except BrokenPipeError:
                pass
