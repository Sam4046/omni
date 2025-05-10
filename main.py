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
        
        
# Einfahrt -> Sensor A aktiviert >> 
        if pk.is_activeted("a"):
            
            if pk.get_parkp() == 0:
                light.red_on(False)
                light.green_on(False,True)
                lcd.display_two_lines("Kein Platz","frei",True)
                sleep(2)
                
            else:
                light.red_on()
                light.green_on(False,False)
                lcd.display_two_lines("Einfahrt erkannt",">>>",True)
                pk.einfahrt()
            

# Ausfahrt -> Sensor B aktiviert >> 
        elif pk.is_activeted("b"):
            
            light.red_on()
            light.green_on(False,False)
            lcd.display_two_lines("Ausfahrt erkannt","<<<",True)
            pk.ausfahrt()
        
        

        sleep(0.02)

except KeyboardInterrupt:
    print("\n🚦 Programm manuell beendet.")
    lcd.display_two_lines("System gestoppt","_x_",True)
    sleep(2)
finally:
    gp.cleanup()
    lcd.clear()
    pk.tor_zu
