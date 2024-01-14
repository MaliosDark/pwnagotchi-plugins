# Install dependencies: apt update; apt install nmap macchanger
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import os
import subprocess
import requests
import time
from pwnagotchi.ai.reward import RewardFunction
import socket
from reportlab.pdfgen import canvas
import datetime


READY = 0
STATUS = ''
NETWORK = ''
CHANNEL = 0

class EducationalPurposesOnly(plugins.Plugin):
    __author__ = '@nagy_craig , MaliosDark'
    __version__ = '1.0.2'
    __license__ = 'GPL3'
    __description__ = 'A plugin to automatically authenticate to known networks and perform internal network recon'

    def on_loaded(self):
        global READY
        logging.info("educational-purposes-only loaded")
        READY = 1
    
    def display_text(self, text):
        global STATUS
        STATUS = text
    
    def on_ui_update(self, ui):
        global STATUS
        while STATUS == 'rssi_low':
            ui.set('face', '(ﺏ__ﺏ)')
            ui.set('status', 'Signal strength of %s is currently too low to connect ...' % NETWORK)
        while STATUS == 'home_detected':
            ui.set('face', '(◕‿‿◕)')
            ui.set('face', '(ᵔ◡◡ᵔ)')
            ui.set('status', 'Found home network at %s ...' % NETWORK)
        while STATUS == 'switching_mon_off':
            ui.set('face', '(◕‿‿◕)')
            ui.set('face', '(ᵔ◡◡ᵔ)')
            ui.set('status', 'We\'re home! Pausing monitor mode ...')
        while STATUS == 'scrambling_mac':
            ui.set('face', '(⌐■_■)')
            ui.set('status', 'Scrambling MAC address before connecting to %s ...' % NETWORK)
        while STATUS == 'associating':
            ui.set('status', 'Greeting the AP and asking for an IP via DHCP ...')
            ui.set('face', '(◕‿◕ )')
            ui.set('face', '( ◕‿◕)')
        if STATUS == 'associated':
            ui.set('face', '(ᵔ◡◡ᵔ)')
            ui.set('status', 'Home at last!')


    def _connect_to_target_network(self, network_name, channel, interface='wlan0'):
        global READY
        global STATUS
        global NETWORK
        global CHANNEL

        NETWORK = network_name
        logging.info(f'sending command to Bettercap to stop using mon0 on {interface}...')
        STATUS = 'switching_mon_off'
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon off"}', auth=('pwnagotchi', 'pwnagotchi'))
        logging.info('ensuring all wpa_supplicant processes are terminated...')
        subprocess.Popen(f'systemctl stop wpa_supplicant; killall wpa_supplicant', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'disabling monitor mode on {interface}...')
        subprocess.Popen(f'modprobe --remove brcmfmac; modprobe brcmfmac', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        # Runs this driver reload command again because sometimes it gets stuck the first time:
        subprocess.Popen(f'modprobe --remove brcmfmac; modprobe brcmfmac', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'randomizing {interface} MAC address prior to connecting...')
        STATUS = 'scrambling_mac'
        subprocess.Popen(f'macchanger -A {interface}', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'setting hostname to a ^work dictionary word prior to connecting (for added stealth since their DHCP server will see this name)...')
        subprocess.Popen(f'hostnamectl set-hostname $(grep "^work" /usr/share/dict/words | grep -v "s$" | sort -u | shuf -n 1))', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info(f'starting up {interface} again...')
        subprocess.Popen(f'ifconfig {interface} up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(3)
        # This command runs multiple times because it sometimes doesn't work the first time:
        subprocess.Popen(f'ifconfig {interface} up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'setting {interface} channel to match the target...')
        STATUS = 'associating'
        subprocess.Popen(f'iwconfig {interface} channel {channel}', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        subprocess.Popen(f'ifconfig {interface} up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'writing to wpa_supplicant.conf file...')
        with open('/tmp/wpa_supplicant.conf', 'w') as wpa_supplicant_conf:
            wpa_supplicant_conf.write(f"ctrl_interface=DIR=/var/run/wpa_supplicant\nupdate_config=1\ncountry=GB\n\nnetwork={{\n\tssid=\"%s\"\n\tpsk=\"%s\"\n}}\n" % (network_name, self.options['home-password']))
        logging.info(f'starting wpa_supplicant background process on {interface}...')
        subprocess.Popen(f'ifconfig {interface} up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        subprocess.Popen(f'wpa_supplicant -u -s -c /tmp/wpa_supplicant.conf -i {interface} &', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'connecting to wifi on {interface}...')
        subprocess.Popen(f'ifconfig {interface} up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        subprocess.Popen(f'wpa_cli -i {interface} reconfigure', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info(f'trying to get an IP address on the network via DHCP on {interface}...')
        subprocess.Popen(f'dhclient {interface}', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)

        # Nueva mejora: Registrar la conexión exitosa
        self._log_successful_connection(network_name)
        STATUS = 'associated'
        READY = 1
        CHANNEL = channel  # Esta línea ya está presente al principio de la función
        NETWORK = network_name
        logging.info(f'sending command to Bettercap to stop using mon0 on {interface}...')



        
    def _restart_monitor_mode(self):
        logging.info('resuming wifi recon and monitor mode...')
        logging.info('stopping wpa_supplicant...')
        subprocess.Popen('systemctl stop wpa_supplicant; killall wpa_supplicant', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info('reloading brcmfmac driver...')
        subprocess.Popen('modprobe --remove brcmfmac && modprobe brcmfmac', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        logging.info('randomizing MAC address of wlan0...')
        subprocess.Popen('macchanger -A wlan0', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(10)
        subprocess.Popen('ifconfig wlan0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        logging.info('starting monitor mode...')
        subprocess.Popen('iw phy "$(iw phy | head -1 | cut -d" " -f2)" interface add mon0 type monitor && ifconfig mon0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        logging.info('telling Bettercap to resume wifi recon...')
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon on"}', auth=('pwnagotchi', 'pwnagotchi'))

    def on_epoch(self, ui):
        # If not connected to a wireless network and mon0 doesn't exist, run _restart_monitor_mode function
        if "Not-Associated" in subprocess.Popen('iwconfig wlan0').read() and "Monitor" not in subprocess.Popen('iwconfig mon0').read():
            self._restart_monitor_mode()

    def on_wifi_update(self, agent, access_points):
        global READY
        global STATUS
        home_network = self.options['home-network']
        if READY == 1 and "Not-Associated" in os.popen('iwconfig wlan0').read():
            for network in access_points:
                if network['hostname'] == home_network:
                    signal_strength = network['rssi']
                    channel = network['channel']
                    logging.info("FOUND home network nearby on channel %d (rssi: %d)" % (channel, signal_strength))
                    if signal_strength >= self.options['minimum-signal-strength']:
                        logging.info("Starting association...")
                        READY = 0
                        self._connect_to_target_network(network['hostname'], channel)
                    else:
                        logging.info("The signal strength is too low (%d) to connect." % (signal_strength))
                        STATUS = 'rssi_low'

    # Función para realizar la autenticación con varias redes
    def __init__(self, *args, **kwargs):
        super(EducationalPurposesOnly, self).__init__(*args, **kwargs)
        self.allowed_networks = ['Red1', 'Red2', 'Red3']


    def _port_scan(self, target_ip):
        open_ports = []
        for port in range(1, 1025):  # Rango común de puertos
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        logging.info(f"Open ports on {target_ip}: {open_ports}")

    # Función para generar un informe en PDF
    def _generate_report(self, file_path, content):
        with open(file_path, 'w') as pdf_file:
            pdf = canvas.Canvas(pdf_file)
            pdf.drawString(72, 800, "Informe de Actividades")
            pdf.drawString(72, 780, content)
            pdf.save()


    def on_ui_update(self, ui):
        global STATUS
        global NETWORK
        global CHANNEL 
        # ... (mantén o modifica según sea necesario)
        if STATUS == 'associated':
            ui.set('face', '(ᵔ◡◡ᵔ)')
            ui.set('status', f'Connected to {NETWORK} on channel {CHANNEL}.')
            ui.set('status_detail', 'Performing network reconnaissance...')


    # Notificaciones avanzadas
    def _send_notification(self, message, urgency='normal'):
        # Implementa notificaciones avanzadas aquí (por ejemplo, Pushbullet API).
        logging.info(f"Sending {urgency} notification: {message}")

    # Seguimiento de conexiones exitosas
    def _log_successful_connection(self, target_ip):
        logging.info(f"Successfully connected to {target_ip} at {datetime.datetime.now()}")