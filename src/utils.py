from pytube import YouTube
  
# creating function
def return_video_name(url):
      
    return YouTube(url).title