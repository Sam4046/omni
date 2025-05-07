from time import sleep as out
import RPi.GPIO as GPIO



class Traffic:
    def __init__(self,
        red_en = 7,
        green_en = 8,
        red_ex = 4,
        green_ex = 17,
        buzzer = 27,
        ):

        GPIO.setmode(GPIO.BCM)

        self.red_en = red_en
        self.green_en = green_en
        self.red_ex = red_ex
        self.green_ex = green_ex
        self.buzzer = buzzer

        self.list_led_low = ["low_all", 
                             "low_en", 
                             "low_ex", 
                             "low_red_en", 
                             "low_green_en", 
                             "low_red_ex", 
                             "low_green_ex"
                             ]
        
        #LEDs and Buzzer definieren
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
# Traffic Light Controller
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
           
    def led_off(self, mode="low_all"):

        """ 
            mode indexex 
            0. All OFF     | 
            1. Entry OFF   | 2. Exit OFF    |
            3. Red Entry   | 4. Green Entry | 
            5. Red Exit    | 6. Green Exit  |
        """

        if isinstance(mode, int):
            if 0 <= mode < len(self.list_led_low):
                mode = self.list_led_low[mode]
            else:
                print(f"[Warnung] Ungültiger Index für led_off(): {mode}")
                return
        elif mode not in self.list_led_low:
            print(f"[Warnung] Ungültiger Modusname für led_off(): {mode}")
            return

        if mode == "low_all":
            GPIO.output(self.red_en, 0)
            GPIO.output(self.green_en, 0)
            GPIO.output(self.red_ex, 0)
            GPIO.output(self.green_ex, 0)

        elif mode == "low_en":
            GPIO.output(self.red_en, 0)
            GPIO.output(self.green_en, 0)
            
        elif mode == "low_ex":
            GPIO.output(self.red_ex, 0)
            GPIO.output(self.green_ex, 0)

        elif mode == "low_red_en":
            GPIO.output(self.red_en, 0)

        elif mode == "low_green_en":
            GPIO.output(self.green_en, 0)

        elif mode == "low_red_ex":
            GPIO.output(self.red_ex, 0)

        elif mode == "low_green_ex":
            GPIO.output(self.green_ex, 0)

    #Seriene
    def danger(self,sleepTime=0.3):
        self.high_buz()
        out(sleepTime)
        self.high_buz(False)

    def cleanPi(self):
        GPIO.cleanup()
