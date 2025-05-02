import time as t
import RPi.GPIO as GPIO

# GPIO-Setup
GPIO.setmode(GPIO.BCM)





class Traffic:

    GPIO.setmode(GPIO.BCM)
    red_en = 7
    green_en = 8
    red_ex = 4
    green_ex = 17
    buzzer = 27

    GPIO.setup(self.red_en, GPIO.OUT)
    GPIO.setup(self.green_en, GPIO.OUT)
    GPIO.setup(self.red_ex, GPIO.OUT)
    GPIO.setup(self.green_ex, GPIO.OUT)
    GPIO.setup(self.red_ex, GPIO.OUT)
    GPIO.setup(self.buzzer, GPIO.OUT)

    def red_on(self,en=True,ex=True):
        led_off()
        if en and ex:
            GPIO.output(self.red_en, 1)
            GPIO.output(self.red_ex, 1)
        elif en and not ex:
            GPIO.output(self.red_en, 1)
            GPIO.output(self.red_ex, 0)
        elif not en and ex:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.red_ex, 1)
        else:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.red_ex, 0)

    def green_on(self,en=True,ex=True):
        led_off()
        if en and ex:
            GPIO.output(self.red_en, 1)
            GPIO.output(self.red_ex, 1)
        elif en and not ex:
            GPIO.output(self.red_en, 1)
            GPIO.output(self.red_ex, 0)
        elif not en and ex:    
            GPIO.output(self.red_en, 0)
            GPIO.output(self.red_ex, 1)
        else:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.red_ex, 0)

        



    


    def high_buz(self,on=True):
        if on == True:
            GPIO.output(self.buzzer, 1)
        else:
            GPIO.output(self.buzzer, 0)

    def led_off (self,lowAll=True,en=False):
        if lowAll:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.green_en, 0)
            GPIO.output(self.red_ex, 0)
            GPIO.output(self.green_ex, 0)
        elif en:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.green_en, 0)
        else:
            GPIO.output(self.red_ex, 0)
            GPIO.output(self.green_ex, 0)



    
    # LEDs ausschalten
    led_off()

           
    # def red_on(self):
    #     led_off()
    #     print('led off')
    #     GPIO.output(red_en, 1)
    #     print('red entry on')
    #     GPIO.output(red_ex, 1)
    #     print('red exit on')

    # def green_on(): 
    #     led_off()
    #     print('red exit on')
    #     GPIO.output(green_en, 1)
    #     print('red exit on')
    #     GPIO.output(green_ex, 1)
    #     print('red exit on')

    # def buz():
    #     GPIO.output(buzzer, 1)
    #     t.sleep(0.5)
    #     GPIO.output(buzzer, 0)
    
    


try:
    while True:
        request = input("Modus wählen (1 = Police, 2 = Alarm, 0 = Stop): ")

        if request == "1":
            red_on()
        elif request == "2":
            green_on()
        elif request == "3":
            buz()
        elif request == "4":
            all_mix()
        
        

        elif request == "0":
            print("Programm beendet.")
            break
        else:
            print("Ungültige Eingabe. Grün wird aktiviert.")
            GPIO.output(green_en, 1)
            t.sleep(2)
            GPIO.output(green_en, 0)

except KeyboardInterrupt:
    print("\nProgramm manuell unterbrochen.")

finally:
    GPIO.cleanup()
    print("GPIO-Pins zurückgesetzt.")
