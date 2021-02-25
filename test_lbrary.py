from  pysubtitle import Subtile
from pys3 import Awss3
from pytranscrib import Transcib

# s3 = Awss3(aws_access_key_id='AKIAVQ4O4UA5EIJ5NMIW', aws_secret_access_key='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')
# audio_file = s3.video2audio('/media/parvej/ALL/trump/President Donald Trump I know how you feel but go home.mp4', 'trump')

# new_bucket = 'ticon-deep-fake-video'
#print(s3.create_bucket(new_bucket))
# print(s3.s3_bucketlist())

# s3_file = s3.upload_file(new_bucket, 'trump.wav', 'trump')
# print(s3_file)

# trancrib = Transcib(bucket=new_bucket, aws_access_key_id='AKIAVQ4O4UA5EIJ5NMIW', aws_secret_access_key='XsQ2hUfvhU92abzpVHJdquTTO6gukhLX8Jp6ZDIG')
# print(trancrib.transcribjob('s3://ticon-deep-fake-video/trump.wav', 'en-US'))
sub = Subtile('trump.json')
print(sub.transcribe('trump.wav'))