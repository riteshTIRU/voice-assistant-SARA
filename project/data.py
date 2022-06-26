import datetime
import threading

if __name__=="__main__":
    time = input("Enter the time !(THROUGH KEYBOARD)(hh:mm:ss)(24 HOUR FORMAT)")
    time = time.replace(":"," ")
    print(time)

    multi=1
    nu = 0
    print(type(time))
    for word in time.split():
        if word.isdigit():
            print("inside IF")
            num = word
            nu = nu + (int(word)*3600)/multi
            multi=multi*60

    print(type(int(nu)))

