import threading
import uuid
import time
import os
import random
from pwnagotchi import plugins

class HoneyPotPlugin(plugins.Plugin):
    __author__ = 'Your Name'
    __version__ = '1.0.3'
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

    def handle_wifi_handshake(self, agent, filename, access_point, client_station):
        self.log(f"WiFi Handshake captured from {client_station['addr']} at {access_point['addr']}")
        # Implement additional logic if needed, such as notification or logging.

    def handle_ap_beacon(self, agent, ap):
        if ap['essid'] in self.honey_pot_aps:
            self.log(f"Fake Beacon detected: {ap['essid']} ({ap['addr']})")
            self.detected_fake_aps += 1

            # Check if the detected fake AP is still active
            self.active_fake_aps += 1

    def generate_fake_essid(self):
        return str(uuid.uuid4())[:8]  # Use the first 8 characters of the UUID as ESSID

    def generate_random_mac_address(self):
        return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

    def create_fake_aps(self):
        for _ in range(self.num_initial_aps):
            fake_essid = self.generate_fake_essid()
            fake_mac = self.generate_random_mac_address()
            fake_ap = {
                'essid': fake_essid,
                'addr': fake_mac,
                # Add more access point properties as needed
            }
            self.honey_pot_aps.add(fake_essid)
            self.log(f"Created HoneyPot: {fake_essid} ({fake_ap['addr']})")

    def render_honey_pots(self):
        # Update UI with information about honey pots
        self.ui.add_element('honey-pots', self.honey_pot_aps)
        self.ui.add_element('detected-fake-aps', self.detected_fake_aps)
        self.ui.add_element('active-fake-aps', self.active_fake_aps)

        # Update the log file with information about detected fake APs
        with open(self.log_path, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Detected Fake APs: {self.detected_fake_aps}, Active Fake APs: {self.active_fake_aps}\n")

        # Reset counters
        self.detected_fake_aps = 0
        self.active_fake_aps = 0

        # Schedule the next update
        threading.Timer(self.update_interval, self.render_honey_pots).start()

    def on_ui_setup(self, ui):
        # Add honey pot information to the UI
        ui.add_element('honey-pots', self.honey_pot_aps)
        ui.add_element('detected-fake-aps', self.detected_fake_aps)
        ui.add_element('active-fake-aps', self.active_fake_aps)

# Register the plugin
def setup():
    return HoneyPotPlugin()
