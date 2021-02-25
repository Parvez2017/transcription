import boto3
import datetime
from botocore.exceptions import ClientError
import requests

    
class Transcib:
    def __init__(self, bucket, region_name='ap-southeast-1', aws_access_key_id=None, aws_secret_access_key=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.bucket = bucket
        self.now = datetime.datetime.now()
        self.timestamp = datetime.datetime.timestamp(self.now)
        if self.aws_secret_access_key==None or self.aws_access_key_id==None:
            self.transcribe =  boto3.client(
                        'transcribe',
                )
        else:
            self.transcribe = boto3.client(
                                'transcribe',
                                aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key,
                                region_name = self.region_name
                        )
    def getTranscriptionJobStatus(self, jobName):
    
    
        response = self.transcribe.get_transcription_job( TranscriptionJobName=jobName )
        return response
    

    # purpose: get and return the transcript structure given the provided uri
    def getTranscript(self, transcriptURI , SaveJsonLocation=''):
        # Get the resulting Transcription Job and store the JSON response in transcript
        result = requests.get( transcriptURI )
        jsonfile = SaveJsonLocation+'{}.json'.format(self.File[0])
        create_json = open(jsonfile,'w')
        create_json.write(result.text)
        return jsonfile   
    
    
    def transcribjob(self, S3MediaURL, language, ShowSpeakerLabels=True, MaxSpeakerLabels=10, ChannelIdentification=False):
        
        # Set up the full uri for the bucket and media file
        mediaUri = S3MediaURL
        self.File = mediaUri.split('/')[-1].split('.')
        self.job_name = self.File[0]+str(self.timestamp)
        # Use the uuid functionality to generate a unique job name.  Otherwise, the Transcribe service will return an error
        response = self.transcribe.start_transcription_job(
            TranscriptionJobName=self.job_name,
            Media={'MediaFileUri': mediaUri},
            MediaFormat=self.File[-1],
            LanguageCode=language,
            Settings={
                'ShowSpeakerLabels': ShowSpeakerLabels,
                'MaxSpeakerLabels': MaxSpeakerLabels,
                'ChannelIdentification': ChannelIdentification
            }
        
        )
        key = True
        while(key):
            res = self.getTranscriptionJobStatus(self.job_name)
            if res['TranscriptionJob']['TranscriptionJobStatus']=='COMPLETED':
                key=False
            print('Generate Json File: '+res['TranscriptionJob']['TranscriptionJobStatus'])
        jsonfile = self.getTranscript(res['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        # return the response structure found in the Transcribe Documentation
        return jsonfile
    
    

    
    
