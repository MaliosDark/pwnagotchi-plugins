#THIS IS A TEST. TO LOAD THE NEW UI USING JUST A PLUGIN.
#THIS PLUGIN IS BEING TESTED
#DO NOT USE UNTIL TEST ARE CONFIRMED AND RESULTS ARE AVAILABLE
#I DO INSIST!!
#JUST WAIT A BIT

# Plugin para activar/desactivar el tema egirl-pwnagotchi en Pwnagotchi

import pwnagotchi.plugins as plugins
import os

class EgirlThemePlugin(plugins.Plugin):
    __author__ = 'MaliosDark'
    __version__ = '1.0.3'
    __name__ = "Egirl Theme"
    __license__ = 'GPL3'
    __description__ = 'Plugin to activate/deactivate the egirl-pwnagotchi theme'

    def __init__(self):
        super().__init__()

        # Variable para rastrear si el tema está activado o desactivado
        self.theme_enabled = False

    def on_loaded(self):
        # Log para indicar que el tema se ha cargado
        self.logger.info("Egirl Theme loaded")

        # Configuración inicial al cargar el tema
        self.configure_theme()

    def configure_theme(self):
        # Ruta al directorio de pwnagotchi donde se almacenarán los archivos del tema
        pwnagotchi_directory = '/root/.pwnagotchi/'

        # URL al repositorio del tema egirl-pwnagotchi
        theme_repo = 'https://github.com/PersephoneKarnstein/egirl-pwnagotchi/archive/main.zip'

        # Descarga el archivo ZIP del repositorio del tema y lo extrae en el directorio de pwnagotchi
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

    def on_unload(self, ui):
        # Restaura la configuración original al descargar o desactivar el tema
        if self.theme_enabled:
            self.restore_original_config()

    def restore_original_config(self):
        # Restaura el archivo de configuración original de Pwnagotchi
        original_config = '/etc/pwnagotchi/config.toml.orig'
        config_file = '/etc/pwnagotchi/config.toml'

        # Copia el archivo de configuración original al archivo actual
        os.system(f'cp {original_config} {config_file}')

        # Elimina el archivo de configuración original
        os.system(f'rm {original_config}')

    def on_webhook(self, path, request):
        # Cambia el estado del tema (activado/desactivado) al recibir un webhook
        if path == 'egirl-theme/toggle':
            self.theme_enabled = not self.theme_enabled

            if self.theme_enabled:
                self.configure_theme()
            else:
                self.restore_original_config()

            # Devuelve una respuesta al cliente que realizó la solicitud
            return "Tema egirl-pwnagotchi " + ("activado" if self.theme_enabled else "desactivado")

