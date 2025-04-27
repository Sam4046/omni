import RPi.GPIO as gp
from gpiozero import OutputDevice
import csv
import os  # Für Datei-Existenzprüfung
from time import sleep, time
import sys
import termios
import tty
import lcd as v

# gp.setmode(gp.BOARD) # Board Pins (deaktiviert)
gp.setmode(gp.BCM) # Mode in pi nach GPIO Pins numm

# Sensore definieren
gp.setup(24, gp.IN, pull_up_down=gp.PUD_UP) 
gp.setup(25, gp.IN, pull_up_down=gp.PUD_UP)

class ParkhausSystem:
    def __init__(self):
        
        # Motorsteuerung
        self.motor_pins = [OutputDevice(pin) for pin in [14, 15, 18, 23]] # Stepmotor hat 14, 15, 18 und 23 GPIO (siehe Bilder)
        self.step_sequence = [
            [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
            [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
        ]
        
        self.pos = 0                # Definieren von Position 0 = Tor ist zu
        self.max_schritte = 130     # Nach 130 Schritten geht die Tor ist auf oder Max Position
        self.load_position()        # Letzte Position beim Start laden
        
        
        self.start = 0
        # Sensoren
        self.irs_enter = 24         # Eingangsensor hat GPIO 24 / pin 18 (siehe Bilder)
        self.irs_exit = 25          # Eingangsensor hat GPIO 25 / pin 22 (siehe Bilder)
        
        # Beide Sensor Definieren
        gp.setup([self.irs_enter, self.irs_exit], gp.IN) 

        # Parkplaetze Variabln
        self.max_pp = 4     # maximale Parkplaetze
        self.min_pp = 0     # minimalte Parkplaetze
        self.parkp = 4      # Aktuell frei
        
        
    def auto_recovery(self):
        self.tor_zu(0)
        
     
# Speichert die aktuelle Position in einer CSV-Datei        
    def save_position(self):
        with open("last_pos.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.pos])  # ✅ Die Datei enthält immer nur eine Zeile mit der aktuellen Position
            file.flush()  # ✅ Sofort auf Festplatte schreiben

# Liest die letzte gespeicherte Position aus der Datei
    def load_position(self):
        if os.path.exists("last_pos.csv"):
            with open("last_pos.csv", "r") as file:
                reader = csv.reader(file)
                try:
                    self.pos = int(next(reader)[0])  # Erste Zeile lesen
                    print(f"🔄 Letzte gespeicherte Position geladen: {self.pos}")
                except (StopIteration, ValueError):
                    self.pos = 0  # Falls Datei leer oder fehlerhaft ist
        else:
            self.pos = 0  # Standardwert falls keine Datei existiert

#Funktion zum einen Parkplatz frei zu stellen
    def add_parkplatz(self):
        if self.parkp < self.max_pp:
            self.parkp += 1
            print("Ein Parkplatz ist jetzt frei ➕.", self.parkp)

#Funktion zum einen Parkplatz zu reservieren    
    def drop_parkplatz(self):
        if self.parkp > self.min_pp:
            self.parkp -= 1
            print("Ein Parkplatz ist jetzt reserviert ➖.", self.parkp)
        else:
            print("🛑 Kein Parkplatz frei!")    

# Funktion Schritte zu zaehlen 
    def set_step(self, values):
        for pin, value in zip(self.motor_pins, values):
            pin.value = value

# Funktion Schritte zu fahren.
    def step_motor(self, steps, direction=1):
        # Scleife lauft bis Tor ganz auf oder zu
        for _ in range(steps): 
            if (direction == 1 and self.pos >= self.max_schritte) or (direction == -1 and self.pos <= 0):
                break
            for step in (self.step_sequence if direction > 0 else reversed(self.step_sequence)): # wenn direction 1 nach Uhrzeigen ausserdenn rueckwerts
                self.set_step(step) 
                sleep(0.002)  # Motorbeschleunigung (1 sek / 500 )
            self.pos += direction
            self.save_position()
        # Speichert die aktuelle Position nach jeder Bewegung
        

# Funktoin Rampa hoch
    def tor_auf(self):
        if self.pos < self.max_schritte:
            self.step_motor(self.max_schritte - self.pos, direction=1)

# Funktoin Rampa hoch
    def tor_zu(self,time=3):
    # Time 
        if self.pos > 0:
            self.step_motor(self.pos, direction=-1)       
    # Timerzaehler       
        if time > 0:
            i=0
            print (" ⬇️ die Rampe fährt runter in :") 
            for i in range(time):
                sleep(1)
                i +=1
                print (" ... ",i)
            print (" Tor ist zu ") 
            
# Funktion fuer die Einfahrtprozess
    def einfahrt(self):
        if self.parkp > 0:
            print("🚗 Einfahrt erkannt. Rampe öffnet...")
            self.tor_auf()
            
            timeout = time() + 3  # Maximale Wartezeit für Sensor
            
            while time() < timeout:
                if not gp.input(self.irs_exit):  
                    self.drop_parkplatz()
                    self.tor_zu()
                    return
                sleep(0.02)  # Schnellere Erkennung
            
            print("❌ Einfahrt abgebrochen. Rampe fährt runter...")
            self.tor_zu(0)
        return self.parkp
            
# Funktion fuer die Ausfahrtprozess
    def ausfahrt(self):
        if self.parkp < self.max_pp:
            print("🚙 Ausfahrt erkannt. Rampe öffnet...")
            self.tor_auf()
            timeout = time() + 3  # Maximale Wartezeit für Sensor
            
            while time() < timeout:
                if not gp.input(self.irs_enter):  
                    self.add_parkplatz()
                    self.tor_zu()
                    return
                sleep(0.02)  # Schnellere Erkennung
            
            print("❌ Ausfahrt abgebrochen. Rampe fährt runter...")
            self.tor_zu(0)
            
        else:
            print("🚫 Kein registriertes Auto im Parkhaus, Ausfahrt verweigert!")

        return self.parkp

    def get_parkp(self):
        return self.parkp
# Hauptprogramm 
    def run(self):
        try:
            print("🚀 Parkhaussystem gestartet... 🚀🚀🚀")
            #self.auto_recovery()
            while True:
                if not gp.input(self.irs_enter):
                    self.einfahrt()
                if not gp.input(self.irs_exit):
                    self.ausfahrt()
                sleep(0.02)  # Schnellere Hauptschleife
        except KeyboardInterrupt:
            print("\n🚦 Programm beendet.")
        finally:
            self.set_step([0, 0, 0, 0])
            gp.cleanup()
