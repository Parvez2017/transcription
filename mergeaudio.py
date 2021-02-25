from moviepy.editor import *
from os import listdir
from os.path import isfile, join

mypath = 'TTS/trump'
onlyfiles = [int(f.split('.mp3')[0]) for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.sort()
audio_list = []
duration = 0
for i in range(len(onlyfiles)):
    onlyfiles[i]=str(onlyfiles[i])+'.mp3'
    try:
        audio_list.append(AudioFileClip('TTS/trump/'+onlyfiles[i]) )
        duration+=AudioFileClip('TTS/trump/'+onlyfiles[i]).duration
        print(i, duration)
        
    except:
        pass
# videoclip = AudioFileClip("out_sine.wav")
# audioclip = AudioFileClip("test1.mp3")
aaaaa=concatenate_audioclips(audio_list)
aaaaa.write_audiofile('New Test.mp3')