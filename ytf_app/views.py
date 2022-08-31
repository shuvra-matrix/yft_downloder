from hashlib import new
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
    return render(request, 'ydown.html', context=my_dict)

def ytdownload(request):
    if request.method == 'POST':
        quality_list =[]
        size_list = []
        link = request.POST.get('link')  
        try:
            yt = YouTube(link)
            title = yt.title
            length = yt.length
            thumb = yt.thumbnail_url
            
        except:
            print("Connection Error")  # to handle exception
        
        try:
            
            s1 = (yt.streams.get_by_resolution('360p').filesize)/1000000
            
            size_list.append(s1)
            quality_list.append('360p')
        except:
            pass
        try:
            s2 = (yt.streams.get_by_resolution('720p').filesize)/1000000
            size_list.append(s2)
            quality_list.append('720p')
        except:
            pass

        my_dict = {
            'qlist': quality_list,
            'llist': link,
            'color' : 'ytdown',
            'title' : title,
            'length' :length,
            'thumb' : thumb,
            'size' : size_list,
        }
        
        return render(request, 'ytdownload.html', context=my_dict)
    return redirect('/')

def yvdown(request):
    if request.method == 'POST':
        SAVE_PATH = "./media"
        dc = None
        title = request.POST.get('title')
        link = request.POST.get('link')      
        reg = request.POST.get('reg')
        print(reg)
        thumb = request.POST.get('thumb')
        try:
            yt = YouTube(link)
            link = yt.streams.filter(res=reg,progressive=True).first()
            print(link)
            dc = link.download(SAVE_PATH)
        except:
            print("Some Error!")

        print('Task Completed!')
        url = os.path.basename(dc)
        mydict = {
    
            'color' : 'ytdowns',
            'title' : title,
            'url' :url,
            'thumb' : thumb,
            'reg' :reg,
        }
        return render(request,'ytdownpage.html',context=mydict)
    return redirect('/')

