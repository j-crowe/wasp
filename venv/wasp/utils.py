import wasp
import socket
import bencode
from struct import pack, unpack


def decode_port(port):
    """ Given a big-endian encoded port, returns the numerical port. """

    return unpack(">H", port)[0]

def decode_expanded_peers(peers):
    """ Return a list of IPs and ports, given an expanded list of peers,
    from a tracker response. """

    return [(p["ip"], p["port"]) for p in peers]

def decode_binary_peers(peers):
    """ Return a list of IPs and ports, given a binary list of peers,
    from a tracker response. """

    peers = slice(peers, 6) # Cut the response at the end of every peer
    return [(socket.inet_ntoa(p[:4]), decode_port(p[4:])) for p in peers]


def parse_peerlist(response):
    peer_dict = bencode.bdecode(response.content)
    peers = peer_dict['peers']
    if type(peers) == str:
        return decode_binary_peers(peers)
    elif type(peers) == list:
        return decode_expanded_peers(peers)
