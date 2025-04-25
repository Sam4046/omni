import smbus2 as smbus
import time

# Adresse des I2C-LCDs
I2C_ADDR = 0x27
LCD_WIDTH = 16  # Für ein 16x2 Display

# LCD Befehle
LCD_CHR = 1  # Zeichenmodus
LCD_CMD = 0  # Befehlsmodus

LCD_LINE_1 = 0x80  # Erste Zeile
LCD_LINE_2 = 0xC0  # Zweite Zeile

ENABLE = 0b00000100  # Enable Bit
BACKLIGHT = 0x08  # Hintergrundbeleuchtung EIN

# Initialisiere I2C (Bus 1 für Raspberry Pi)
bus = smbus.SMBus(1)

def lcd_byte(bits, mode):
    try:
        high = mode | (bits & 0xF0) | BACKLIGHT | ENABLE
        low = mode | ((bits << 4) & 0xF0) | BACKLIGHT | ENABLE
        bus.write_byte(I2C_ADDR, high)
        bus.write_byte(I2C_ADDR, high & ~ENABLE)
        bus.write_byte(I2C_ADDR, low)
        bus.write_byte(I2C_ADDR, low & ~ENABLE)
    except Exception as e:
        print(f"I2C-Fehler: {e}")

def lcd_init():
    time.sleep(0.5)
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.5)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, ' ')
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

def user_input_display():
    while True:
        user_input = input("Gib etwas ein (oder 'exit' zum Beenden): ")
        if user_input.lower() == 'exit':
            break
        lcd_string(user_input[:16], LCD_LINE_1)
        time.sleep(2)
        lcd_byte(0x01, LCD_CMD)  # Display löschen

def calculate_expression():
    while True:
        expression = input("Gib eine Rechnung ein (oder 'exit' zum Beenden): ")
        if expression.lower() == 'exit':
            break
        try:
            result = str(eval(expression))
        except Exception as e:
            result = "Fehler!"
        lcd_string(expression[:16], LCD_LINE_1)
        lcd_string(result[:16], LCD_LINE_2)
        time.sleep(3)
        lcd_byte(0x01, LCD_CMD)

def timer_function():
    seconds = int(input("Gib die Timer-Dauer in Sekunden ein: "))
    for i in range(seconds, 0, -1):
        lcd_string(f"Timer: {i}s", LCD_LINE_1)
        time.sleep(1)
    lcd_string("Zeit abgelaufen!", LCD_LINE_1)
    time.sleep(2)
    lcd_byte(0x01, LCD_CMD)

if __name__ == "__main__":
    lcd_init()
    while True:
        print("\nWähle eine Option:")
        print("1: Text anzeigen")
        print("2: Rechnung berechnen")
        print("3: Timer starten")
        print("4: Beenden")
        choice = input("Auswahl: ")
        lcd_byte(0x01, LCD_CMD)
        
        if choice == '1':
            user_input_display()
        elif choice == '2':
            calculate_expression()
        elif choice == '3':
            timer_function()
        elif choice == '4':
            lcd_string("Auf Wiedersehen", LCD_LINE_1)
            time.sleep(2)
            lcd_byte(0x01, LCD_CMD)
            break
        else:
            print("Ungültige Auswahl!")
