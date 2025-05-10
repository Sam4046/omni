import RPi.GPIO as gp
from time import sleep, time
from classes.Mojo import Mojo
from classes.LCD import LCD
from classes.Key import Manuell
import sys
import select
import tty
import termios

# GPIO vorbereiten
gp.setmode(gp.BCM)

# Initialisierung
pk = Mojo()
view = LCD()

def tor_zu_mit_sicherheitscheck():
    close_delay = 3
    print("⬇️ Schranke fährt in", close_delay, "Sekunden runter...")
    for i in range(close_delay):
        if pk.is_activeted("a") or pk.is_activeted("b"):
            print("⚠️ Sensor blockiert – Schranke öffnet wieder.")
            pk.tor_auf()
            return False
        view.display_two_lines("Schranke schließt", f"In {close_delay - i}s")
        sleep(1)
    pk.tor_zu()
    return True

def is_key_pressed():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    return dr

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        if is_key_pressed():
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return None

def menu_action(key):
    if key == "m":
        view.display_text("Manuell aktiviert",True)
        print("🎮 Manuelle Steuerung gestartet...")
        system = Manuell()
        system.steuerung()
        view.display_two_lines("Zuruck zum","System",True)

    elif key == "s":
        view.display_two_lines("STATUS", f"Frei: {pk.get_parkp()}")
        print("📋 Status angezeigt")

    elif key == "e":
        view.display_text("⚙️ Einstellungen")
        print("⚙️ Menü: Einstellungen – Platzlimit ändern (funktion vorbereitet)")
        sleep(2)

    elif key == "q":
        view.display_text("🛑 Beendet")
        print("❌ System wird beendet...")
        sleep(2)
        gp.cleanup()
        view.clear()
        sys.exit(0)

# Startinfo
print("🚀 Parkhaussystem gestartet...")
pk.auto_recovery()
view.display_two_lines("Parkhaus bereit", f"Frei: {pk.get_parkp()}")

try:
    while True:
        # >>> Tasteneingaben prüfen <<<
        key = get_key()
        if key in ["m", "s", "e", "q"]:
            menu_action(key)

        freie_plaetze = pk.get_parkp()
        view.display_two_lines("Verfügbar:", f"{freie_plaetze} Plätze")

        # Sensor A = Einfahrt
        if pk.is_activeted("a"):
            view.display_text("Einfahrt erkannt")
            pk.tor_auf()
            timeout = time() + 4
            while time() < timeout:
                if not gp.input(25):
                    pk.drop_parkplatz()
                    tor_zu_mit_sicherheitscheck()
                    break
                if pk.is_activeted("a") or pk.is_activeted("b"):
                    pk.tor_auf()
                    timeout = time() + 4
                sleep(0.1)

        # Sensor B = Ausfahrt
        elif pk.is_activeted("b"):
            view.display_text("Ausfahrt erkannt")
            pk.tor_auf()
            timeout = time() + 4
            while time() < timeout:
                if not gp.input(24):
                    pk.add_parkplatz()
                    # tor_zu_mit_sicherheitscheck()
                    break
                if pk.is_activeted("a") or pk.is_activeted("b"):
                    pk.tor_auf()
                    timeout = time() + 4
                sleep(0.1)

        sleep(0.2)

except KeyboardInterrupt:
    print("\n🚦 Programm manuell beendet.")
    view.display_text("System gestoppt")
    sleep(2)
finally:
    gp.cleanup()
    view.clear()
