from time import sleep as out
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

    GPIO.setup(red_en, GPIO.OUT)
    GPIO.setup(green_en, GPIO.OUT)
    GPIO.setup(red_ex, GPIO.OUT)
    GPIO.setup(green_ex, GPIO.OUT)
    GPIO.setup(red_ex, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)

    def high_buz(self,on=True):
        if on == True:
            GPIO.output(self.buzzer, 1)
        else:
            GPIO.output(self.buzzer, 0)

    def red_on(self,en=True,ex=True):
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
        if en and ex:
            GPIO.output(self.green_en, 1)
            GPIO.output(self.green_ex, 1)
        elif en and not ex:
            GPIO.output(self.green_en, 1)
            GPIO.output(self.green_ex, 0)
        elif not en and ex:    
            GPIO.output(self.green_en, 0)
            GPIO.output(self.green_ex, 1)
        else:
            GPIO.output(self.green_en, 0)
            GPIO.output(self.green_ex, 0)

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

    def denger(self,sleepTime=0.3):
        self.high_buz()
        out(sleepTime)
        self.high_buz(False)
        




    
    
    
    


