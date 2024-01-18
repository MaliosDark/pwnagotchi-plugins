#wifi_adventures.py

## Disclaimer
#**Note:** This plugin is created for educational purposes
#The author does not take responsibility for any misuse or unauthorized activities conducted with this plugin.
#Be aware of and comply with legal and ethical standards when using this software.
#Always respect privacy, adhere to local laws, and ensure that your actions align with the intended educational purpose of the plugin.
#Use this plugin responsibly and ethically.
#Any actions that violate laws or infringe upon the rights of others are not endorsed or supported.
#By using this software, you acknowledge that the author is not liable for any consequences resulting from its misuse.
#If you have any concerns or questions regarding the ethical use of this plugin, please contact the author for guidance.


import logging
import os
import subprocess
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import datetime
import json
import random

class AdventureType:
    HANDSHAKE = "handshake"
    NEW_NETWORK = "new_network"
    PACKET_PARTY = "packet_party"
    PIXEL_PARADE = "pixel_parade"
    DATA_DAZZLE = "data_dazzle"

class FunAchievements(plugins.Plugin):
    __author__ = 'https://github.com/MaliosDark/'
    __version__ = '1.2.99'
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
        self.data_dazzle_count = 0 
        self.treasure_chests_count = 0
        self.title = ""
        self.last_claimed = None
        self.daily_quest_target = 3
        self.current_adventure = self.choose_random_adventure()
        self.data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fun_achievements.json')

    def get_label_based_on_adventure(self):
        if self.current_adventure == AdventureType.NEW_NETWORK:
            return "New Adventure: "
        elif self.current_adventure == AdventureType.PACKET_PARTY:
            return "Party Time: "
        elif self.current_adventure == AdventureType.PIXEL_PARADE:
            return "Pixel Parade: "
        elif self.current_adventure == AdventureType.DATA_DAZZLE:
            return "Data Dazzle: "
        else:
            return "Mysterious Quest: "

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
                self.current_adventure = FunAchievements.choose_random_adventure()
        logging.info(f"[FunAchievements] Loaded data from JSON: {data}")

    @staticmethod
    def choose_random_adventure():
        return random.choice([AdventureType.HANDSHAKE, AdventureType.NEW_NETWORK, AdventureType.PACKET_PARTY, AdventureType.PIXEL_PARADE, AdventureType.DATA_DAZZLE])

    def on_loaded(self):
        logging.info("[FunAchievements] plugin loaded")

    def on_ui_setup(self, ui):
        title = self.get_title_based_on_achievements()
        label = self.get_label_based_on_adventure()

        ui.add_element('showFunAchievements', LabeledValue(color=BLACK, label=label, value=f"{self.handshake_count}/{self.daily_quest_target} ({self.get_title_based_on_achievements()})", position=(0, 95), label_font=fonts.Medium, text_font=fonts.Medium))

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

        # Buscar el título más alto alcanzado y actualizar el atributo 'title'
        for threshold, title in titles.items():
            if self.fun_achievement_count >= threshold:
                self.title = title

        # Si el título actual es mayor al título anterior, actualiza el título
        if titles.get(self.fun_achievement_count, "") != self.title:
            self.title = titles.get(self.fun_achievement_count, "")

        logging.info(f"[FunAchievements] Updated title: {self.title}")


    def get_title_based_on_achievements(self):
        # Llamar a update_title para asegurarse de que el atributo 'title' esté actualizado
        self.update_title()
        
        # Retornar el título actualizado
        return self.title


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
        logging.info(f"[FunAchievements] on_handshake - Current Adventure: {self.current_adventure}, Handshake Count: {self.handshake_count}")
        
        difficulty_multiplier = {
            AdventureType.HANDSHAKE: 2,
            AdventureType.NEW_NETWORK: 1,  
            AdventureType.PACKET_PARTY: 1,
            AdventureType.PIXEL_PARADE: 2,
            AdventureType.DATA_DAZZLE: 1
        }

        self.handshake_count += difficulty_multiplier.get(self.current_adventure, 1)
        self.check_and_update_daily_quest_target()
        self.check_treasure_chest()

        if self.is_adventure_completed():
            self.fun_achievement_count += 1
            self.update_title()

        self.save_to_json()


    def on_packet_party(self, agent, party_count):
        if self.current_adventure == AdventureType.PACKET_PARTY:
            self.packet_party_count += party_count
            self.check_and_update_daily_quest_target()
            self.check_treasure_chest()
            
            # Check if the current adventure is Packet Party
            if self.current_adventure == AdventureType.PACKET_PARTY:
                # Get the SSID from the current packet
                ssid = agent.get('ssid')
                
                # Check if SSID is available
                if ssid:
                    password = self.get_password_from_potfile(ssid)
                    if password:
                        self.connect_to_wifi(ssid, password)

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
                self.update_title()
                return True
            return False
        elif self.current_adventure == AdventureType.NEW_NETWORK:
            if self.new_networks_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                self.update_title()
                return True
        elif self.current_adventure == AdventureType.PACKET_PARTY:
            if self.packet_party_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                self.update_title()
                return True
        elif self.current_adventure == AdventureType.PIXEL_PARADE:
            if self.pixel_parade_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                self.update_title()
                return True
        elif self.current_adventure == AdventureType.DATA_DAZZLE:
            if self.data_dazzle_count >= self.daily_quest_target:
                self.fun_achievement_count += 1
                self.update_title()
                return True
        return False

    def check_and_update_daily_quest_target(self):
        today = datetime.date.today()
        if self.last_claimed is None or self.last_claimed < today:
            self.last_claimed = today
            self.daily_quest_target += 2

            # Move the adventure update logic outside of is_adventure_completed()
            self.current_adventure = self.choose_random_adventure()


            # Incrementar el título después de actualizar la aventura actual
            self.update_title()

            if self.is_adventure_completed():
                self.fun_achievement_count += 1

        # Save changes to JSON after updating data
        self.save_to_json()


    def on_unfiltered_ap_list(self, agent):
        self.new_networks_count += 1

    def get_password_from_potfile(self, ssid):
        try:
            # Assuming the potfile is located at /root/handshakes/wpa-sec.cracked.potfile
            potfile_path = '/root/handshakes/wpa-sec.cracked.potfile'
            
            # Using grep to find the password for the given SSID
            result = subprocess.run(['grep', f'^{ssid}:', potfile_path], capture_output=True, text=True)

            # If there is a match, extract the password
            if result.stdout:
                password = result.stdout.strip().split(':')[1]
                return password
            else:
                return None
        except Exception as e:
            logging.error(f"Error getting password from potfile: {e}")
            return None

    def connect_to_wifi(self, ssid, password):
        try:

            #using wpa_supplicant:
            subprocess.run(['wpa_supplicant', '-B', '-i', 'your_wifi_interface', '-c', f'/etc/wpa_supplicant/wpa_supplicant.conf', '-D', 'nl80211,wext'])
        except Exception as e:
            logging.error(f"Error connecting to WiFi: {e}")

    def check_treasure_chest(self):
        if random.random() < 0.1:  # 10% chance to find a treasure chest
            self.treasure_chests_count += 1
            logging.info("[FunAchievements] You found a treasure chest!")
