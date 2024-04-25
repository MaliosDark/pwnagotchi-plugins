import logging
import time
import threading
import subprocess
import os
from scapy.all import ARP, Ether, srp
from flask import Flask, render_template_string
import pwnagotchi.plugins as plugins
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK  
import pwnagotchi.ui.fonts as fonts

class SecurityPlugin(plugins.Plugin):
    __author__ = 'MaliosDark'
    __version__ = '1.9.93'
    __license__ = 'GPL3'
    __description__ = 'The Security Plugin for Pwnagotchi is a comprehensive tool designed to enhance network monitoring and security capabilities on the Pwnagotchi platform. With a focus on simplicity and effectiveness, this plugin provides real-time insights into the network environment, allowing users to take proactive security measures.'

    def __init__(self):
        logging.debug("Security plugin created")
        self.detected_pwnagotchi_count = 0
        self.security_action_options = ["Do Nothing", "Alert User", "Change Wi-Fi Channel"]
        self.selected_security_action = self.security_action_options[0]  # Default to changing Wi-Fi channel
        self.ethernet_scan_results = "No scan results yet"
        self.is_scapy_installed = self.check_scapy_installed()
        self.target_ip = "192.168.68.1"  # Default target IP, can be edited through UI
        self.monitoring_interval = 10  # Default monitoring interval in seconds
        self.ethernet_scan_interval = 300  # Default Ethernet scan interval in seconds
        self.app = Flask(__name__)
        self.app.add_url_rule('/ethernet-scan-results', 'ethernet_scan_results', self.ethernet_scan_results_page)
        self.web_thread = threading.Thread(target=self.run_web)
        self.web_thread.start()

    def run_web(self):
        self.app.run(host='0.0.0.0', port=8888, debug=False)

    def ethernet_scan_results_page(self):
        return render_template_string('<pre>{{ results }}</pre>', results=self.ethernet_scan_results)


    def on_loaded(self, ui):
        logging.debug("Security plugin loaded")
        logging.basicConfig(level=logging.DEBUG)

        # Check and install scapy if needed
        if not self.is_scapy_installed:
            self.install_scapy()

        # Start a thread to monitor the network
        monitoring_thread = threading.Thread(target=self.monitor_network, args=(ui,))
        monitoring_thread.start()
        logging.debug("Monitoring thread started.")

        # Start a thread for Ethernet scanning
        ethernet_scan_thread = threading.Thread(target=self.ethernet_scan)
        ethernet_scan_thread.start()
        logging.debug("Ethernet scan thread started.")

        # Start a separate thread for UI updates
        ui_update_thread = threading.Thread(target=self.ui_update_handler, args=(ui,))
        ui_update_thread.start()
        logging.debug("UI update thread started.")

    def on_ui_setup(self, ui):
        # Add custom UI elements
        ui.add_element('security_status', LabeledValue(color=BLACK, label='Security Status', value='OK',
                                                       position=(ui.width() / 2 - 50, 0), label_font=fonts.Bold,
                                                       text_font=fonts.Medium))

        ui.add_element('detected_pwnagotchi', LabeledValue(color=BLACK, label='Detected Pwnagotchi:',
                                                           value='',
                                                           position=(10, 40),
                                                           label_font=fonts.Medium,
                                                           text_font=fonts.Medium))

        ui.add_element('security_actions', LabeledValue(color=BLACK, label='Security Actions:',
                                                         value='',
                                                         position=(10, 80),
                                                         label_font=fonts.Medium,
                                                         text_font=fonts.Medium))

        # Add a button to access Ethernet scan results
        ui.add_element('scan_button', LabeledValue(color=BLACK, label='Scan Ethernet',
                                                    value='',
                                                    position=(ui.width() / 2 - 25, 120),
                                                    label_font=fonts.Medium,
                                                    text_font=fonts.Medium,
                                                    on_press=self.show_ethernet_scan_results))

        # Add a text input for configuring the target IP
        ui.add_element('target_ip_input', LabeledValue(color=BLACK, label='Target IP:',
                                                        value=str(self.target_ip),
                                                        position=(10, 160),
                                                        label_font=fonts.Medium,
                                                        text_font=fonts.Medium,
                                                        on_change=self.update_target_ip))

        # Add text inputs for configuring monitoring and Ethernet scan intervals
        ui.add_element('monitoring_interval_input', LabeledValue(color=BLACK, label='Monitoring Interval (s):',
                                                                 value=str(self.monitoring_interval),
                                                                 position=(10, 200),
                                                                 label_font=fonts.Medium,
                                                                 text_font=fonts.Medium,
                                                                 on_change=self.update_monitoring_interval))

        ui.add_element('ethernet_scan_interval_input', LabeledValue(color=BLACK, label='Ethernet Scan Interval (s):',
                                                                    value=str(self.ethernet_scan_interval),
                                                                    position=(10, 240),
                                                                    label_font=fonts.Medium,
                                                                    text_font=fonts.Medium,
                                                                    on_change=self.update_ethernet_scan_interval))
        
        # Subscribe to UI updates for detected pwnagotchi and security actions
        ui.subscribe(self, 'detected_pwnagotchi', 'security_actions')
        

    def on_ui_update(self, ui):
        ui.set('security_status', "OK" if self.is_security_ok() else "Alert")
        ui.set('security_actions', f'  {self.selected_security_action}')
        ui.set('detected_pwnagotchi', f'  {self.detected_pwnagotchi_count}')
        ui.update()


    def check_scapy_installed(self):
        try:
            # Try to import scapy
            import scapy.all
            return True
        except ImportError:
            return False

    def install_scapy(self):
        # Install scapy using pip
        os.system("pwnagotchi plug scapy --install")

    def monitor_network(self, ui):
        logging.debug("Monitoring thread is running.")
        while True:
            try:
                detected_pwnagotchi = self.detect_pwnagotchi_nearby()

                if detected_pwnagotchi:
                    self.display_detected_pwnagotchi(ui, detected_pwnagotchi)
                    self.take_security_actions(ui)
                else:
                    ui.set('detected_pwnagotchi', 'No Pwnagotchi detected yet...')
                    logging.debug('No Pwnagotchi detected yet...')

                time.sleep(self.monitoring_interval)

            except Exception as e:
                logging.error(f"Error in network monitoring: {e}")

    def detect_pwnagotchi_nearby(self):
        try:
            # Use ARP requests to find devices on the network (Wi-Fi)
            wifi_target_ip = self.target_ip
            wifi_request = ARP(pdst=wifi_target_ip)
            wifi_response, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / wifi_request, timeout=2, verbose=0)

            # Lista para almacenar direcciones MAC detectadas
            detected_macs = []

            # Check if there is any response in Wi-Fi
            if wifi_response:
                # Check if any of the responses is from a Pwnagotchi device
                for _, received in wifi_response:
                    detected_macs.append(received.hwsrc)
                    if "Pwnagotchi" in received.hwsrc:
                        return True

            # Use ARP requests to find devices on the network (Ethernet)
            try:
                ethernet_result = subprocess.check_output(["arp-scan", "--localnet"], universal_newlines=True)
                ethernet_detected_macs = [line.split()[1] for line in ethernet_result.splitlines()]

                # Log de direcciones MAC detectadas en Wi-Fi y Ethernet
                logging.debug(f"Detected MAC addresses (Wi-Fi): {detected_macs}")
                logging.debug(f"Detected MAC addresses (Ethernet): {ethernet_detected_macs}")

                # Combina las direcciones MAC detectadas en ambas interfaces
                all_detected_macs = set(detected_macs + ethernet_detected_macs)

                # Verifica si alguna dirección MAC pertenece a un dispositivo Pwnagotchi
                for mac in all_detected_macs:
                    if "Pwnagotchi" in mac:
                        return True

            except Exception as e_ethernet:
                # Manejar errores en la detección de Ethernet
                logging.error(f"Error during Ethernet scan: {e_ethernet}")

            # No Pwnagotchi devices detected
            return False

        except Exception as e:
            # Manejar errores en la detección de Wi-Fi
            logging.error(f"Error detecting Pwnagotchi nearby: {e}")
            return False
    def display_detected_pwnagotchi(self, ui, detected_pwnagotchi):
        if detected_pwnagotchi:
            self.detected_pwnagotchi_count += 1
            ui.set('detected_pwnagotchi', f' : {self.detected_pwnagotchi_count}')
            logging.debug(f' : {detected_pwnagotchi}')

            # Seleccionar una acción basada en la detección
            self.select_security_action(detected_pwnagotchi)
            self.take_security_actions(ui)
        else:
            ui.set('detected_pwnagotchi', 'None detected yet...')
            logging.debug('No Pwnagotchi detected yet...')

        ui.update()

    def select_security_action(self, detected_pwnagotchi):
        # Lógica para seleccionar la acción de seguridad basada en la detección
        if detected_pwnagotchi:
            # Pwnagotchi detectado, seleccionar acción correspondiente
            self.selected_security_action = "Alert User"
        else:
            # Ningún Pwnagotchi detectado, seleccionar acción por defecto
            self.selected_security_action = "Change Wi-Fi Channel"

    def take_security_actions(self, ui):
        try:
            if self.selected_security_action == "Change Wi-Fi Channel":
                self.change_wifi_channel()
            elif self.selected_security_action == "Alert User":
                self.alert_user(ui)
            elif self.selected_security_action == "Do Nothing":
                pass

            logging.debug(f'Took security actions: {self.selected_security_action}')

        except Exception as e:
            logging.error(f"Error in taking security actions: {e}")

        ui.set('security_actions', f'Security Actions: {self.selected_security_action}')
        ui.update()



    def change_wifi_channel(self):
        # Logic for changing Wi-Fi channel
        try:
            # Use pwnagotchi's API to execute bettercap commands
            command = "ble.recon on"
            self.execute_bettercap_command(command)

            # Log the success
            logging.debug("Changed Wi-Fi channel successfully.")
        except Exception as e:
            # Handle any errors that may occur during the channel change
            logging.error(f"Error changing Wi-Fi channel: {e}")

    def execute_bettercap_command(self, command):
        # Execute a bettercap command using pwnagotchi's API
        try:
            os.system(f"pwnagotchi bettercap '{command}'")
        except Exception as e:
            logging.error(f"Error executing bettercap command: {e}")

    def alert_user(self, ui):
        # Logic for alerting the user
        try:
            # Set UI elements
            ui.set('security_status', "Alert")
            ui.set('security_actions', f'Security Actions: Alert - Detected Pwnagotchi!')

            # Display message on the screen
            os.system("pwnagotchi display 'Alert: Detected Pwnagotchi!'")

            # Log the alert
            logging.debug("Alerted user about detected Pwnagotchi.")
        except Exception as e:
            # Handle any errors that may occur during the alert process
            logging.error(f"Error alerting user: {e}")


    def is_security_ok(self):
        # Logic to determine if security is okay
        # For demonstration, security is considered okay if no pwnagotchi is detected
        return not self.detect_pwnagotchi_nearby()

    def ethernet_scan(self):
        logging.debug("Ethernet scan thread is running.")
        while True:
            try:
                result = subprocess.check_output(["arp-scan", "--localnet"], universal_newlines=True)
                lines = result.split('\n')
                if lines:
                    self.ethernet_scan_results = result
                    logging.debug("Ethernet scan successful.")
                else:
                    logging.warning("No results obtained during Ethernet scan.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error during Ethernet scan (CalledProcessError): {e}")
                self.ethernet_scan_results = "Error during scan."
            except Exception as e:
                logging.error(f"Error during Ethernet scan: {e}")
                self.ethernet_scan_results = "Error during scan."

            time.sleep(self.ethernet_scan_interval)


    def show_ethernet_scan_results(self):
        # Log the Ethernet scan results
        logging.info(self.ethernet_scan_results)

    def ui_update_handler(self, ui):
        logging.debug("UI update thread is running.")
        while True:
            try:
                ui.set('ethernet_scan_results', f'Ethernet Scan Results: {self.ethernet_scan_results}')
                ui.update()
                time.sleep(60)

            except Exception as e:
                logging.error(f"Error in UI update handler: {e}")

    def update_target_ip(self, value):
        # Update the target IP based on the user input
        self.target_ip = value

    def update_monitoring_interval(self, value):
        # Update the monitoring interval based on the user input
        try:
            self.monitoring_interval = int(value)
        except ValueError:
            logging.warning("Invalid monitoring interval value. Please enter a valid integer.")

    def update_ethernet_scan_interval(self, value):
        # Update the Ethernet scan interval based on the user input
        try:
            self.ethernet_scan_interval = int(value)
        except ValueError:
            logging.warning("Invalid Ethernet scan interval value. Please enter a valid integer.")

