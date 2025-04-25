def show_case(val):
        hello_msg= "Willkommen"
        gbey_msg = "Auf Wiedersehen"
        warning_msg = "Zurckfahren Bitte"
        noPlace_msg = "Kein Platz frei"
        stop_msg = "Stop"
        start_msg = "Auf geht's"
        msg = ""
        
        if val== 1:
                msg = hello_msg
        elif val== 2:
                msg = gbey_msg
        elif val== 3:
                msg = warning_msg
        elif val== 4:
                msg = noPlace_msg
        elif val== 5:
                msg = stop_msg 
        elif val== 6:
                msg= start_msg
        
        print (msg)
    
show_case(6)