import logging
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK

class VoicePlugin(plugins.Plugin):
    __author__ = 'malios666@gmail.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A voice interface plugin for Pwnagotchi, giving voice to it.'

    def __init__(self):
        logging.debug("Voice plugin created")
        self.recognizer = None
        self.speech_engine = None

    def install_dependencies(self):
        try:
            import speech_recognition as sr
            import pyttsx3
        except ImportError:
            import subprocess
            subprocess.call(["pip", "install", "speechrecognition", "pyttsx3"])

    def on_loaded(self):
        logging.warning("WARNING: this plugin should be disabled!")
        self.install_dependencies()

        try:
            import speech_recognition as sr
            import pyttsx3
            self.recognizer = sr.Recognizer()
            self.speech_engine = pyttsx3.init()
        except ImportError:
            logging.error("Failed to import required modules.")

    def on_ui_setup(self, ui):
        ui.add_element('ups', LabeledValue(color=BLACK, label='UPS', value='0%/0V', position=(ui.width() / 2 - 25, 0),
                                           label_font=fonts.Bold, text_font=fonts.Medium))

    def on_ui_update(self, ui):
        some_voltage = 0.1
        some_capacity = 100.0
        ui.set('ups', "%4.2fV/%2i%%" % (some_voltage, some_capacity))

    def on_voice_command(self, command):
        if command == "hello":
            self.speak("Hello! How can I assist you?")
        elif command == "status":
            self.speak("The Pwnagotchi is currently operational.")
        # Add more commands and their corresponding actions here

    def speak(self, text):
        self.speech_engine.say(text)
        self.speech_engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                print("You said:", command)
                self.on_voice_command(command)
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def on_ready(self, agent):
        logging.info("Pwnagotchi is ready")
        self.listen()

    def on_internet_available(self, agent):
        self.speak("Internet connection is available.")

    def on_bored(self, agent):
        self.speak("The Pwnagotchi is feeling bored.")

    def on_sad(self, agent):
        self.speak("The Pwnagotchi is feeling sad.")

    def on_excited(self, agent):
        self.speak("The Pwnagotchi is feeling excited.")

    def on_lonely(self, agent):
        self.speak("The Pwnagotchi is feeling lonely.")

    def on_rebooting(self, agent):
        self.speak("The Pwnagotchi is rebooting.")

    def on_wait(self, agent, t):
        self.speak("The Pwnagotchi is waiting for {} seconds.".format(t))

    def on_sleep(self, agent, t):
        self.speak("The Pwnagotchi is sleeping for {} seconds.".format(t))

    def on_wifi_update(self, agent, access_points):
        self.speak("Wi-Fi access points updated.")

    def on_unfiltered_ap_list(self, agent, access_points):
        self.speak("Unfiltered access points list updated.")

    def on_association(self, agent, access_point):
        self.speak("Associated with access point: {}".format(access_point))

    def on_deauthentication(self, agent, access_point, client_station):
        self.speak("Deauthenticated client {} from access point {}".format(client_station, access_point))

    def on_channel_hop(self, agent, channel):
        self.speak("Hopping to channel {}".format(channel))

    def on_handshake(self, agent, filename, access_point, client_station):
        self.speak("Handshake captured from access point {} and client {}".format(access_point, client_station))

    def on_epoch(self, agent, epoch, epoch_data):
        self.speak("Epoch {} completed.".format(epoch))

    def on_peer_detected(self, agent, peer):
        self.speak("Peer {} detected.".format(peer))

    def on_peer_lost(self, agent, peer):
        self.speak("Lost connection with peer {}.".format(peer))
