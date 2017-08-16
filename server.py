import sys
import select
import socket
import errno
import logging

_logger = logging.getLogger("SERVER")

READ_BUFFER_SIZE = 1024


def _configure_logger():
    format = ('%(asctime)s %(levelname)s:%(name)s'
              ' %(filename)s:%(lineno)d  %(message)s')
    logging.basicConfig(format=format,
                        # filename='/tmp/echo-server.log',
                        level=logging.INFO)


def _read_socket(conn, addr):
    data = b''
    while True:
        try:
            chunk = conn.recv(READ_BUFFER_SIZE)
            if not chunk:
                return chunk

            data += chunk
        except OSError as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                # no more data available
                break
            else:
                _logger.error("Error reading socket address {}, error: "
                              .format(err))
                raise

    return data


class Server(object):

    def __init__(self, n_processor_threads=1):
        self._num_threads = n_processor_threads
        self._fds = {}    # fd -> (socket, address)
        self._listener_sock = None
        self._port = None
        self._poller = None

    def _process_data(self, conn, addr, data):
        _logger.info("Processing {} bytes of data for fd {} addr {}"
                     .format(len(data), conn.fileno(), addr))
        conn.sendall(data)

    def _handle_events(self, ready_list):
        listener_fd = self._listener_sock.fileno()
        for fd, event in ready_list:
            if fd == listener_fd:
                conn, addr = self._listener_sock.accept()
                _logger.info("New connection from {}".format(addr))
                self._fds[conn.fileno()] = (conn, addr)
                self._poller.register(conn.fileno(), select.POLLIN)
                continue

            conn, addr = self._fds[fd]
            if event & select.POLLIN:
                _logger.debug("Processing POLLIN for fd {} addr {}"
                              .format(fd, addr))
                data = _read_socket(conn, addr)
                if not data:
                    _logger.info("Connection closed for client {}"
                                 .format(addr))
                    del self._fds[fd]
                    self._poller.unregister(fd)
                    conn.close()
                    continue

                self._process_data(conn, addr, data)

            elif event & select.POLLHUP:
                _logger.debug("Processing POLLHUP for fd {} addr {}"
                              .format(fd, addr))
                del self._fds[fd]
                self._poller.unregister(fd)
                conn.close()
                _logger.info("Connection closed for client addr {}"
                             .format(addr))
            else:
                _logger.info("Unsupported event: {}".format(event))
                del self._fds[fd]
                self._poller.unregister(fd)
                conn.close()

    def run(self, port):
        if port < 0:
            raise ValueError("Port number must be positive")

        self._port = port

        self._poller = select.poll()

        _logger.info("Starting server...")

        self._listener_sock = socket.socket()
        self._listener_sock.setblocking(False)
        self._listener_sock.bind(('', port))

        _logger.info("Listening on port {}".format(port))

        self._listener_sock.listen()
        self._poller.register(self._listener_sock.fileno())

        while True:
            _logger.debug("Waiting for data...")
            ready_list = self._poller.poll()
            self._handle_events(ready_list)


if __name__ == "__main__":
    _configure_logger()
    argv = sys.argv
    if len(argv) == 1:
        print("Expect port number to accept connections.")
        exit(1)

    port = int(argv[1])
    server = Server()
    server.run(port)
