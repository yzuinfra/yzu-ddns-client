import requests, time
from yzu_ddns_client.args import args
from yzu_ddns_client.logger import logger
from yzu_ddns_client.provider import ProviderManager

def get_public_ip(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None
    
def watch(config):
    updatable_zones = config.zones
    while True:
        current_ip = get_public_ip(args.public_ip_server)
        if not current_ip:
            logger.error("Failed to retrieve current public IP.")
            time.sleep(args.watch_timeout)
            continue
        logger.info("Current public IP: %s", current_ip)

        remote_zones = ProviderManager.get_provider().getZones()

        matching_zones = [zone for zone in remote_zones if zone.name in [z.name for z in updatable_zones]]
        if not matching_zones:
            logger.info("The account does not have any zones that match the current configuration.")
            raise Exception("No matching zones found.")
        for zone in matching_zones:
            matching_records = [
                record for record in zone.records 
                if record.record_name in [
                    r.record_name for z in updatable_zones for r in z.records if r.record_name == record.record_name and r.record_type == record.record_type
                    and (r.record_id == record.record_id if r.record_id != "use_remote" else True)
                ]
            ]
            if not matching_records:
                logger.info(f"No matching records found in zone {zone.name}.")
                continue
            for record in matching_records:
                if record.record_content != current_ip:
                    if record.record_name == "":
                        logger.info(f"Updating root record in zone {zone.name} from {record.record_content} to {current_ip}")
                    else:
                        logger.info(f"Updating record {record.record_name} in zone {zone.name} from {record.record_content} to {current_ip}")
                    ret, code = ProviderManager.get_provider().updateRecord(zone.id, record.record_id, {"content": current_ip})
                    if code not in ProviderManager.get_provider().successCodes():
                        logger.error(f"Failed to update record {record.record_name} in zone {zone.name}. Error code: {code}, response: {ret}")
                    else:
                        logger.info(f"Record {record.record_name} in zone {zone.name} updated successfully.")
                else:
                    if record.record_name == "":
                        logger.info(f"Record {zone.name} in zone {zone.name} is already up to date.") # When record is empty, usually root record
                    else:
                        logger.info(f"Record {record.record_name} in zone {zone.name} is already up to date.")
        
        logger.info("My job here is done! I'll check again in %d seconds.", args.watch_timeout)
        time.sleep(args.watch_timeout)