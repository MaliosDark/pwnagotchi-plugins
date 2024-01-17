#THIS IS A TEST. TO LOAD THE NEW UI USING JUST A PLUGIN.
#THIS PLUGIN IS BEING TESTED
#DO NOT USE UNTIL TEST ARE CONFIRMED AND RESULTS ARE AVAILABLE
#I DO INSIST!!
#JUST WAIT A BIT
#COMMENTS ARE ON SPANISH AT THE MOMENT

# Plugin para activar el tema egirl-pwnagotchi en Pwnagotchi

import pwnagotchi.plugins as plugins
import os

class EgirlThemePlugin(plugins.Plugin):
    __author__ = 'MaliosDark'

    def on_loaded(self):
        # Ruta al directorio de pwnagotchi donde se almacenarán los archivos del tema
        pwnagotchi_directory = '/root/.pwnagotchi/'

        # Ruta al repositorio del tema egirl-pwnagotchi
        theme_repo = 'https://github.com/PersephoneKarnstein/egirl-pwnagotchi/archive/main.zip'

        # Descarga el archivo ZIP del repositorio del tema
        self.download_and_extract(theme_repo, pwnagotchi_directory)

        # Configura el archivo de configuración de Pwnagotchi con las nuevas rutas de las caras personalizadas
        self.update_config()

    def download_and_extract(self, url, destination):
        # Descarga el archivo ZIP del repositorio del tema
        os.system(f'wget {url} -O /tmp/egirl-pwnagotchi.zip')

        # Extrae el contenido del ZIP al directorio de pwnagotchi
        os.system(f'unzip /tmp/egirl-pwnagotchi.zip -d {destination}')

    def update_config(self):
        # Actualiza el archivo de configuración de Pwnagotchi con las nuevas rutas de las caras personalizadas
        config_file = '/etc/pwnagotchi/config.toml'

        # Diccionario que mapea las caras originales a las nuevas rutas
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

        # Lee el archivo de configuración existente
        with open(config_file, 'r') as f:
            config_lines = f.readlines()

        # Modifica las líneas correspondientes con las nuevas rutas de las caras personalizadas
        updated_lines = []
        for line in config_lines:
            for face_name, new_path in face_mapping.items():
                if f'ui.faces.{face_name}' in line:
                    updated_lines.append(f'ui.faces.{face_name} = "/custom-faces/egirl-pwnagotchi/{face_name.upper()}.png"\n')
                    break
            else:
                updated_lines.append(line)

        # Escribe el archivo de configuración actualizado
        with open(config_file, 'w') as f:
            f.writelines(updated_lines)

# Registra el plugin
plugins.register_plugin(EgirlThemePlugin())
