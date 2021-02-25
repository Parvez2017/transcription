import boto3
import datetime
from botocore.exceptions import ClientError
import requests
import json
import os


class Subtile:
    
    
    def __init__(self, JsonFileLocation):
        self.JsonFileLocation = JsonFileLocation
        
    
    def getTimeCode(self, seconds ):
    # Format and return a string that contains the converted number of seconds into vtt format
       return seconds 
    
    
        
    def GetWordsFromJson(self):
        File = open(self.JsonFileLocation, 'r')
        ReadJson = File.read()
        LoadJson = json.loads(ReadJson)
        result = LoadJson['results']['speaker_labels']['segments']
        word = LoadJson['results']['items']
        
        speaker_label = []
        create_line = []
        new_line = []
        punc = 0
        end_time = 0
        for ii in result:
            for j in ii['items']:
                
                speaker_label.append(j['speaker_label'])
        for i in word:
            if i['type']!='punctuation':
                WordDetails = {}
                WordDetails['start_time'] = i['start_time']
                WordDetails['end_time'] = i['end_time']
                WordDetails['word'] = i['alternatives'][0]['content']
                create_line.append(WordDetails)
                if float(WordDetails['start_time'])-float(end_time)>=2.0:
                    punc=0
                    new_line.append(end_time)
                end_time = i['end_time']
            else:
                punc+=1
                create_line[-1]['word'] = create_line[-1]['word']+i['alternatives'][0]['content']
                
                if punc==2:
                    punc = 0
                    new_line.append(end_time)
                elif i['alternatives'][0]['content']!=',':
                    # create_line[-1]['word'] = create_line[-1]['word']+'<br>'
                    create_line[-1]['word'] = create_line[-1]['word']
                
        l = len(speaker_label)
        global new_result
        new_result = []
        
        for i in range(l):
            value = {}
            value['s_t'] = create_line[i]['start_time']
            value['e_t'] = create_line[i]['end_time']
            value['word'] = create_line[i]['word']
            value['speaker'] = speaker_label[i]
            new_result.append(value)
            
    
        phrase =  {}
        phrase['words'] = []
        phrases = []
        nPhrase = True
        i = 0
        speaker = ''
        for item in new_result:
            if nPhrase == True:
                speaker = item['speaker']
                phrase = {}
                phrase["start_time"] = self.getTimeCode( float(item["s_t"]) )
                phrase['words'] = []
                
                nPhrase = False
            
            
    
            if item['e_t'] in new_line:
                phrase['words'].append(item['word'])
    #            print(item['e_t'])
                i+=1
                phrase["end_time"] = self.getTimeCode( float(item["e_t"]) )
                phrases.append(phrase)
                nPhrase = True
            elif speaker!=item['speaker']:
    #            print(speaker)
                speaker = item['speaker']
                phrase["end_time"] = self.getTimeCode( float(item["e_t"]) )
                phrases.append(phrase)
                speaker = item['speaker']
                phrase = {}
                phrase["start_time"] = self.getTimeCode( float(item["s_t"]) )
                phrase['words'] = [item['word']]
                
            else:
                phrase['words'].append(item['word'])
            
        return phrases
    
    
    def transcribe(self, filename):
        transcripts = []
        try:
            JsonFile = self.GetWordsFromJson()
            for i in range(len(JsonFile)):
                stime = str(JsonFile[i]['start_time']
                etime = str(JsonFile[i]['end_time'])
                tran = ' '.join(JsonFile[i]['words'])
                transcripts.append(tran)
            
            with open(f'{filename}.txt', 'w') as f:
                f.write('\n'.join(transcripts))
        except:
            print('transcriptions failed')
    
    def subtitle(self, filename):
        
            
        try:
            JsonFile = self.GetWordsFromJson()
            vtt_file = '{}.srt'.format(filename)
            
        
            vtt = open(vtt_file,'w')
            for i in range(len(JsonFile)):
                vtt.write(str(i+1)+'\n')
                vtt.write(str(JsonFile[i]['start_time'])+' --> '+ str(JsonFile[i]['end_time'])+'\n')
                vtt_value = ' '.join(JsonFile[i]['words'])+'\n\n'     
                
                
                vtt.write(vtt_value.replace('\n ','\n'))
            vtt.close()
            
            return {'status':"Subtitle write complete", 'vtt_file':vtt_file,}
        except:
            return {'status':'Subtitle write Failed', 'vtt_file':''}
    
    def GenerateSubtitleWithTranslate(self, filename, region_name, sourceLangCode, targetLangCode, 
                                      translate_aws_access_key_id='', translate_aws_secret_access_key=''):
        try:
            translate = boto3.client(
                'translate',
                aws_access_key_id=translate_aws_access_key_id,
                aws_secret_access_key=translate_aws_secret_access_key,
                region_name = region_name
            #    aws_session_token=SESSION_TOKEN,
            )
        
            
        except:
            return {'status':401, 'vtt_file':''}
        try:
            JsonFile = self.GetWordsFromJson()
            t_vtt_file = '{}'.format(filename)+sourceLangCode+'-'+targetLangCode+'.srt'
            t_vtt = open(t_vtt_file,'w')
            t_vtt.write('WEBVTT\n\n')
            vtt_file = '{}.srt'.format(filename)
            vtt = open(vtt_file,'w')
            
            
            for i in range(len(JsonFile)):
                vtt.write(str(i+1)+'\n')
                vtt.write(str(JsonFile[i]['start_time']).replace(',','.')+' --> '+ str(JsonFile[i]['end_time']).replace(',','.')+'\n')
                vtt_value = ' '.join(JsonFile[i]['words'])+'\n\n'     
                
                if sourceLangCode!=targetLangCode:
                    t_vtt.write('\n'+str(i+1)+'\n')
                    t_vtt.write(str(JsonFile[i]['start_time']).replace(',','.')+' --> '+ str(JsonFile[i]['end_time']).replace(',','.')+'\n')
                    t_vtt_value = translate.translate_text(Text=vtt_value.replace('<br>',''),SourceLanguageCode=sourceLangCode, TargetLanguageCode=targetLangCode)
                    if '<br>' in vtt_value:    
                        t_vtt.write(t_vtt_value['TranslatedText']+'<br>'+'\n\n')
                    else:
                        t_vtt.write(t_vtt_value['TranslatedText']+'\n\n')
                
                vtt.write(vtt_value.replace('\n ','\n'))
            vtt.close()
            
            if sourceLangCode!=targetLangCode:
                t_vtt.close()
                
            return {'status':"Subtitle write complete", 'vtt_file':vtt_file, 'translate_vtt_file':t_vtt_file}
        except:
            return {'status':'Subtitle write Failed', 'vtt_file':'', 'translate_vtt_file':''}
       
       
       
       
       
       