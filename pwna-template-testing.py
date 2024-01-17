#THIS IS A TEST. TO LOAD THE NEW UI USING JUST A PLUGIN.
#THIS PLUGIN IS BEING TESTED
#DO NOT USE UNTIL TESTS ARE CONFIRMED AND RESULTS ARE AVAILABLE
#I DO INSIST!!
#JUST WAIT A BIT

import subprocess
import sys

# Instalar dependencias necesarias
subprocess.run([sys.executable, '-m', 'pip', 'install', 'pillow'])

from pwnagotchi.ui.components import LabeledValue, Widget, Text
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
from PIL import Image, ImageOps
from textwrap import TextWrapper
import logging
import os
import shutil
import subprocess

class EgirlThemePlugin(plugins.Plugin):
    __author__ = 'MaliosDark'
    __version__ = '1.1.7'
    __name__ = "Egirl Theme"
    __license__ = 'GPL3'
    __description__ = 'Plugin to activate/deactivate the egirl-pwnagotchi theme'

    def __init__(self):
        super().__init__()

        # Variable to track whether the theme is enabled or disabled
        self.theme_enabled = False

    def install_dependencies(self):
        logging.info("Installing dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests'])  
    def on_loaded(self):
        # Instalar dependencias al cargar el plugin
        self.install_dependencies()

        logging.info("Egirl Theme loaded")

        # Path to the pwnagotchi directory where theme files will be stored
        pwnagotchi_directory = '/root/.pwnagotchi/'

        # URL to the correct egirl-pwnagotchi theme repository
        theme_repo = 'https://github.com/PersephoneKarnstein/egirl-pwnagotchi/archive/master.zip'

        # Call download_and_extract to get the custom_faces_directory
        custom_faces_directory = self.download_and_extract(theme_repo, pwnagotchi_directory)

        # Configure the Pwnagotchi configuration file with the new paths for custom faces
        self.update_config(custom_faces_directory)

        # Restart Pwnagotchi
        self.restart_pwnagotchi()

    def download_and_extract(self, url, destination):
        logging.info("Downloading and extracting theme files...")

        # Download the ZIP file from the theme repository
        os.system(f'wget {url} -O /tmp/egirl-pwnagotchi-master.zip')

        # Extract the contents of the ZIP file to the pwnagotchi directory
        os.system(f'unzip /tmp/egirl-pwnagotchi-master.zip -d {destination}')

        # Move the contents of 'faces' directory to the 'custom-faces/egirl-pwnagotchi' directory
        faces_directory = os.path.join(destination, 'egirl-pwnagotchi-master/faces')
        destination_directory = os.path.join(destination, 'custom-faces/egirl-pwnagotchi')

        # Ensure the destination directory exists
        os.makedirs(destination_directory, exist_ok=True)

        # Move each file from faces directory to custom-faces/egirl-pwnagotchi
        for file_name in os.listdir(faces_directory):
            source_path = os.path.join(faces_directory, file_name)
            destination_path = os.path.join(destination_directory, file_name)
            shutil.move(source_path, destination_path)

        logging.info("Theme files extracted and moved successfully.")

        # Return the correct destination directory for further configuration
        return destination_directory

    def move_images_to_custom_faces(self, src_directory, dest_directory):
        # Move the contents of the source directory to the destination directory
        for file_name in os.listdir(src_directory):
            source_path = os.path.join(src_directory, file_name)
            destination_path = os.path.join(dest_directory, file_name)
            shutil.move(source_path, destination_path)

    def modify_paths_in_components(self, src_file, dest_file, custom_faces_directory):
        # Verificar si el archivo components.py existe antes de intentar abrirlo
        if not os.path.exists(src_file):
            logging.error(f"File not found: {src_file}")
            return

        # Read the source file
        with open(src_file, 'r') as f:
            src_lines = f.readlines()

        # Modify the lines corresponding to the new paths for custom faces
        updated_lines = []
        for line in src_lines:
            if 'look_r' in line:
                updated_lines.append(f'            "value": "{custom_faces_directory}/LOOK_R.png",\n')
            elif 'look_l' in line:
                updated_lines.append(f'            "value": "{custom_faces_directory}/LOOK_L.png",\n')
            # Add more conditions for other face names as needed
            else:
                updated_lines.append(line)

        # Write the updated file
        with open(dest_file, 'w') as f:
            f.writelines(updated_lines)

    def modify_paths_in_view(self, src_file, dest_file, custom_faces_directory):
        # Read the source file
        with open(src_file, 'r') as f:
            src_lines = f.readlines()

        # Modify the lines corresponding to the new paths for custom faces
        updated_lines = []
        for line in src_lines:
            if 'look_r' in line:
                updated_lines.append(f'        self.draw_sprite(self.LOOK_R, 0, 0)\n')
            elif 'look_l' in line:
                updated_lines.append(f'        self.draw_sprite(self.LOOK_L, 0, 0)\n')
            # Add more conditions for other face names as needed
            else:
                updated_lines.append(line)

        # Write the updated file
        with open(dest_file, 'w') as f:
            f.writelines(updated_lines)

    def update_config(self, custom_faces_directory):
        logging.info("Updating Pwnagotchi configuration...")

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
        updated = False  # Flag to track if any update has been made

        for line in config_lines:
            for face_name, new_path in face_mapping.items():
                if f'ui.faces.{face_name}' in line:
                    updated_lines.append(f'ui.faces.{face_name} = "{custom_faces_directory}/{face_name.upper()}.png"\n')
                    updated = True
                    break
            else:
                updated_lines.append(line)

        # Write the updated configuration file only if there was an update
        if updated:
            with open(config_file, 'w') as f:
                f.writelines(updated_lines)

            logging.info("Pwnagotchi configuration updated successfully.")
        else:
            logging.info("No updates needed in Pwnagotchi configuration.")

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
        logging.info("Restoring original Pwnagotchi configuration...")

        # Restore the original Pwnagotchi configuration file
        original_config = '/etc/pwnagotchi/config.toml.orig'
        config_file = '/etc/pwnagotchi/config.toml'

        # Copy the original configuration file to the current file
        os.system(f'cp {original_config} {config_file}')

        # Remove the original configuration file
        os.system(f'rm {original_config}')

        logging.info("Original Pwnagotchi configuration restored successfully.")

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

# Customize these paths accordingly
src_faces_directory = '/root/.pwnagotchi/egirl-pwnagotchi-master/faces'
dest_faces_directory = '/root/.pwnagotchi/custom-faces/egirl-pwnagotchi'

# Initialize the plugin
egirl_theme_plugin = EgirlThemePlugin()

# Move images to custom-faces directory
egirl_theme_plugin.move_images_to_custom_faces(src_faces_directory, dest_faces_directory)

# Modify paths in components.py
components_file = '/usr/local/lib/python3.9/dist-packages/pwnagotchi/ui/components.py'
egirl_theme_plugin.modify_paths_in_components(components_file, components_file, dest_faces_directory)

# Modify paths in view.py
view_file = '/usr/local/lib/python3.9/dist-packages/pwnagotchi/ui/view.py'
egirl_theme_plugin.modify_paths_in_view(view_file, view_file, dest_faces_directory)
