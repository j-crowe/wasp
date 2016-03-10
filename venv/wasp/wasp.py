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
            bencode.bdecode(t_content)
    except:
        print 'WASP: Error opening file'



class Wasp(object):

    def __init__(self):
        self.tangerine = "And now a thousand years between"

    def apple(self):
        print "I AM CLASSY APPLES!"



if __name__ == "__main__":
    main()
