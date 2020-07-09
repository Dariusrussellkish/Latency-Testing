import logging
import sys
import time
import json
import socketserver
from latencytesting.parameters import PARAMS

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


class LatencyRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('LatencyRequestHandler')
        self.message_size = PARAMS
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self) -> None:
        data = self.request.recv(self.message_size.MESSAGE_SIZE).strip()
        data = json.loads(data)
        received_time = time.time()
        self.logger.debug(f"{self.server.server_address[0]} received client: {data['c_id']} "
                          f"message: {data['m_id']} sent at {data['sent_t']} from {self.client_address[0]} "
                          f"on {received_time}")
        return
