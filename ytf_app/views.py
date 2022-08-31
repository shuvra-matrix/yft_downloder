from django.shortcuts import render,redirect
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

def ytdownload(request):
    if request.method == 'POST':
        quality_list = []
        link_list = []
        size_list = []
        link = request.POST.get('link')
        SAVE_PATH = "./media"  
        try:
            yt = YouTube(link)
            title = yt.title
            length = yt.length
            thumb = yt.thumbnail_url
            
        except:
            print("Connection Error")  # to handle exception
        
        try:
            q360 = yt.streams.filter(res='360p')
            s1 = yt.streams.get_by_resolution('360p').filesize
            quality_list.append('360p')
            link_list.append(q360)
            size_list.append(s1)   
        except:
            pass
        try:
            q480 = yt.streams.filter(res='480p')
            quality_list.append('480p')
            link_list.append(q480)
            s2 = yt.streams.get_by_resolution('480p').filesize
            size_list.append(s2)
        except:
            pass
        try:
            q720 = yt.streams.filter(res='720p')
            quality_list.append('720p')
            link_list.append(q720)
            s3 = yt.streams.get_by_resolution('720p').filesize
            size_list.append(s3)
        except:
            pass
        try:
            q1080 = yt.streams.filter(res='1080p')
            quality_list.append('1080p')
            link_list.append(q1080)
            s4 = yt.streams.get_by_resolution('1080p').filesize
            size_list.append(s4)
        except:
            pass
    
        # print(d_video[1])
        # try:
        #     dc = d_video[1].download(SAVE_PATH)
        # except:
        #     print("Some Error!")

        # print('Task Completed!')
        # url = os.path.basename(dc)
       
        print(size_list)
        ranges = range(len(quality_list))
        print(ranges)
        my_dict = {
            'qlist': quality_list,
            'llist': link_list,
            'color' : 'ytdown',
            'title' : title,
            'length' :length,
            'thumb' : thumb,
            'size' : size_list,
            'ranges' : [1,2,3],
        }

        return render(request, 'ytdownload.html', context=my_dict)
    return redirect('/')
