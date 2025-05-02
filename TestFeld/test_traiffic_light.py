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
