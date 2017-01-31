from bencode import bencode
from hashlib import md5, sha1
import requests
import random
import socket

import utils
import peer as pr

CLIENT_NAME = 'wasptorret'
VERSION_NUM = '0001'
CLIENT_ID = 'WS'


class Wasp(object):
    """DESC: A wasp is a single instance of a torrent.
    Includes all metadata and functionality in seeding/leeching"""

    def __init__(self, meta_data):
        # TODO: Handle non-existant vars appropriately
        self.announce = meta_data[b'announce']
        self.piece_length = meta_data[b'info'][b'piece length']
        self.pieces = meta_data[b'info'][b'pieces']
        self.info_hash = sha1(bencode(meta_data[b'info'])).digest()
        self.name = meta_data[b'info'][b'name']
        self.peer_id = ''
        # TODO: Only works on single file torrents
        file = meta_data[b'info'][b'files'][0]
        self.length = file[b'length']
        self.peer_dict = {}

    def generate_peer_id(self):
        """DESC: Generate unique wasp peer id.
        Used as standard in bittorrent protocol."""

        wasp_random = str(random.randint(100000000000, 999999999999))
        return ('-' + CLIENT_ID + VERSION_NUM + '-' + wasp_random).encode()

    def generate_handshake(self):
        """DESC: Generates and returns initial bit torrent handshake"""

        protocol_id = b"BitTorrent protocol"
        id_length = len(protocol_id)
        if len(self.peer_id) == 0:
            self.generate_peer_id()

        # Initial handshake from docs
        return b''.join([(chr(id_length)).encode(), protocol_id,
                        (chr(0) * 8).encode(), self.info_hash,
                        self.peer_id])

    def send_handshake(self, host, port):
        handshake = self.generate_handshake()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(handshake)

        data = sock.recv(len(handshake))
        try:
            data = sock.recv(68)  # Peer response handshake
            if data:
                print(data)
                peer_id = md5(host.encode() +
                              str(port).encode()).hexdigest()
                temp_peer = pr.Peer(sock, self, peer_id)
                self.peer_dict[peer_id] = temp_peer
                # TODO: handshake completed initiate download after this.
        except:
            print("ERROR: Did not recieve proper return handshake from peer")

    def apple(self):
        # I'm leaving this forever
        print("I AM CLASSY APPLES!")

    def get_peers(self):
        # TODO: For multi files, compute total length
        # from the individual file lengths
        length = self.length
        # Peer id consists of a client code(WS) with a version num and a
        # random client identifier 12 characters long hence the randomint range
        peer_id = self.generate_peer_id()
        self.peer_id = peer_id
        payload = {'info_hash': self.info_hash, 'peer_id': peer_id,
                   'left': length}
        req = requests.get(self.announce, params=payload)
        peers = utils.parse_peerlist(req)
        # TODO: send peers off to be handled
        # TODO: only doing handshake on first peer
        for peer in peers:
            if peer[1] < 1024:
                # Basic step to check if valid ip. If not skip. This should fix
                # the fact that you are included in the ip list
                # which is incorrect
                continue
            self.send_handshake(peer[0], peer[1])
