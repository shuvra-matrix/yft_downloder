from django.shortcuts import render
from pytube import YouTube
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


def index(request):
    my_dict = {
        'urls': None,
    }
    if request.method == 'POST':

        link = request.POST.get('link')
        SAVE_PATH = "./media"  # to_do

        # link of the video to be downloaded
        try:
            # object creation using YouTube
            # which was imported in the beginning
            yt = YouTube(link)
        except:
            print("Connection Error")  # to handle exception

        # filters out all the files with "mp4" extension

        # to set the name of the file

        # get the video with the extension and
        # resolution passed in the get() function
        d_video = yt.streams.get_highest_resolution()
        try:
            # downloading the video
            dc = d_video.download(SAVE_PATH)
        except:
            print("Some Error!")
        print('Task Completed!')
        url = os.path.basename(dc)
        my_dict = {
            'urls': url,
        }

    return render(request, 'index.html', context=my_dict)
