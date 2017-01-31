import wasp as ws


class Nest(object):

    def __init__(self):
        self.colony = {}

    def hatch(self, meta_data):
        """DESC: generate a new wasp"""
        hatchling = ws.Wasp(meta_data)
        self.assimilate(hatchling)
        hatchling.get_peers()

    def assimilate(self, hatchling):
        # TODO: check if torrent already exists in colony
        if hatchling.info_hash in self.colony:
            print("ALERT: torrent file already exists")
        self.colony[hatchling.info_hash] = hatchling

    def destroy(self, wasp):
        # TODO: Check if was exists, destroy it and
        # all saved and associated data
        print("destroy")

    def swarm(self):
        # TODO: Activate the swarm. Spin off threads for each wasp
        # in colony to seed or leech
        print("swarm")
