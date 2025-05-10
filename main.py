from time import sleep, time
from classes.Mojo import Mojo
from classes.LCD import LCD
from classes.Key import Manuell
from classes.Traffic import Traffic
import RPi.GPIO as gp
import sys
import select
import tty
import termios

# Initialisierung
pk = Mojo()
lcd = LCD()
light = Traffic()


# def tor_zu_mit_sicherheitscheck():
#     close_delay = 3
#     print("⬇️ Schranke fährt in", close_delay, "Sekunden runter...")
#     for i in range(close_delay):
#         if pk.is_activeted("a") or pk.is_activeted("b"):
#             print("⚠️ Sensor blockiert – Schranke öffnet wieder.")
#             pk.tor_auf()
#             return False
#         lcd.display_two_lines("⚠️ Schranke schließt", f"In {close_delay - i}s")
#         sleep(1)
#     pk.tor_zu()
#     return True

# def is_key_pressed():
#     dr, _, _ = select.select([sys.stdin], [], [], 0)
#     return dr

# def get_key():
#     fd = sys.stdin.fileno()
#     old = termios.tcgetattr(fd)
#     try:
#         tty.setraw(fd)
#         if is_key_pressed():
#             return sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old)
#     return None

# def menu_action(key):
#     if key == "m":
#         lcd.display_text("Manuell aktiviert",True)
#         print("🎮 Manuelle Steuerung gestartet...")
#         system = Manuell()
#         system.steuerung()
#         lcd.display_two_lines("Zuruck zum","System",True)

#     elif key == "s":
#         lcd.display_two_lines("🔍 STATUS", f"Frei: {pk.get_parkp()}")
#         print("📋 Status angezeigt")

#     elif key == "e":
#         lcd.display_text("⚙️ Einstellungen")
#         print("⚙️ Menü: Einstellungen – Platzlimit ändern (funktion vorbereitet)")
#         sleep(2)

#     elif key == "q":
#         lcd.display_text("🛑 Beendet")
#         print("❌ System wird beendet...")
#         sleep(2)
#         gp.cleanup()
#         lcd.clear()
#         sys.exit(0)

# Startinfo
print("🚀 Parkhaussystem gestartet...")


light.red_on()

pk.auto_recovery()

lcd.display_two_lines("Parkhaus bereit", f"Frei: {pk.get_parkp()}")
sleep(3)

light.red_on()
light.green_on()
light.led_off()

light.green_on()

light.cleanPi()

try:
    while True:
        #>>> Tasteneingaben prüfen <<<
        freie_plaetze = pk.get_parkp()
        lcd.display_two_lines("Verfuegbar:", f"{freie_plaetze} Plaetze",True)
        
        light.led_off(3)
        light.green_on()
        
        
        # Sensor A = Einfahrt
        if pk.is_activeted("a"):
            
            light.led_off(4)
            light.red_on()
            
            lcd.display_text("Einfahrt erkannt",True)
            pk.tor_auf()
            timeout = time() + 3
            
            while time() < timeout:
            
                if pk.is_activeted("b"):
                    lcd.display_two_lines("Haerzlich","Willkommen",True)
                    pk.drop_parkplatz()
                    break
                sleep(0.02)

        # Sensor B = Ausfahrt
        elif pk.is_activeted("b"):
            
            light.led_off(4)
            light.red_on()
            
            lcd.display_text("Ausfahrt erkannt",True)
            pk.tor_auf()
            timeout = time() + 3
            
            while time() < timeout:
                
                if pk.is_activeted("b"):
                    lcd.display_two_lines("Auf","Wiedersehen",True)
                    pk.add_parkplatz()
                    break
                
                sleep(0.02)

        sleep(0.02)

except KeyboardInterrupt:
    print("\n🚦 Programm manuell beendet.")
    lcd.display_text("System gestoppt",True)
    sleep(2)
finally:
    gp.cleanup()
    lcd.clear()
