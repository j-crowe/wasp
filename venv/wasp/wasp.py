import bencode

nest = None

def main():
    parse_torrent()

def parse_torrent():
    "DESC: Asks user for location of .torrent file. Parses and saves metadata results"
    t_content = ''
    torrent_file = raw_input("Torrent File Location: ")

    try:
        # Attempt to open the torrent file and bdecode the metadata
        with open(torrent_file, 'r') as content_file:
            t_content = content_file.read()
            hatch(bencode.bdecode(t_content))
    except IOError:
        print 'ERROR: Could not open file: ' + torrent_file
    except:
        print 'ERROR: An unknown error occurred in opening or bdecoding the file.'


def hatch(meta_data):
    "DESC: generate a new wasp"
    hatchling = Wasp(meta_data)


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


Class Nest(object):

    def __init__(self):
        self.colony = []

    def assimilate(hatchling):
        # TODO: check if torrent already exists in colony
        self.colony.append(hatchling)

    def destroy(wasp):
        # TODO: Check if was exists, destroy it and all saved and associated data
        print "destroy"

    def swarm():
        # TODO: Activate the swarm. Spin off threads for each wasp in colony to seed or leech
        print "swarm"

if __name__ == "__main__":
    main()
