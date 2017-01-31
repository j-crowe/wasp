from bencode import bdecode

import nest as ns


def main():
    parse_torrent()


def parse_torrent():
    """DESC: Asks user for location of .torrent file.
    Parses and saves metadata results"""

    t_content = ''
    meta_dict = {}
    # TODO: allow nest pickling and reloading into memory
    nest = None
    # torrent_file = input("Torrent File Location: ")
    torrent_file = '../test/tst.torrent'
    print(torrent_file)
    if nest is None:
        # TODO: check if nest saved to disk else create a new nest
        nest = ns.Nest()

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


if __name__ == "__main__":
    main()
