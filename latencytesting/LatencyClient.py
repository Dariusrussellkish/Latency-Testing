import json
import socket
import time
import logging
import random
from latencytesting.parameters import PARAMS

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


def encode_and_timestamp(message):
    message['sent_t'] = time.time()
    return json.dumps(message)


class LatencyClient:
    def __init__(self, server_addresses, port, c_id,
                 n_messages=1000,
                 delta=0.5,
                 max_random_latency=0.002,
                 message_size=PARAMS):
        self.connections = []
        self.server_addresses = server_addresses
        self.port = port
        self.client_id = c_id
        self.n_messages = n_messages
        self.delta = delta
        self.logger = logging.getLogger('LatencyClient')
        self.max_random_latency = max_random_latency
        self.message_size = message_size

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
            m = encode_and_timestamp(message).rjust(self.message_size.MESSAGE_SIZE).encode('utf-8')
            assert len(m) == self.message_size.MESSAGE_SIZE
            delay = random.uniform(0., self.max_random_latency)
            time.sleep(delay)
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
