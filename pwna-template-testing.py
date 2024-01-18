#THIS IS A TEST. TO LOAD THE NEW UI USING JUST A PLUGIN.
#THIS PLUGIN IS BEING TESTED
#DO NOT USE UNTIL TESTS ARE CONFIRMED AND RESULTS ARE AVAILABLE
#I DO INSIST!!
#JUST WAIT A BIT

import subprocess
import sys
import os
import shutil
import logging

from pwnagotchi.ui.components import Widget, Text
import pwnagotchi.plugins as plugins

class EgirlThemePlugin(plugins.Plugin):
    __author__ = 'MaliosDark'
    __version__ = '1.2.0'
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
        self.install_dependencies()
        logging.info("Egirl Theme loaded")

        pwnagotchi_directory = '/custom-faces'
        theme_repo = 'https://github.com/PersephoneKarnstein/egirl-pwnagotchi/archive/master.zip'
        custom_faces_directory = self.download_and_extract(theme_repo, pwnagotchi_directory)
        self.update_config(custom_faces_directory)
        self.restart_pwnagotchi()

    def download_and_extract(self, url, destination):
        logging.info("Downloading and extracting theme files...")

        os.system(f'wget {url} -O /tmp/egirl-pwnagotchi-master.zip')
        os.system(f'unzip /tmp/egirl-pwnagotchi-master.zip -d {destination}')

        faces_directory = os.path.join(destination, 'egirl-pwnagotchi-master/faces')
        destination_directory = os.path.join(destination, 'egirl-pwnagotchi')
        os.makedirs(destination_directory, exist_ok=True)

        for file_name in os.listdir(faces_directory):
            source_path = os.path.join(faces_directory, file_name)
            destination_path = os.path.join(destination_directory, file_name)
            shutil.move(source_path, destination_path)

        logging.info("Theme files extracted and moved successfully.")
        return destination_directory

    def update_config(self, custom_faces_directory):
        logging.info("Updating Pwnagotchi configuration...")

        config_file = '/etc/pwnagotchi/config.toml'
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

        with open(config_file, 'r') as f:
            config_lines = f.readlines()

        updated_lines = []
        updated = False

        for line in config_lines:
            for face_name, new_path in face_mapping.items():
                if f'ui.faces.{face_name}' in line:
                    updated_lines.append(f'ui.faces.{face_name} = "{custom_faces_directory}/{face_name.upper()}.png"\n')
                    updated = True
                    break
            else:
                updated_lines.append(line)

        if updated:
            with open(config_file, 'w') as f:
                f.writelines(updated_lines)

            logging.info("Pwnagotchi configuration updated successfully.")
        else:
            logging.info("No updates needed in Pwnagotchi configuration.")

    def modify_paths_in_components(self, source_file, destination_file, custom_faces_directory):
        logging.info("Modifying paths in components.py...")

        # Backup components.py
        backup_file = '/files-backup/components.py'
        shutil.copy(source_file, backup_file)

        # Modify components.py
        with open(source_file, 'r') as f:
            content = f.read()

        modified_content = content.replace(
            'class Text(Widget):',
            'class Text(Widget):\n    def __init__(self, value="", position=(0, 0), font=None, color=0, wrap=False, max_length=0, png=False):\n        super().__init__(position, color)\n        self.value = value\n        self.font = font\n        self.wrap = wrap\n        self.max_length = max_length\n        self.wrapper = TextWrapper(width=self.max_length, replace_whitespace=False) if wrap else None\n        self.png = png\n\n    def draw(self, canvas, drawer):\n        if self.value is not None:\n            if not self.png:\n                if self.wrap:\n                    text = \'\\n\'.join(self.wrapper.wrap(self.value))\n                else:\n                    text = self.value\n                drawer.text(self.xy, text, font=self.font, fill=self.color)\n            else:\n                self.image = Image.open(self.value)\n                self.image = self.image.convert(\'RGBA\')\n                self.pixels = self.image.load()\n                for y in range(self.image.size[1]):\n                    for x in range(self.image.size[0]):\n                        if self.pixels[x,y][3] < 255:    # check alpha\n                            self.pixels[x,y] = (255, 255, 255, 255)\n                if self.color == 255:\n                    self._image = ImageOps.colorize(self.image.convert(\'L\'), black = "white", white = "black")\n                else:\n                    self._image = self.image\n                self.image = self._image.convert(\'1\')\n                canvas.paste(self.image, self.xy)'
        )

        with open(destination_file, 'w') as f:
            f.write(modified_content)

        logging.info("Modified components.py successfully.")

    def modify_paths_in_view(self, source_file, destination_file, custom_faces_directory):
        logging.info("Modifying paths in view.py...")

        # Backup view.py
        backup_file = '/files-backup/view.py'
        shutil.copy(source_file, backup_file)

        # Modify view.py
        with open(source_file, 'r') as f:
            content = f.read()

        modified_content = content.replace(
            "'face': Text(value=faces.SLEEP, position=self._layout['face'], color=BLACK, font=fonts.Huge),",
            "'face': Text(value=faces.SLEEP, position=(config['ui']['faces']['position_x'], config['ui']['faces']['position_y']), color=BLACK, font=fonts.Huge, png=config['ui']['faces']['png']),"
        )

        with open(destination_file, 'w') as f:
            f.write(modified_content)

        logging.info("Modified view.py successfully.")

    def move_images_to_custom_faces(self, src_directory, dest_directory):
        logging.info("Moving images to custom-faces directory...")

        # Ensure destination directory exists
        os.makedirs(dest_directory, exist_ok=True)

        # Move images
        for file_name in os.listdir(src_directory):
            source_path = os.path.join(src_directory, file_name)
            destination_path = os.path.join(dest_directory, file_name)
            shutil.move(source_path, destination_path)

        logging.info("Images moved to custom-faces directory successfully.")

    def modify_paths(self):
        # Customize these paths accordingly
        src_faces_directory = '/custom-faces/egirl-pwnagotchi-master/faces'
        dest_faces_directory = '/custom-faces/egirl-pwnagotchi'

        # Move images to custom-faces directory
        self.move_images_to_custom_faces(src_faces_directory, dest_faces_directory)

        # Modify paths in components.py
        components_file = '/usr/local/lib/python3.9/dist-packages/pwnagotchi/ui/components.py'
        self.modify_paths_in_components(components_file, components_file, dest_faces_directory)

        # Modify paths in view.py
        view_file = '/usr/local/lib/python3.9/dist-packages/pwnagotchi/ui/view.py'
        self.modify_paths_in_view(view_file, view_file, dest_faces_directory)

    def uninstall(self):
        logging.info("Uninstalling Egirl Theme...")

        # Revertir cambios en config.toml
        config_file = '/etc/pwnagotchi/config.toml'
        with open(config_file, 'r') as f:
            config_lines = f.readlines()

        updated_lines = [line for line in config_lines if 'ui.faces.' not in line]

        with open(config_file, 'w') as f:
            f.writelines(updated_lines)

        # Revertir cambios en components.py
        components_file = '/usr/local/lib/python3.9/dist-packages/pwnagotchi/ui/components.py'
        backup_file = '/files-backup/components.py'
        shutil.copy(backup_file, components_file)

        # Revertir cambios en view.py
        view_file = '/usr/local/lib/python3.9/dist-packages/pwnagotchi/ui/view.py'
        backup_file = '/files-backup/view.py'
        shutil.copy(backup_file, view_file)

        logging.info("Egirl Theme uninstalled successfully.")

