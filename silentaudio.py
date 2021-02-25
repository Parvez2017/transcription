from pydub import AudioSegment
from pydub.playback import play

audio_in_file = "trump.wav"
audio_out_file = "out_sine.wav"

# create 1 sec of silence audio segment
one_sec_segment = AudioSegment.silent(duration=10000)  #duration in milliseconds



#Either save modified audio
one_sec_segment.export(audio_out_file, format="wav")

#Or Play modified audio
# play(final_song)