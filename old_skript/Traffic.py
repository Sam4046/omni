from time import sleep as out
import RPi.GPIO as GPIO



class Traffic:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.red_en = 7
        self.green_en = 8
        self.red_ex = 4
        self.green_ex = 17
        self.buzzer = 27

        self.list_led_low = ["low_all", 
                             "low_en", 
                             "low_ex", 
                             "low_red_en", 
                             "low_green_en", 
                             "low_red_ex", 
                             "low_green_ex"
                             ]

        GPIO.setup(self.red_en, GPIO.OUT)
        GPIO.setup(self.green_en, GPIO.OUT)
        GPIO.setup(self.red_ex, GPIO.OUT)
        GPIO.setup(self.green_ex, GPIO.OUT)
        GPIO.setup(self.buzzer, GPIO.OUT)

#buzzer on/off
    def high_buz(self,on=True):
        if on:
            GPIO.output(self.buzzer, 1)
        else:
            GPIO.output(self.buzzer, 0)

    def red_on(self,en=True,ex=True,alone=False):
        if not alone:
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

        else:
            if en:
                GPIO.output(self.red_en, 1)
            else:
                GPIO.output(self.red_ex, 1)

    def green_on(self,en=True,ex=True,alone=False):

        if not alone:
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
        else:
            if en:
                GPIO.output(self.green_en, 1)
            if ex:
                GPIO.output(self.green_ex, 1)
           
    def led_off (self,mode=0):
        """ 
            mode indexex 
            0. All OFF     | 
            1. Entry OFF   | 2. Exit OFF    |
            3. Red Entry   | 4. Green Entry | 
            5. Red Exit    | 6. Green Exit  |
        """
        if self.list_led_low[0] == self.list_led_low[mode]:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.green_en, 0)
            GPIO.output(self.red_ex, 0)
            GPIO.output(self.green_ex, 0)
        elif self.list_led_low[1] == self.list_led_low[mode]:
            GPIO.output(self.red_en, 0)
            GPIO.output(self.green_en, 0)
        elif self.list_led_low[2] == self.list_led_low[mode]:
            GPIO.output(self.red_ex, 0)
            GPIO.output(self.green_ex, 0)
        elif self.list_led_low[3] == self.list_led_low[mode]:
            GPIO.output(self.red_en, 0)
        elif self.list_led_low[4] == self.list_led_low[mode]:
            GPIO.output(self.green_en, 0)
        elif self.list_led_low[5] == self.list_led_low[mode]:
            GPIO.output(self.red_ex, 0)
        elif self.list_led_low[6] == self.list_led_low[mode]:
            GPIO.output(self.green_ex, 0)
        else: 
            print(f"[Warnung] Ungültiger Index für led_off(): {mode}")

    def denger(self,sleepTime=0.3):
        self.high_buz()
        out(sleepTime)
        self.high_buz(False)

    def claer(self):
        GPIO.cleanup()
