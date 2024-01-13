import threading
import uuid
import time
import os
import random
import logging
from pwnagotchi.plugins import Plugin, on_loaded, on_ui_setup, on_ui_update, on_bored, on_deauthentication

class HoneyPotPlugin(Plugin):
    __author__ = 'Andryu Schittone'
    __version__ = '1.2.4'
    __license__ = 'GPL3'
    __description__ = 'A honey pot plugin for Pwnagotchi.'

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

    @on_loaded()
    def loaded(self):
        self.register_event("wifi-handshake", self.handle_wifi_handshake)
        self.register_event("ap-beacon", self.handle_ap_beacon)
        logging.warning("WARNING: This honey pot plugin is active!")

    def handle_wifi_handshake(self, agent, filename, access_point, client_station):
        message = f"WiFi Handshake captured from {client_station['addr']} at {access_point['addr']}"
        self.log(message)
        self.ui.add_element('honey-pots', message, position=[10, 40], color="blue")
        # Implement additional logic if needed, such as notification or logging.

    def handle_ap_beacon(self, agent, ap):
        if ap['essid'] in self.honey_pot_aps:
            message = f"Fake Beacon detected: {ap['essid']} ({ap['addr']})"
            self.log(message)
            self.ui.add_element('honey-pots', message, position=[10, 40], color="green")
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
            message = f"Created HoneyPot: {fake_essid} ({fake_ap['addr']})"
            self.log(message)
            self.ui.add_element('honey-pots', message, position=[10, 40], color="orange")

    def render_honey_pots(self):
        # Update UI with information about honey pots
        self.ui.add_element('honey-pots', self.honey_pot_aps, position=[10, 10], color="black")
        self.ui.add_element('detected-fake-aps', self.detected_fake_aps, position=[10, 20], color="black")
        self.ui.add_element('active-fake-aps', self.active_fake_aps, position=[10, 30], color="black")

        # Update the log file with information about detected fake APs
        with open(self.log_path, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Detected Fake APs: {self.detected_fake_aps}, Active Fake APs: {self.active_fake_aps}\n")

        # Reset counters
        self.detected_fake_aps = 0
        self.active_fake_aps = 0

        # Schedule the next update
        threading.Timer(self.update_interval, self.render_honey_pots).start()

    @on_ui_setup()
    def ui_setup(self, ui):
        # Add honey pot information to the UI
        ui.add_element('honey-pots', self.honey_pot_aps, position=[10, 10], color="black")
        ui.add_element('detected-fake-aps', self.detected_fake_aps, position=[10, 20], color="black")
        ui.add_element('active-fake-aps', self.active_fake_aps, position=[10, 30], color="black")

    @on_ui_update()
    def ui_update(self, ui):
        # Update UI elements
        some_voltage = 0.1
        some_capacity = 100.0
        ui.set('ups', "%4.2fV/%2i%%" % (some_voltage, some_capacity))

    @on_bored()
    def bored(self):
        message = "Pwnagotchi is bored"
        self.log(message)
        self.ui.add_element('honey-pots', message, position=[10, 40], color="purple")
        logging.info(message)

    @on_deauthentication()
    def deauthentication(self, agent, access_point, client_station):
        # Your code to handle deauthentication events
        message = f"Deauthentication event: {client_station['addr']} deauthenticated from {access_point['addr']}"
        self.log(message)
        self.ui.add_element('honey-pots', message, position=[10, 40], color="red")
        # Implement additional logic if needed, such as notification or logging.

# Register the plugin
def setup():
    return HoneyPotPlugin()
