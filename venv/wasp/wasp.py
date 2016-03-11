import bencode
import requests
import hashlib
import random
import urllib

nest = None
version_num = '0001'

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
        # TODO: Only works on single file torrents
        file = meta_data['info']['files'][0]
        self.length = file['length']

    def apple(self):
        # I'm leaving this forever
        print "I AM CLASSY APPLES!"

    def find_peers(self):
        # TODO: For multi files, compute total length from the individual file lengths
        length = self.length
        # Peer id consists of a client code(WS) with a version num and a random client identifier 12 characters long hence the randomin range.
        peer_id = '-WS' + version_num + '-' + str(random.randint(100000000000, 999999999999))
        payload = {'info_hash': self.info_hash, 'peer_id': peer_id, 'left': length}
        req = requests.get(self.announce, params=payload)
        def parse_peerlist(response):
            peer_dict = bencode.bdecode(response.content)
            if isinstance(peer_dict['peers'], dict):
                #TODO: Finish this. Don't have torrent of this type yet
                print 'dictionary peer list'
            else:
                #TODO: Finish this. Figure out how to decode binary list. Maybe build a utils decoder
                print 'binary encoded peer list'
            import pdb; pdb.set_trace()
            print peer_dict

        parse_peerlist(req)


        print req


class Nest(object):

    def __init__(self):
        self.colony = {}

    def hatch(self, meta_data):
        "DESC: generate a new wasp"
        hatchling = Wasp(meta_data)
        self.assimilate(hatchling)
        hatchling.find_peers()

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
