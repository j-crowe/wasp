
class Peer(object):

    def __init__(self, sock, wasp, peer_id):
        self.sock = sock
        self.sock.setblocking(True)
        self.wasp = wasp
        self.id = peer_id
