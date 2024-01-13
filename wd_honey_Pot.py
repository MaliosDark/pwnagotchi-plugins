import logging
import threading
from pwnagotchi.ui.components import LabeledValue
import pwnagotchi.ui.fonts as fonts
import time
import uuid
import os
import random
from pwnagotchi.plugins import Plugin

class HoneyPotPlugin(Plugin):
    __author__ = 'Andryu Schittone'
    __version__ = '1.3.0'
    __license__ = 'GPL3'
    __description__ = 'A Pwnagotchi plugin for setting up a honey pot to just detect other Pwnagotchis making deauths.'

    def __init__(self):
        logging.debug("HoneyPot plugin created")
        self.honey_pot_aps = set()
        self.detected_fake_aps = 0
        self.active_fake_aps = 0
        self.num_initial_aps = 5
        self.update_interval = 60
        self.log_path = "/etc/pwnagotchi/hplogs.log"

        threading.Timer(self.update_interval, self.render_honey_pots).start()
        self.create_fake_aps()

    def on_loaded(self):
        self.register_event(self.handle_wifi_handshake, 'wifi-handshake')
        self.register_event(self.handle_ap_beacon, 'ap-beacon')

    def on_unload(self, ui):
        pass

    def on_ui_setup(self, ui):
        ui.add_element('honey-pots', LabeledValue(color=fonts.BLACK, label='Honey Pots', value='0', position=(ui.width() / 2 - 25, 0),
                                                   label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('detected-fake-aps', LabeledValue(color=fonts.BLACK, label='Detected Fake APs', value='0', position=(ui.width() / 2 - 25, 10),
                                                            label_font=fonts.Bold, text_font=fonts.Medium))
        ui.add_element('active-fake-aps', LabeledValue(color=fonts.BLACK, label='Active Fake APs', value='0', position=(ui.width() / 2 - 25, 20),
                                                          label_font=fonts.Bold, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        some_voltage = 0.1
        some_capacity = 100.0
        ui.set('honey-pots', str(len(self.honey_pot_aps)))
        ui.set('detected-fake-aps', str(self.detected_fake_aps))
        ui.set('active-fake-aps', str(self.active_fake_aps))

    def handle_wifi_handshake(self, agent, filename, access_point, client_station):
        self.log(f"WiFi Handshake captured from {client_station['addr']} at {access_point['addr']}")
        # Implement additional logic if needed, such as notification or logging.

    def handle_ap_beacon(self, agent, ap):
        if ap['essid'] in self.honey_pot_aps:
            self.log(f"Fake Beacon detected: {ap['essid']} ({ap['addr']})")
            self.detected_fake_aps += 1

        if ap['essid'] in self.honey_pot_aps:
            self.active_fake_aps += 1

    def generate_fake_essid(self):
        return str(uuid.uuid4())[:8]

    def generate_random_mac_address(self):
        return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

    def create_fake_aps(self):
        for _ in range(self.num_initial_aps):
            fake_essid = self.generate_fake_essid()
            fake_ap = {
                'essid': fake_essid,
                'addr': self.generate_random_mac_address(),
            }
            self.honey_pot_aps.add(fake_essid)
            self.log(f"Created HoneyPot: {fake_essid} ({fake_ap['addr']})")

    def render_honey_pots(self):
        self.ui.add_element('honey-pots', LabeledValue(color=fonts.BLACK, label='Honey Pots', value=str(len(self.honey_pot_aps)), position=(self.ui.width() / 2 - 25, 0),
                                                        label_font=fonts.Bold, text_font=fonts.Medium))
        self.ui.add_element('detected-fake-aps', LabeledValue(color=fonts.BLACK, label='Detected Fake APs', value=str(self.detected_fake_aps), position=(self.ui.width() / 2 - 25, 10),
                                                                 label_font=fonts.Bold, text_font=fonts.Medium))
        self.ui.add_element('active-fake-aps', LabeledValue(color=fonts.BLACK, label='Active Fake APs', value=str(self.active_fake_aps), position=(self.ui.width() / 2 - 25, 20),
                                                               label_font=fonts.Bold, text_font=fonts.Medium))

        with open(self.log_path, 'a') as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Detected Fake APs: {self.detected_fake_aps}, Active Fake APs: {self.active_fake_aps}\n")

        self.detected_fake_aps = 0
        self.active_fake_aps = 0

        threading.Timer(self.update_interval, self.render_honey_pots).start()

    def log(self, message):
        logging.info(message)
        status = self.ui.get('status')
        if status:
            status.value = message

# Register the plugin
def setup():
    return HoneyPotPlugin()
