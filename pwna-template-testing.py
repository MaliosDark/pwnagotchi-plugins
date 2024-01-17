#THIS IS A TEST. TO LOAD THE NEW UI USING JUST A PLUGIN.
#THIS PLUGIN IS BEING TESTED
#DO NOT USE UNTIL TEST ARE CONFIRMED AND RESULTS ARE AVAILABLE
#I DO INSIST!!
#JUST WAIT A BIT


from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import logging
import os


class EgirlThemePlugin(plugins.Plugin):
    __author__ = 'MaliosDark'
    __version__ = '1.0.0'
    __name__ = "Egirl Theme"
    __license__ = 'GPL3'
    __description__ = 'Plugin to activate/deactivate the egirl-pwnagotchi theme'

    def __init__(self):
        super().__init__()

        # Variable to track whether the theme is enabled or disabled
        self.theme_enabled = False

    def on_loaded(self):
        logging.info("Egirl Theme loaded")

        # Path to the pwnagotchi directory where theme files will be stored
        pwnagotchi_directory = '/root/.pwnagotchi/'

        # URL to the egirl-pwnagotchi theme repository
        theme_repo = 'https://github.com/PersephoneKarnstein/egirl-pwnagotchi/archive/main.zip'

        # Download the ZIP file from the theme repository and extract it to the pwnagotchi directory
        self.download_and_extract(theme_repo, pwnagotchi_directory)

        # Configure the Pwnagotchi configuration file with the new paths for custom faces
        self.update_config()

    def download_and_extract(self, url, destination):
        # Download the ZIP file from the theme repository
        os.system(f'wget {url} -O /tmp/egirl-pwnagotchi.zip')

        # Extract the contents of the ZIP file to the pwnagotchi directory
        os.system(f'unzip /tmp/egirl-pwnagotchi.zip -d {destination}')

    def update_config(self):
        # Update the Pwnagotchi configuration file with the new paths for custom faces
        config_file = '/etc/pwnagotchi/config.toml'

        # Dictionary mapping original faces to new paths
        face_mapping = {
            'look_r': "( ⚆‿⚆)",
            'look_l': "(☉‿☉ )",
            'look_r_happy': "( ◔‿◔)",
            'look_l_happy': "(◕‿◕ )",
            'sleep': "(⇀‿‿↼)",
            'sleep2': "(≖‿‿≖)",
            'awake': "(◕‿‿◕)",
            'bored': "(-__-)",
            'intense': "(°▃▃°)",
            'cool': "(⌐■_■)",
            'happy': "(•‿‿•)",
            'excited': "(ᵔ◡◡ᵔ)",
            'grateful': "(^‿‿^)",
            'motivated': "(☼‿‿☼)",
            'demotivated': "(≖__≖)",
            'smart': "(✜‿‿✜)",
            'lonely': "(ب__ب)",
            'sad': "(╥☁╥ )",
            'angry': "( ¬_¬')",
            'friend': "(♥‿‿♥)",
            'broken': "(☓‿‿☓)",
            'debug': "(#__#)",
            'upload': "(⇀‸↼)",
            'upload1': "(⇀_⇀)",
            'upload2': "(↼_↼)"
        }

        # Read the existing configuration file
        with open(config_file, 'r') as f:
            config_lines = f.readlines()

        # Modify the lines corresponding to the new paths for custom faces
        updated_lines = []
        for line in config_lines:
            for face_name, new_path in face_mapping.items():
                if f'ui.faces.{face_name}' in line:
                    updated_lines.append(f'ui.faces.{face_name} = "/custom-faces/egirl-pwnagotchi/{face_name.upper()}.png"\n')
                    break
            else:
                updated_lines.append(line)

        # Write the updated configuration file
        with open(config_file, 'w') as f:
            f.writelines(updated_lines)

    def on_ui_update(self, ui):
        # Customize the UI here as needed
        if not self.theme_enabled:
            return

        # Your UI customization code goes here

    def on_agent_updated(self, agent, old_pi, new_pi):
        # Customize the agent here as needed
        if not self.theme_enabled:
            return

        # Your agent customization code goes here

    def on_unload(self, ui):
        # Restore the original configuration when unloading the theme
        if self.theme_enabled:
            self.restore_original_config()

    def restore_original_config(self):
        # Restore the original Pwnagotchi configuration file
        original_config = '/etc/pwnagotchi/config.toml.orig'
        config_file = '/etc/pwnagotchi/config.toml'

        # Copy the original configuration file to the current file
        os.system(f'cp {original_config} {config_file}')

        # Remove the original configuration file
        os.system(f'rm {original_config}')

    def on_webhook(self, path, request):
        # Change the state of the theme (enabled/disabled) upon receiving a webhook
        if path == 'egirl-theme/toggle':
            self.theme_enabled = not self.theme_enabled

            if self.theme_enabled:
                self.update_config()
            else:
                self.restore_original_config()

            # Return a response to the client that made the request
            return "Egirl-pwnagotchi theme " + ("activated" if self.theme_enabled else "deactivated")


# Register the plugins
plugins.register_plugin(EgirlThemePlugin())
