from classes.key import *
from classes.mojo import ParkhausSystem as pk
import classes.lcd as screen 


# die freie verfügbare Parkplätze 
FreeP = pk.get_parkp()

#screen.lcd_string(FreeP,LCD_LINE_1)

if __name__ == "__main__":
    pk().run()
    system.steuerung()
    