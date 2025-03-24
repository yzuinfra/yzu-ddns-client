from typing import List, Dict
import jsonpickle
from yzu_ddns_client.models.zone import Zone

class Zones:
    def __init__(self, zones: List[Dict]):
        self.zones = [Zone(**zone) for zone in zones]

    def __repr__(self):
        return jsonpickle.encode(self.zones, unpicklable=False, indent=4)

    def __getitem__(self, index):
        return self.zones[index]
