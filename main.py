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


# Startinfo
print("🚀 Parkhaussystem gestartet...")

lcd.display_two_lines("Parkhaussystem", f"gestartet...",True)

light.red_on()

pk.auto_recovery()

lcd.display_two_lines("Parkhaus bereit", f"Frei: {pk.get_parkp()}",True)
sleep(3)

light.red_on()
light.led_off()

light.green_on()


try:
    while True:
        #>>> Tasteneingaben prüfen <<<
        freie_plaetze = pk.get_parkp()
        lcd.display_two_lines("Verfuegbar:", f"{freie_plaetze} Plaetze",True)
        
        light.red_on(False,False)
        light.green_on()
        
        
# Sensor A aktiviert >> Einfahrt
        if pk.is_activeted("a"):
            
            light.red_on()
            light.green_on(False,False)
            lcd.display_text("Einfahrt erkannt",True)
            pk.einfahrt()
            

# Sensor B aktiviert >> Ausfahrt
        if pk.is_activeted("b"):
            
            light.red_on()
            light.green_on(False,False)
            lcd.display_text("Ausfahrt erkannt",True)
            pk.ausfahrt()

        sleep(0.02)

except KeyboardInterrupt:
    print("\n🚦 Programm manuell beendet.")
    lcd.display_text("System gestoppt",True)
    sleep(2)
finally:
    gp.cleanup()
    lcd.clear()
