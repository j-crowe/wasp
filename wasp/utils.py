import wasp
import socket
import bencode
import hashlib
from struct import pack, unpack


def decode_port(port):
    """DESC: Given big endian encoded port, returns numerical port."""

    return unpack(">H", port)[0]


def decode_expanded_peers(peers):
    """ Return a list of IPs and ports, given an expanded list of peers,
    from a tracker response. """

    return [(p["ip"], p["port"]) for p in peers]


def decode_binary_peers(peers):
    """DESC: Parse out binary peers list and
    return list of IPs and ports for connection attempts"""
    peers = [peers[i:i+6] for i in range(0, len(peers), 6)]
    return [(socket.inet_ntoa(p[:4]), decode_port(p[4:])) for p in peers]


def parse_peerlist(response):
    """DESC: Given a response, parse out peers list and call appropriate
    decoding function for either protocol standard encoding."""
    peer_dict = bencode.bdecode(response.content)
    peers = peer_dict['peers']
    if type(peers) == str:
        return decode_binary_peers(peers)
    elif type(peers) == list:
        return decode_expanded_peers(peers)


def socket_id(sock):
    return hashlib.md5(sock.getpeername()[0] +
                       str(sock.getpeername()[1])).hexdigest()
