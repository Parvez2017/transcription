from  pysubtitle import Subtile
from pys3 import Awss3
from pytranscrib import Transcib
import os 
import glob 
import re 


path = '/media/parvej/ALL/parvez/audiobook_trans'
files = glob.glob('/media/parvej/ALL/parvez/audiobook_trans/*.wav')
files = sorted(files, key=lambda x:float(re.findall("(\d+)",x)[0]))
print(files)

for file in files:
    basename = os.path.basename(file).split('.')[0]
    sub = Subtile(f'{path}/{basename}.json')
    sub.transcribe(f'{path}/{basename}.wav')
    print('transcription done!...')