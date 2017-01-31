from bencode import bencode, bdecode
from hashlib import md5, sha1
import requests
import random
import socket

import utils
from nest import Nest
from peer import Peer


nest = None

CLIENT_NAME = 'wasptorret'
VERSION_NUM = '0001'
CLIENT_ID = 'WS'


def main():
    parse_torrent()


def parse_torrent():
    """DESC: Asks user for location of .torrent file.
    Parses and saves metadata results"""

    t_content = ''
    meta_dict = {}
    global nest
    # torrent_file = input("Torrent File Location: ")
    torrent_file = '../test/tst.torrent'
    print(torrent_file)
    if nest is None:
        # TODO: check if nest saved to disk else create a new nest
        nest = Nest()

    try:
        # Attempt to open the torrent file and bdecode the metadata
        with open(torrent_file, 'rb') as content_file:
            t_content = content_file.read()
            meta_dict = bdecode(t_content)
    except IOError:
        print('ERROR: Could not open file: ' + torrent_file)
    except:
        print ('ERROR: An unknown error occurred in opening or decoding file.')
    else:
        nest.hatch(meta_dict)


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
        return bytes('-' + CLIENT_ID + VERSION_NUM + '-' + wasp_random, encoding='UTF-8')

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
                # import pdb; pdb.set_trace()
                # import pdb
                # pdb.set_trace()
                peer_id = md5(host.encode() +
                              str(port).encode()).hexdigest()
                temp_peer = Peer(sock, self, peer_id)
                self.peer_dict[peer_id] = temp_peer

                import pdb
                pdb.set_trace()
                # self.initpeer(sock)
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


if __name__ == "__main__":
    main()
