import requests
from yzu_ddns_client.models.provider import BaseProvider
from yzu_ddns_client.models.zones import Zones
from yzu_ddns_client.models.record import Record

BASE_URL = "https://api.bunny.net"

def bunny_type_to_str(bunny_type: int) -> str:
    type_mapping = {
        0: "A",
        1: "AAAA",
        2: "CNAME",
        3: "TXT",
        4: "MX",
        5: "Redirect",
        6: "Flatten",
        7: "PullZone",
        8: "SRV",
        9: "CAA",
        10: "PTR",
        11: "Script",
        12: "NS"
    }
    return type_mapping.get(bunny_type, "Unknown")

class BunnyProvider(BaseProvider):
    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.api_key
    
    def getZones(self) -> Zones:
        headers = {
            'AccessKey': self.api_key,
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{BASE_URL}/dnszone", headers=headers, timeout=10)
        
        if not response.status_code == 200:
            return {"error": "Failed to retrieve zones", "status_code": response.status_code}
        
        return Zones([{
            "id": zone.get('Id'),
            "name": zone.get('Domain'),
            "records": [Record(
                zone_id=zone.get('Id'),
                record_id=record.get('Id'),
                record_name=record.get('Name'),
                record_type=bunny_type_to_str(record.get('Type')),
                record_content=record.get('Value'),
                record_ttl=record.get('Ttl')
            ) for record in zone.get('Records', [])]
        } for zone in response.json()["Items"]])
    
    def updateRecord(self, zone_id, record_id, fields={}):
        headers = {
            'AccessKey': self.api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(f"{BASE_URL}/dnszone/{zone_id}/records/{record_id}", json=fields, headers=headers, timeout=10)
        
        if not response.status_code == 204:
            return "Failed to update record", response.status_code
        
        return "Record updated successfully", 204
    
    def successCodes(self):
        return [204]