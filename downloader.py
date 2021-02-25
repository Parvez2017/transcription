from pytube import YouTube  
  
# where to save  
SAVE_PATH = "/media/parvej/ALL/trump" #to_do  
  
# links of the video to be downloaded  
# opening the file    
failed = []
with open('links.txt', 'r') as f:
    links = [line.strip('\n') for line in f.readlines()]
    
print(links)
for link in links:  
    try:  
        yt = YouTube(link)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().last()
        yt.download(SAVE_PATH)
    except:  
        #to handle exception 
        print("Connection Error")
        failed.append(link)


with open('failed_links.txt', 'w') as f:
    f.write("\n".join(failed))

print('Task Completed!')  