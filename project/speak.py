import sys
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import wikipedia
from playsound import playsound
import webbrowser
import os
import winsound
import pywhatkit
import pyjokes
import mysql.connector
import threading
import requests
from bs4 import BeautifulSoup #FOR WEB SCRAPING

engine = pyttsx3.init()
voices = engine.getProperty('voices')



# VOICE
engine.setProperty('voice', voices[0].id)

engine.setProperty('rate', 150)  # 120 is the best
# engine.setProperty('pitch', 180)


# DATA BASE CONNECTION
mydb = mysql.connector.connect(host="localhost", user="igris", passwd="qazwsxedc", database="record")

# CURSOR
mycursor = mydb.cursor()


# ******

# SPEAK
def speak(audio):
    if engine._inLoop:
        engine.endLoop()

    engine.say(audio)
    engine.runAndWait()



# INTRODUCTION PART
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("good morning !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")

    else:
        speak("Good Evening !")

    speak("Hello I am sara  , How may i help you")


def takecommand():
    '''
    it takes input from microphone and return
    text as an output

    Recognizer class helps to recognize audio

    '''

    r = sr.Recognizer()


    try:
        with sr.Microphone() as source:
            print("Listening ...")
            r.pause_threshold = 1  # 1 sec break will not complete the sentence
            r.energy_threshold = 800  # energy threshold for backround noise
            audio = r.listen(source)

            try:
                print("Recognizing ...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said : {query}\n")

            except Exception as e:
                # print("e")
                print("Say that again please")
                return "None"
            return query
    except Exception as e:
        print("Didn't found Micro Phone")

#OR BEEP SOUND
def alexa():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)
    wishme()


# SHUTDONW
def shutdown():
    mydb.close()
    speak("shutting down")


    sys.exit()


# OK GOT IT
def ok():
    speak("ok got it!")


# CLEAR DATA
def cleardata():
    print("ARE YOU SURE YOU WANT CLEAR ALL DATA (YES/NO)")

    speak("ARE YOU SURE YOU WANT CLEAR ALL DATA , YES OR NO")

    while True:
        query = takecommand().lower()

        if 'yes' in query:
            ok()
            mycursor.execute("delete from rem")
            mydb.commit()
            break
        elif 'no' in query:
            ok()
            break
        else:
            dk()


# CLEAR DATA FROM LAST
def clearpastdata():
    print("ARE YOU SURE YOU WANT THIS  DATA (YES/NO)")
    showoldest()
    speak("ARE YOU SURE YOU WANT THIS DATA , YES OR NO")

    while True:
        query = takecommand().lower()

        if 'yes' in query:
            ok()

            '''
            You can not delete the rows from the same data source which your sub query refers to. 
            Above mentioned query is a workaround, but it’s ugly for several reasons, including performance.
            Here nested sub query makes a temporary table. So it doesn’t count as the same table you’re trying to delete data from.
            In other words in MySQL, you can’t modify the same table which you use in the SELECT part. 
            This behaviour is documented
            '''

            mycursor.execute("delete from rem where Date_Time = (select * from (select min(Date_Time) from rem) AS x)")
            mydb.commit()
            speak("data deleted")
            break
        elif 'no' in query:
            ok()
            break

        elif 'shut down' in query:  # SHUTDOWN

            shutdown()


        elif 'shutdown' in query:  # SHUTDOWN
            shutdown()

        else:
            dk()





# CLEAR DATA FROM LASTEST
def clearlatestdata():
    print("ARE YOU SURE YOU WANT CLEAR THIS DATA (YES/NO)")
    showlatest()
    speak("ARE YOU SURE YOU WANT CLEAR THIS DATA , YES OR NO")

    while True:
        query = takecommand().lower()

        if 'yes' in query:
            ok()
            mycursor.execute("delete from rem where Date_Time = (select * from (select min(Date_Time) from rem) AS x)")

            mydb.commit()
            speak("Data deleted")
            break

        elif 'no' in query:
            ok()
            break
        elif 'shut down' in query:  # SHUTDOWN

            shutdown()


        elif 'shutdown' in query:  # SHUTDOWN
            shutdown()

        else:
            dk()


def dk():
    speak("I don't understand what you said")


def showlatest():
    mycursor.execute(
        "select * from rem where Date_Time=(SELECT max(Date_Time) FROM rem)")  # now = datetime.datetime.now()

    t = mycursor.fetchall()
    i = t[0]
    print("Date_Time                 What i  remember")
    print("--------------------------------------------------")
    print(str(i[0]) + "     " + i[1])

    print("\n")
    mycursor.execute("select info from rem")
    rs = mycursor.fetchone()
    speak(str(rs))


def showoldest():
    mycursor.execute(
        "select * from rem where Date_Time=(SELECT min(Date_Time) FROM rem)")  # now = datetime.datetime.now()

    t = mycursor.fetchall()
    i = t[0]
    print("Date_Time                 What i  remember")
    print("--------------------------------------------------")
    print(str(i[0]) + "     " + i[1])
    print("\n")

q2="hello" #global variable

def reminder():
    global q2
    speak(q2)


def Temp():
    search ="today's weather"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temperature = data.find("div",class_= "BNeawe").text
    print(temperature)
    speak(f"the tamperature is {temperature},Celsius")

#TIME TO SECONDS
def seconds(time):
    multi = 1
    nu = 0
    print(type(time))
    for word in time.split():
        if word.isdigit():

            num = word
            nu = nu + (int(word) * 3600) / multi
            multi = multi * 60
    return int(nu)

