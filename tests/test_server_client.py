import pytest
from latencytesting.LatencyServer import LatencyRequestHandler
from latencytesting.LatencyClient import LatencyClient
import socketserver
import threading
import logging
import time

server_ips = ['127.0.0.1', '127.0.0.2', '127.0.0.3']
port = 8090

logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s: %(message)s',
                    )


def test_setup():
    logger = logging.getLogger('Setup-Test')
    print()
    servers = []
    for s_ip in server_ips:
        server = socketserver.TCPServer((s_ip, port), LatencyRequestHandler)
        t = threading.Thread(target=server.serve_forever)
        t.setDaemon(True)
        t.start()
        servers.append((server, t))

    clients = []
    for i in range(5):
        client = LatencyClient(server_ips, port, i)
        t = threading.Thread(target=client.start)
        t.start()
        clients.append((client, t))

    for client, t in clients:
        t.join()
        client.cleanup()

    logger.debug(f"All clients are done, shutting down servers")

    for server, t in servers:
        server.shutdown()
        server.socket.close()


def test_production():
    logger = logging.getLogger('Setup-Production')
    print()
    server = socketserver.TCPServer(('localhost', port), LatencyRequestHandler)
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()

    time.sleep(30)

    clients = []
    for i in range(5):
        client = LatencyClient(server_ips, port, i)
        t = threading.Thread(target=client.start)
        t.start()
        clients.append((client, t))

    for client, t in clients:
        t.join()
        client.cleanup()

    logger.debug(f"All clients are done, shutting down servers")

    time.sleep(10)
    server.shutdown()
    server.socket.close()