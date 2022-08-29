from django.shortcuts import render
from pytube import YouTube
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.


def index(request):
    if request.method == 'POST':

        link = request.POST.get('link')
        yt = YouTube(link)
        print("Title: ", yt.title)

        print("Number of views: ", yt.views)
        print("Length of video: ", yt.length)
        print("Rating of video: ", yt.rating)
        # Getting the highest resolution possible
        ys = yt.streams.get_highest_resolution()
        print(ys)

        print("Downloading...")
        dc = ys.download()
        file_name = os.path.basename(dc)
        print(file_name)

        file_path = os.getcwd(dc)
        print(file_path)
        # print("Download completed!!")
        # file = FileSystemStorage()
        # upload_file = file.save(file_name, dc)

    return render(request, 'index.html')
