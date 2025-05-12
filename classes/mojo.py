import RPi.GPIO as gp
from gpiozero import OutputDevice
import csv
import os  # Für Datei-Existenzprüfung
from time import sleep, time
from LCD import LCD 
import random as rnd
# gp.setmode(gp.BOARD) # Board Pins (deaktiviert)
gp.setmode(gp.BCM) # Mode in pi nach GPIO Pins numm

# Sensore definieren
gp.setup(24, gp.IN, pull_up_down=gp.PUD_UP) 
gp.setup(25, gp.IN, pull_up_down=gp.PUD_UP)
v = LCD()

class Mojo:
    def __init__(self):
        
        # Motorsteuerung
        # Stepmotor hat 14, 15, 18 und 23 GPIO (siehe Bilder)
        self.motor_pins = [OutputDevice(pin) for pin in [14, 15, 18, 23]] 
        self.step_sequence = [
            [1, 0, 0, 0], 
            [1, 1, 0, 0], 
            [0, 1, 0, 0], 
            [0, 1, 1, 0],
            [0, 0, 1, 0], 
            [0, 0, 1, 1], 
            [0, 0, 0, 1], 
            [1, 0, 0, 1]
            ]
        
        self.heyMsg=["Hallo","Moin","Willkommen","Viel Spass!","Guten Tag"]
        self.beyMsg=["Tciao","Tschuess","Adios","Auf Wiedersehen","Schoenen Tag noch"]
        
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
        closing = True
        for _ in range(steps): 
            if (direction == 1 and self.pos >= self.max_schritte) or (direction == -1 and self.pos <= 0):
                break
            
        # Sicherheitsabbruch beim Schließen, falls Sensor aktiv
            if direction == -1 and (self.is_activeted("a") or self.is_activeted("b")):
                print("🛑 Sensor erkannt während Schließen! Tor wird erneut geöffnet.")
                self.tor_auf()
                sleep(3)
                self.tor_zu()
                return

                
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
    def tor_zu(self):
    # Time 
        if self.pos > 0:
            self.step_motor(self.pos, direction=-1)                
            
# Funktion fuer die Einfahrtprozess
    def einfahrt(self):
        if self.parkp > 0:
            print("🚗 Einfahrt erkannt. Schranke öffnet...")
            self.tor_auf()
            timeout = time() + 3  # Maximale Wartezeit für Sensor
            
            while time() < timeout:
                if not gp.input(self.irs_exit):
                    v.display_text(rnd.randint(self.heyMsg))  
                    self.drop_parkplatz()
                    self.tor_zu()
                    return
                sleep(0.02)  # Schnellere Erkennung
            
            print("❌ Einfahrt abgebrochen. Schranke fährt runter...")
            self.tor_zu(0)
        return self.parkp
            
# Funktion fuer die Ausfahrtprozess
    def ausfahrt(self):
        if self.parkp < self.max_pp:
            print("🚙 Ausfahrt erkannt. Schranke öffnet...")
            self.tor_auf()
            timeout = time() + 3  # Maximale Wartezeit für Sensor
            
            while time() < timeout:
                if not gp.input(self.irs_enter): 
                    v.display_text(rnd.randint(self.beyMsg))    
                    self.add_parkplatz()
                    self.tor_zu()
                    return
                sleep(0.02)  # Schnellere Erkennung
            
            print("❌ Ausfahrt abgebrochen. Schranke fährt runter...")
            self.tor_zu(0)
            
        else:
            print("🚫 Kein registriertes Auto im Parkhaus, Ausfahrt verweigert!")

        return self.parkp

    def get_parkp(self):
        return self.parkp
    
    def is_activeted(self,val):
        val = val.lower()

        if val == "a":
            return not gp.input(self.irs_enter)
        elif val == "b"  :
            return not gp.input(self.irs_exit) 
        else:
            print ("kein Sensor aktiv.")
            return False
        