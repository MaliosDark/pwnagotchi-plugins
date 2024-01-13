import threading
import uuid
import time
import os
import random
from pwnagotchi.plugins import Plugin
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

class HoneyPotPlugin(Plugin):
    __author__ = 'Andryu Schittone'
    __version__ = '1.2.3'
    __license__ = 'GPL3'

    def __init__(self):
        super(HoneyPotPlugin, self).__init__()
        self.honey_pot_aps = set()
        self.detected_fake_aps = 0
        self.active_fake_aps = 0
        self.num_initial_aps = 5
        self.update_interval = 60
        self.log_path = "/etc/pwnagotchi/hplogs.log"  # Default log path

        # Read configurations from config.toml
        if 'ui.plugins.honey-pot-plugin' in self.config:
            self.num_initial_aps = self.config['ui.plugins.honey-pot-plugin'].get('num_initial_aps', 5)
            self.update_interval = self.config['ui.plugins.honey-pot-plugin'].get('update_interval', 60)
            self.log_path = self.config['ui.plugins.honey-pot-plugin'].get('log_path', "/etc/pwnagotchi/hplogs.log")

        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(self.log_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Initialize the honey pots on plugin load
        self.create_fake_aps()

        # Start a timer for periodic updates
        threading.Timer(self.update_interval, self.render_honey_pots).start()

    def on_loaded(self):
        self.register_event("wifi-handshake", self.handle_wifi_handshake)
        self.register_event("ap-beacon", self.handle_ap_beacon)
        self.register_event("deauthentication", self.handle_deauthentication)

    def handle_wifi_handshake(self, agent, filename, access_point, client_station):
        self.log(f"WiFi Handshake captured from {client_station['addr']} at {access_point['addr']}")
        self.ui.set('info', f"WiFi Handshake captured from {client_station['addr']} at {access_point['addr']}")

    def handle_ap_beacon(self, agent, ap):
        if ap['essid'] in self.honey_pot_aps:
            self.log(f"Fake Beacon detected: {ap['essid']} ({ap['addr']})")
            self.detected_fake_aps += 1
            self.active_fake_aps += 1
            self.ui.set('info', f"Fake Beacon detected: {ap['essid']} ({ap['addr']})")

    def generate_fake_essid(self):
        return str(uuid.uuid4())[:8]

    def generate_random_mac_address(self):
        return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

    def create_fake_aps(self):
        for _ in range(self.num_initial_aps):
            fake_essid = self.generate_fake_essid()
            fake_mac = self.generate_random_mac_address()
            fake_ap = {
                'essid': fake_essid,
                'addr': fake_mac,
            }
            self.honey_pot_aps.add(fake_essid)
            self.log(f"Created HoneyPot: {fake_essid} ({fake_ap['addr']})")

    def render_honey_pots(self):
        self.ui.add_element('honey-pots', self.honey_pot_aps)
        self.ui.add_element('detected-fake-aps', self.detected_fake_aps)
        self.ui.add_element('active-fake-aps', self.active_fake_aps)

        with open(self.log_path, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Detected Fake APs: {self.detected_fake_aps}, Active Fake APs: {self.active_fake_aps}\n")

        self.detected_fake_aps = 0
        self.active_fake_aps = 0

        threading.Timer(self.update_interval, self.render_honey_pots).start()

    def handle_deauthentication(self, agent, access_point, client_station):
        self.ui.set('info', f"Deauthentication event: {client_station['addr']} deauthenticated from {access_point['addr']}")
        self.log(f"Deauthentication event: {client_station['addr']} deauthenticated from {access_point['addr']}")

# Register the plugin
def setup():
    return HoneyPotPlugin()
