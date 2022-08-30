from django.shortcuts import render
from pytube import YouTube
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


def index(request):
    my_dict = {
        'color' : 'bodyclass',
    }
    return render(request, 'index.html',context=my_dict)

def ydown(request):
    my_dict = {
        'urls': None,
        'color': 'ytclass',
    }
    if request.method == 'POST':
        link = request.POST.get('link')
        SAVE_PATH = "./media"  
        try:
            yt = YouTube(link)
            print('Title: ',yt.title)
            #Length of the video
            print('Length of video: ',yt.length,'seconds')
        except:
            print("Connection Error")  # to handle exception
        d_video = yt.streams.all()
        print(d_video[1])
        try:
            dc = d_video[1].download(SAVE_PATH)
        except:
            print("Some Error!")

        print('Task Completed!')
        url = os.path.basename(dc)
        my_dict = {
            'urls': url,
        }

    return render(request, 'ydown.html', context=my_dict)