def alarm():

    speak("alarm set")
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    while True:
        winsound.Beep(frequency, duration)

        if "ok got it" in query:
            break

    speak("ALARM CLOSED!")

if __name__ == "__main__":


        alexa()

        while True:
            query = takecommand().lower()

            if 'wikipedia' in query :
                speak('Searching Wikipedia ... ')
                query = query.replace("who is", "").replace("what is","").replace("tell me","")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to wikipedia")

                except Exception as e:
                    speak("No result found!")
                    print("No result Found!")
                print(results)
                speak(results)

            elif 'sara' in query:
                sys.exit()

            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                webbrowser.open("google.com")

            elif ' the time' in query:
                Time = datetime.datetime.now().strftime("%I:%M %p")
                print(Time)
                speak("The time is" + Time)

            elif 'on youtube' in query:
                playcom = query.replace("play", "")
                speak(playcom)
                print(playcom)
                pywhatkit.playonyt(playcom)

#For Jokes
            elif 'joke' in query:
                speak(pyjokes.get_joke())


            # SEARCH
            elif 'search' in query:
                find = query.replace("search", "")
                print(find)
                pywhatkit.search(str(find))

            elif 'google' in query:
                find = query.replace("google", "")
                print(find)
                pywhatkit.search(str(find))

            # SEARCH


            # SHUT DOWN
            elif 'shut down' in query  or 'shutdown' in query:  # shut down

                shutdown()



            elif 'remember that' in query or 'remember this' in query:

                read = [(query.replace("remember this", ""))]

                mycursor.execute("insert into rem values (now(),%s)", (read))

                mydb.commit()
                speak("ok got it !")


            elif 'you have something to tell me' in query:

                # REMEMBER COMMAND

                # FETCH DATA FROM DATABASE

                while True:
                    mycursor.execute("select * from rem")
                    mycursor.fetchall()
                    rows_count = mycursor.rowcount

                    # print(rows_count)

                    if (rows_count == 1):

                        showlatest()

                        break


                    elif (rows_count > 1):
                        print("There are my things you tell me to remember")
                        speak("There are my things you tell me to remember")
                        print("Do you want me to show you all")
                        speak("Do you want me to show you all")
                        print("OR i tell you the last think i remember")
                        speak("OR i tell you the last think i remember")

                        query = takecommand().lower()

                        if "all" in query:
                            speak("Showing all data")
                            mycursor = mydb.cursor()
                            mycursor.execute("select * from rem")
                            result = mycursor.fetchall()
                            print("Date_Time                 What i  remember")
                            print("--------------------------------------------------")

                            for i in result:
                                print(str(i[0]) + "     " + i[1])

                            break






                        elif "last" in query:
                            mycursor.execute("select * from rem where Date_Time=(SELECT max(Date_Time) FROM rem)")

                            t = mycursor.fetchall()
                            i = t[0]
                            print("Date_Time                 What i  remember")
                            print("--------------------------------------------------")
                            print(str(i[0]) + "     " + i[1])
                            print("\n")


                            mycursor.execute("select info from rem where Date_Time=(SELECT max(Date_Time) FROM rem)")
                            rs = mycursor.fetchall()
                            speak(str(rs))
                            break





                        elif 'shut down' in query:  # SHUTDOWN

                            shutdown()


                        elif 'shutdown' in query:  # SHUTDOWN
                            shutdown()


                        else:
                            dk()



                    else:
                        speak("hmmm... I didn't remember anything")
                        break

            elif 'delete this' in query:
                clearlatestdata()

            elif 'last thing you remember' in query:
                mycursor.execute("select * from rem")
                mycursor.fetchall()
                rows = mycursor.rowcount
                print(rows)
                if int(rows) > 0:
                    showlatest()
                else:
                    speak("hmm....... I don't remember anything")

            # Timer
            elif 'from now' and ('remind me' or 'tell me') in query:

                a_string = query


                for word in a_string.split():
                    if word.isdigit():
                        num = word
                        nu = int(word)

                if 'second' in query:
                    t = 'second'

                    ti = nu

                elif 'minute' in query:

                    t = 'minute'

                    ti = (nu) * (60)

                elif 'hour' in query:
                    t = 'hour'

                    ti = (nu) * (60) * (60)

                else:
                    dk()

                if 'that' in query:
                    th = 'that'

                elif 'this' in query:
                    th = 'this'

                elif 'to' in query:
                    th = 'to'

                else:
                    th = ""


                q2= query.replace(num, "").replace(t, "").replace("remind me", "").replace(th, "").replace(
                    "i", "you").replace("from now", "").replace("tell me","")



                timer=threading.Timer(ti, reminder)
                ok()
                timer.start()

            elif "what is the temperature" in query or "today's weather" in query or "today's temperature" in query:
                Temp()


            elif "alarm" in query:
                speak("Enter The Time !:")
                try:
                    time = input("Enter the time !(THROUGH KEYBOARD)(hh:mm:ss)(24 HOUR FORMAT)")

                except Exception as e:
                    print("Your Input is in IMPROPER FORMAT")


                time = seconds(time)
                time_ac=datetime.datetime.now().time()
                current_time = time_ac.strftime("%H:%M:%S")
                current_time = seconds(current_time)
                ti = time-current_time
                zehar = threading.Timer(ti , alarm)
                ok()
                zehar.start()




            elif "what is " in query or "who is" in query or  "what's" in query or "tell me" in query:
                try :
                    pywhatkit.info(query.replace("tell me",""), lines = 2)

                except Exception as a:
                    print("Didn't get it")


                speak("here is what i found")







