#import classes.lcd as view
#from classes.key import Manuell as k
import termios
import tty
import sys

def steuerung():
        print("\n🎮 **Manuelle Steuerung aktiviert** 🎮")
        print("W = Schritt hoch | S = Schritt runter")
        print("D = Tor auf | A = Tor zu | Q = Beenden\n")

        while True:
            key = get_key()
            if key == "w":
                print("⬆️ Schritt hoch")
                #self.step_motor(1, direction=1)
            elif key == "s":
                print("⬇️ Schritt runter")
                #self.step_motor(1, direction=-1)
            elif key == "d":
                print ("Tor auf")
                #self.tor_auf()
            elif key == "a":
                print("Tor zu")
                #self.tor_zu()
            elif key == "q":
                print("🚦 Beenden...")
                break

def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key.lower()

steuerung()
#view.user_input_display(6)