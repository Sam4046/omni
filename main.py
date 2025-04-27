import RPi.GPIO as gp
from gpiozero import OutputDevice
import csv
import os  # Für Datei-Existenzprüfung
from time import sleep, time
import sys
import termios
import tty
from classes.key import *
from classes.mojo import ParkhausSystem as pk
import classes.lcd as screen 

# gp.setmode(gp.BOARD) # Board Pins (deaktiviert)
gp.setmode(gp.BCM) # Mode in pi nach GPIO Pins numm

# Sensore definieren
gp.setup(24, gp.IN, pull_up_down=gp.PUD_UP) 
gp.setup(25, gp.IN, pull_up_down=gp.PUD_UP)

# die freie verfügbare Parkplätze 
FreeP = pk.get_parkp()

#screen.lcd_string(FreeP,LCD_LINE_1)

if __name__ == "__main__":
    pk().run()
    system.steuerung()
    