from django.shortcuts import render
from pytube import YouTube
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

        print("Downloading...")
        ys.download()
        print("Download completed!!")

    return render(request, 'index.html')
