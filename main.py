from time import sleep, time
from classes.mojo import Mojo
from classes.Traffic import Traffic

import json
import os
import RPi.GPIO as gp

CMD_PATH = "ipc/command.json"
STATUS_PATH = "ipc/last_status.json"

# LCD sicher initialisieren
try:
    from classes.lcd import LCD
    lcd = LCD()
except:
    from classes.lcd_safe import NoLCD
    lcd = NoLCD()

# Instanzen
pk = Mojo()
light = Traffic()

def read_command():
    if os.path.exists(CMD_PATH):
        try:
            with open(CMD_PATH, "r") as f:
                cmd = json.load(f)
                return cmd.get("action")
        except:
            return None
    return None

def clear_command():
    with open(CMD_PATH, "w") as f:
        json.dump({}, f)

def write_status():
    with open(STATUS_PATH, "w") as f:
        json.dump({
            "frei": pk.get_parkp(),
            "tor_offen": pk.motor.pos > 0
        }, f)

# Start
print("🚀 Parkhaussystem gestartet...")
lcd.display_two_lines("Parkhaussystem", "gestartet...", True)
pk.auto_recovery()
light.test_buzz()
light.test_leds()

try:
    while True:
        freie_plaetze = pk.get_parkp()
        lcd.display_two_lines("Verfuegbar:", f"{freie_plaetze} Plaetze", True)
        write_status()

        # Sensor A (Einfahrt)
        if pk.is_activeted("a"):
            if freie_plaetze == 0:
                light.red_on(False)
                light.green_on(True, False)
                light.danger()
                lcd.display_two_lines("Kein Platz", "frei", True)
                sleep(2)
            else:
                light.red_on()
                light.green_on(False, False)
                lcd.display_two_lines("Einfahrt erkannt", ">>>", True)
                pk.einfahrt()

        # Sensor B (Ausfahrt)
        elif pk.is_activeted("b"):
            light.red_on()
            light.green_on(False, False)
            lcd.display_two_lines("Ausfahrt erkannt", "<<<", True)
            pk.ausfahrt()

        # Lichtsteuerung
        elif freie_plaetze == 0:
            light.red_on(False)
            light.green_on(True, False)
        elif freie_plaetze == 4:
            light.red_on(True, False)
            light.green_on(False, True)
        else:
            light.red_on(False, False)
            light.green_on()

        # IPC prüfen
        cmd = read_command()
        if cmd == "tor_auf":
            pk.tor_auf()
            clear_command()
        elif cmd == "tor_zu":
            pk.tor_zu()
            clear_command()

        sleep(0.1)

except KeyboardInterrupt:
    print("\n🚦 Manuell beendet.")
    lcd.display_two_lines("System gestoppt", "_x_", True)
    sleep(2)
finally:
    gp.cleanup()
    lcd.clear()
    pk.tor_zu()
