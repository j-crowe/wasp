import bencode

def main():
    parse_torrent()

def parse_torrent():
    '''DESC: Asks user for location of .torrent file. Parses and saves metadata results'''
    t_content = ''
    torrent_file = raw_input("Torrent File Location: ")

    try:
        with open(torrent_file, 'r') as content_file:
            t_content = content_file.read()
            meta_data = bencode.bdecode(t_content)
            print meta_data
            import pdb; pdb.set_trace()
    except:
        print 'WASP: Error opening file'



class Wasp(object):

    def __init__(self, meta_data):
        self.announce = meta_data['announce']
        self.piece_length = meta_data['info']['piece length']
        self.pieces = meta_data['info']['pieces']
        # TODO: Only works on single file torrents
        self.name = meta_data['info']['name']
        self.length = meta_data['info']['length']

    def apple(self):
        print "I AM CLASSY APPLES!"



if __name__ == "__main__":
    main()
