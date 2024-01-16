#wifi_adventures.py
import logging
from optparse import TitledHelpFormatter
import os
import pwnagotchi.plugins as plugins
import datetime
import json
import random

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts

class AdventureType:
    HANDSHAKE = "handshake"
    NEW_NETWORK = "new_network"
    PACKET_PARTY = "packet_party"
    PIXEL_PARADE = "pixel_parade"
    DATA_DAZZLE = "data_dazzle"  # New adventure type

def choose_random_adventure():
    return random.choice([AdventureType.HANDSHAKE, AdventureType.NEW_NETWORK, AdventureType.PACKET_PARTY, AdventureType.PIXEL_PARADE, AdventureType.DATA_DAZZLE])

class FunAchievements(plugins.Plugin):
    __author__ = 'https://github.com/MaliosDark/'
    __version__ = '1.2.0'
    __license__ = 'GPL3'
    __description__ = 'Taking Pwnagotchi on WiFi adventures and collect fun achievements.'
    __defaults__ = {
        'enabled': False
    }

    def __init__(self):
        self.ready = False
        self.fun_achievement_count = 0
        self.handshake_count = 0
        self.new_networks_count = 0
        self.packet_party_count = 0
        self.pixel_parade_count = 0
        self.data_dazzle_count = 0  # New counter for data dazzles
        self.treasure_chests_count = 0
        self.title = ""
        self.last_claimed = None
        self.daily_quest_target = 3
        self.current_adventure = choose_random_adventure()
        self.data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fun_achievements.json')

    def get_label_based_on_adventure(self):
        if self.current_adventure == AdventureType.NEW_NETWORK:
            return "New Adventure:"
        elif self.current_adventure == AdventureType.PACKET_PARTY:
            return "Party Time:"
        elif self.current_adventure == AdventureType.PIXEL_PARADE:
            return "Pixel Parade:"
        elif self.current_adventure == AdventureType.DATA_DAZZLE:
            return "Data Dazzle:"
        else:
            return "Mysterious Quest:"

    def load_from_json(self):
        logging.info('[FunAchievements] Loading data from JSON...')
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as file:
                data = json.load(file)
                self.handshake_count = data.get('handshake_count', 0)
                self.fun_achievement_count = data.get('fun_achievement_count', 0)
                self.new_networks_count = data.get('new_networks_count', 0)
                self.packet_party_count = data.get('packet_party_count', 0)
                self.pixel_parade_count = data.get('pixel_parade_count', 0)
                self.data_dazzle_count = data.get('data_dazzle_count', 0)
                self.treasure_chests_count = data.get('treasure_chests_count', 0)
                self.daily_quest_target = data.get('daily_quest_target', 5)
                self.last_claimed = datetime.datetime.strptime(data['last_claimed'], '%Y-%m-%d').date() if 'last_claimed' in data else None
                self.current_adventure = data.get('current_adventure', choose_random_adventure())
        logging.info(f"[FunAchievements] Loaded data from JSON: {data}")

    def on_loaded(self):
        logging.info("[FunAchievements] plugin loaded")

    def on_ui_setup(self, ui):
        title = self.get_title_based_on_achievements()
        label = self.get_label_based_on_adventure()

        ui.add_element('showFunAchievements', LabeledValue(color=BLACK, label=label, value=f"{self.handshake_count}/{self.daily_quest_target} ({title})", position=(0, 83), label_font=fonts.Medium, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        if self.ready:
            ui.set('showFunAchievements', f"{self.handshake_count}/{self.daily_quest_target} ({self.get_title_based_on_achievements()})")

    def on_ready(self, agent):
        _ = agent
        self.ready = True
        if os.path.exists(self.data_path):
            self.load_from_json()
        else:
            self.save_to_json()

    def update_title(self):
        titles = {
            0: "WiFi Whisperer",
            2: "Signal Maestro",
            4: "Adventure Artisan",
            8: "Byte Buccaneer",
            10: "Data Dynamo",
            12: "Network Nomad",
            14: "Binary Bard",
            16: "Code Commander",
            20: "Cyber Corsair",
            24: "Protocol Pioneer",
            30: "Bit Bazaar",
            34: "Digital Druid",
            40: "Epic Explorer",
            60: "System Sorcerer",
            65: "Crypto Crusader",
            75: "Digital Dynamo",
            80: "Cyber Celestial",
            90: "Bitlord of the Bits",
            95: "Master of the Matrix",
            100: "Legendary Adventurer"
        }
        for threshold, title in titles.items():
            if self.fun_achievement_count >= threshold:
                return title


    def get_title_based_on_achievements(self):
        return self.update_title()

    def save_to_json(self):
        data = {
            'handshake_count': self.handshake_count,
            'new_networks_count': self.new_networks_count,
            'packet_party_count': self.packet_party_count,
            'pixel_parade_count': self.pixel_parade_count,
            'data_dazzle_count': self.data_dazzle_count,
            'treasure_chests_count': self.treasure_chests_count,
            'last_claimed': self.last_claimed.strftime('%Y-%m-%d') if self.last_claimed else None,
            'daily_quest_target': self.daily_quest_target,
            'current_adventure': self.current_adventure,
            'fun_achievement_count': self.fun_achievement_count
        }
        with open(self.data_path, 'w') as file:
            json.dump(data, file)

    def on_handshake(self, agent, filename, access_point, client_station):
        if self.current_adventure == AdventureType.HANDSHAKE:
            self.handshake_count += 1
            self.check_and_update_daily_quest_target()
            self.check_treasure_chest()
        self.save_to_json()

    def on_packet_party(self, agent, party_count):
        if self.current_adventure == AdventureType.PACKET_PARTY:
            self.packet_party_count += party_count
            self.check_and_update_daily_quest_target()
            self.check_treasure_chest()
        self.save_to_json()

    def on_pixel_parade(self, agent, pixel_count):
        if self.current_adventure == AdventureType.PIXEL_PARADE:
            self.pixel_parade_count += pixel_count
            self.check_and_update_daily_quest_target()
            self.check_treasure_chest()
        self.save_to_json()

    def on_data_dazzle(self, agent, dazzle_count):
        if self.current_adventure == AdventureType.DATA_DAZZLE:
            self.data_dazzle_count += dazzle_count
            self.check_and_update_daily_quest_target()
            self.check_treasure_chest()
        self.save_to_json()

    def is_adventure_completed(self):
        if self.current_adventure == AdventureType.HANDSHAKE:
            if self.handshake_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                return True
            return False
        elif self.current_adventure == AdventureType.NEW_NETWORK:
            if self.new_networks_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                return True
        elif self.current_adventure == AdventureType.PACKET_PARTY:
            if self.packet_party_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                return True
        elif self.current_adventure == AdventureType.PIXEL_PARADE:
            if self.pixel_parade_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                return True
        elif self.current_adventure == AdventureType.DATA_DAZZLE:
            if self.data_dazzle_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                return True
        return False

    def check_and_update_daily_quest_target(self):
        today = datetime.date.today()
        if self.last_claimed is None or self.last_claimed < today:
            self.last_claimed = today
            self.daily_quest_target += 2
            if self.is_adventure_completed():
                self.fun_achievement_count += 1
            self.current_adventure = choose_random_adventure()

    def on_unfiltered_ap_list(self, agent):
        self.new_networks_count += 1

    def check_treasure_chest(self):
        if random.random() < 0.1:  # 10% chance to find a treasure chest
            self.treasure_chests_count += 1
            logging.info("[FunAchievements] You found a treasure chest!")
