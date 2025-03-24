from yzu_ddns_client.config import Config
from yzu_ddns_client.args import args
from yzu_ddns_client.utils import get_public_ip, watch
from yzu_ddns_client.logger import logger
from yzu_ddns_client.provider import ProviderManager

if __name__ == "__main__":
    config = Config(filename=args.config)
    ProviderManager.setup(config)

    if args.get_zones:
        logger.info("%s", ProviderManager.get_provider().getZones())
    if args.get_public_ip:
        logger.info("%s", get_public_ip(args.public_ip_server))
    if args.get_updatable_zones:
        logger.info("%s", config.zones)
    if args.watch:
        logger.debug("Initializing watch mode...")
        watch(config)
