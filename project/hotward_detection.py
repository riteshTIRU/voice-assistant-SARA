import speech_recognition as sr
import os



def takecommand():
    '''
    it takes input from microphone and return
    text as an output

    Recognizer class helps to recognize audio

    '''
    r = sr.Recognizer()
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
        return query.lower()

while True:
    query = takecommand()

    if 'wake up sara' in query or 'sara' in query:
        #path of main file
        os.startfile('C:\\Users\\91988\\Desktop\\project\\speak.py')
        #\\ inter lining , Prevent from error

    else:
        print("WAITING FOR CALL......")