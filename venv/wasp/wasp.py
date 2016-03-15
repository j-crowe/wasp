import bencode
import requests
import hashlib
import random
import socket
import utils


nest = None

CLIENT_NAME = 'wasptorret'
VERSION_NUM = '0001'
CLIENT_ID = 'WS'

def main():
    parse_torrent()

def parse_torrent():
    "DESC: Asks user for location of .torrent file. Parses and saves metadata results"
    t_content = ''
    meta_dict = {}
    global nest
    torrent_file = raw_input("Torrent File Location: ")
    if nest is None:
        #TODO: check if nest saved to disk else create a new nest
        nest = Nest()

    try:
        # Attempt to open the torrent file and bdecode the metadata
        with open(torrent_file, 'r') as content_file:
            t_content = content_file.read()
            meta_dict = bencode.bdecode(t_content)
    except IOError:
        print 'ERROR: Could not open file: ' + torrent_file
    except:
        print 'ERROR: An unknown error occurred in opening or bdecoding the file.'

    nest.hatch(meta_dict)


class Wasp(object):
    "DESC: A wasp is a single instance of a torrent. Includes all metadata and functionality in seeding/leeching"

    def __init__(self, meta_data):
        # TODO: Handle non-existant vars appropriately
        self.announce = meta_data['announce']
        self.piece_length = meta_data['info']['piece length']
        self.pieces = meta_data['info']['pieces']
        self.info_hash = hashlib.sha1(bencode.bencode(meta_data['info'])).digest()
        self.name = meta_data['info']['name']
        self.peer_id=''
        # TODO: Only works on single file torrents
        file = meta_data['info']['files'][0]
        self.length = file['length']


    def generate_peer_id(self):
        "DESC: Generate unique wasp peer id. Used as standard in bittorrent protocol."
        wasp_random = str(random.randint(100000000000, 999999999999))
        return '-' + CLIENT_ID + VERSION_NUM + '-' + wasp_random

    def generate_handshake(self):
        "DESC: Generates and returns initial bit torrent handshake"

        protocol_id = "BitTorrent protocol"
        id_length = len(protocol_id)
        if len(self.peer_id) == 0:
            self.generate_peer_id()
        return ''.join([chr(id_length), protocol_id, chr(0) * 8, self.info_hash, self.peer_id])

    def send_handshake(self, host, port):
        # import pdb; pdb.set_trace()
        handshake = self.generate_handshake()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(handshake)

        data = sock.recv(len(handshake))
        try:
            data = sock.recv(68)  # Peer's handshake - len from docs
            if data:
                print data
                # self.initpeer(sock)
        except:
            print "ERROR: Did not recieve proper return handshake from peer"
    def apple(self):
        # I'm leaving this forever
        print "I AM CLASSY APPLES!"

    def get_tracker(self):
        # TODO: For multi files, compute total length from the individual file lengths
        length = self.length
        # Peer id consists of a client code(WS) with a version num and a random client identifier 12 characters long hence the randomint range.
        peer_id = self.generate_peer_id()
        self.peer_id = peer_id
        payload = {'info_hash': self.info_hash, 'peer_id': peer_id, 'left': length}
        req = requests.get(self.announce, params=payload)
        peers = utils.parse_peerlist(req)
        #TODO: send peers off to be handled
        #TODO: only doing handshake on first peer
        self.send_handshake(peers[0][0], peers[0][1])



class Nest(object):

    def __init__(self):
        self.colony = {}

    def hatch(self, meta_data):
        "DESC: generate a new wasp"
        hatchling = Wasp(meta_data)
        self.assimilate(hatchling)
        hatchling.get_tracker()

    def assimilate(self, hatchling):
        # TODO: check if torrent already exists in colony
        if hatchling.info_hash in self.colony:
            print "ALERT: torrent file already exists"
        self.colony[hatchling.info_hash] = hatchling

    def destroy(self, wasp):
        # TODO: Check if was exists, destroy it and all saved and associated data
        print "destroy"

    def swarm(self):
        # TODO: Activate the swarm. Spin off threads for each wasp in colony to seed or leech
        print "swarm"

if __name__ == "__main__":
    main()
