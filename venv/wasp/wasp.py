import bencode
import urllib

nest = None

def main():
    parse_torrent()

def parse_torrent():
    "DESC: Asks user for location of .torrent file. Parses and saves metadata results"
    t_content = ''
    global nest
    torrent_file = raw_input("Torrent File Location: ")
    if nest is None:
        #TODO: check if nest saved to disk else create a new nest
        nest = Nest()

    try:
        # Attempt to open the torrent file and bdecode the metadata
        with open(torrent_file, 'r') as content_file:
            t_content = content_file.read()
            import pdb; pdb.set_trace()
            tmp = bencode.bdecode(t_content)
            nest.hatch(tmp)
    except IOError:
        print 'ERROR: Could not open file: ' + torrent_file
    except:
        print 'ERROR: An unknown error occurred in opening or bdecoding the file.'



class Wasp(object):
    "DESC: A wasp is a single instance of a torrent. Includes all metadata and functionality in seeding/leeching"

    def __init__(self, meta_data):
        # TODO: Handle non-existant vars appropriately
        self.announce = meta_data['announce']
        self.piece_length = meta_data['info']['piece length']
        self.pieces = meta_data['info']['pieces']
        self.name = meta_data['info']['name']
        # TODO: Only works on single file torrents
        file = meta_data['info']['files'][0]
        self.length = file['length']

    def apple(self):
        print "I AM CLASSY APPLES!"

    def find_peers(self):
        print urllib.quote_plus("http://www.yahoo.com/")


class Nest(object):

    def __init__(self):
        self.colony = []

    def hatch(self, meta_data):
        "DESC: generate a new wasp"
        hatchling = Wasp(meta_data)
        self.assimilate(hatchling)

    def assimilate(self, hatchling):
        # TODO: check if torrent already exists in colony
        self.colony.append(hatchling)

    def destroy(self, wasp):
        # TODO: Check if was exists, destroy it and all saved and associated data
        print "destroy"

    def swarm(self):
        # TODO: Activate the swarm. Spin off threads for each wasp in colony to seed or leech
        print "swarm"

if __name__ == "__main__":
    main()
