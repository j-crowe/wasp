import bencode

def main():
    parse_torrent()

def parse_torrent():
    "DESC: Asks user for location of .torrent file. Parses and saves metadata results"
    t_content = ''
    torrent_file = raw_input("Torrent File Location: ")

    try:
        with open(torrent_file, 'r') as content_file:
            t_content = content_file.read()
            meta_data = bencode.bdecode(t_content)
            print meta_data
            hatchling = Wasp(meta_data)

    except:
        print 'WASP: Error opening file'



class Wasp(object):
    "DESC: A wasp is a single instance of a torrent. Includes all metadata and functionality in seeding/leeching"

    def __init__(self, meta_data):
        import pdb; pdb.set_trace()
        self.announce = meta_data['announce']
        self.piece_length = meta_data['info']['piece length']
        self.pieces = meta_data['info']['pieces']
        self.name = meta_data['info']['name']
        # TODO: Only works on single file torrents
        file = meta_data['info']['files'][0]
        self.length = file['length']

    def apple(self):
        print "I AM CLASSY APPLES!"



if __name__ == "__main__":
    main()
