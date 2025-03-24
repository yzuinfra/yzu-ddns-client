import pyjson5

from yzu_ddns_client.models.record import Record
from yzu_ddns_client.models.zones import Zones
from yzu_ddns_client.logger import logger

class Config:
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.config = {}
        if not self.load_config():
            raise Exception("Failed to load configuration file.")
        self.api_key = self.config.get('api_key', '')
        self.provider = self.config.get('provider', '')
        self.zones = Zones([
            {
                "name": zone.get('name'),
                "records": [
                    Record(
                        zone_id=zone.get('id', "use_remote"),
                        record_id=record.get('id', "use_remote"),
                        record_name=record.get('name'),
                        record_type=record.get('type', "use_remote"),
                        record_ttl=record.get('ttl', "use_remote"),
                        record_content="use_remote"
                    ) for record in zone.get('records', [])
                ]
            } for zone in self.config.get('zones', [])
        ])

        if any(record.record_type == "use_remote" and record.record_name == "" for zone in self.zones.zones for record in zone.records):
            logger.warning("Found empty record name with 'use_remote' type. This may cause erronous updates to root records with no name of various types.")
            logger.warning("Continue? (y/n)")
            if input().strip().lower() != 'y':
                raise Exception("Configuration contains invalid records. Exiting.")

    def load_config(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.config = pyjson5.load(file)
                return True
        except FileNotFoundError:
            print(f"Configuration file '{self.filename}' not found.")
            self.config = {}
        except pyjson5.Json5DecoderException as e:
            print(f"Error decoding JSON from the configuration file: {e}")
            self.config = {}
        return False
