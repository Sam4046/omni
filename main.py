from classes.Key import *
from classes.Mojo import ParkhausSystem as pk
import classes.LCD as screen 
from classes.Traffic import Traffic as tr

# die freie verfügbare Parkplätze 
FreeP = pk.get_parkp()

#screen.lcd_string(FreeP,LCD_LINE_1)

if __name__ == "__main__":
    pk().run()
    system.steuerung()
    