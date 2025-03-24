import argparse

parser = argparse.ArgumentParser(description="yzu-ddns-client: A dynamic DNS client.")
parser.add_argument('--config', type=str, help='Path to the configuration file.', required=False, default='config.json')
parser.add_argument('--get_zones', action='store_true', help='Retrieve the list of zones from the DNS provider.')
parser.add_argument('--get_public_ip', action='store_true', help='Fetch the current public IP address.')
parser.add_argument('--get_updatable_zones', action='store_true', help='Retrieve the list of zones that can be updated as defined by the config.')
parser.add_argument('--public_ip_server', type=str, help='Specify the public IP server to use.', required=False, default='https://api.ipify.org?format=txt')
parser.add_argument('--watch', action='store_true', help='Periodically check and update the DNS records if the public IP changes.')
parser.add_argument("--debug", action="store_true", help="Enable debug mode for detailed logging.")
parser.add_argument("--watch_timeout" , type=int, help="Specify the timeout for watch mode in seconds.", required=False, default=60)
args = parser.parse_args()