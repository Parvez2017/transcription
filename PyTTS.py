import pyttsx3
from pydub import AudioSegment

engine = pyttsx3.init() # object creation

""" RATE"""
                     #printing current voice rate
engine.setProperty('rate', 150)     # setting up new voice rate
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)   

"""VOLUME"""
# volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# print (volume)                          #printing current volume level
# engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

# """VOICE"""
# voices = engine.getProperty('voices')       #getting details of current voice
# #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

# engine.say("Hello World!")
# engine.say('My current speaking rate is ' + str(rate))
# engine.runAndWait()
# engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
a=open('TrumpNewFF.srt').readlines()
i=2
l = len(a)
while i<l:
    engine.save_to_file(a[i], 'TTS/trump/{}.mp3'.format(str(i)))
    engine.runAndWait()
    if i+3<l:
        time_1 = a[i-1].split(' --> ')[1].split(':')
        time_1_mil = time_1[-1].split(',')
        time_1_mil = int(time_1_mil[0])*1000+int(time_1_mil[1])%1000
        time_1_hour = float(time_1[-2])*60000
        
        time_2 = a[i+3].split(' --> ')[0].split(':')
        time_2_hour = float(time_2[-2])*60000
        time_2_mil = time_2[-1].split(',')
        time_2_mil = int(time_2_mil[0])*1000+int(time_2_mil[1])%1000
        
        duration = float(time_2_hour+time_2_mil)-float(time_1_hour+time_1_mil)        
        # create 1 sec of silence audio segment
        one_sec_segment = AudioSegment.silent(duration=int(duration))  #duration in milliseconds
    
    
        print(i, duration, time_2_hour+time_2_mil, time_1_hour+time_1_mil)
        #Either save modified audio
        one_sec_segment.export('TTS/trump/{}.mp3'.format(str(i+1)), format="wav")
    i+=4
engine.stop()