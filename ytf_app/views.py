from django.shortcuts import render, redirect
from pytube import YouTube
import os
import glob
from random import randint


def index(request):
    dir = 'media'
    urls = None
    if request.session.has_key('url'):
        file_name = request.session['url']
        urls = f'media\\{file_name}'
        del request.session['url']
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        if f == urls:
            continue
        else:
            os.remove(f)

    my_dict = {
        'color': 'bodyclass',
    }
    return render(request, 'index.html', context=my_dict)


def ydown(request):
    my_dict = {
        'urls': None,
        'color': 'ytclass',

    }
    return render(request, 'ydown.html', context=my_dict)


def ytdownload(request):
    if request.method == 'POST':
        quality_list = []
        size_list = []
        link = request.POST.get('link')
        if 'youtu' not in link:
            return redirect('/ytdown')
        try:
            yt = YouTube(link)
            title = yt.title
            length = yt.length
            thumb = yt.thumbnail_url

        except:
            return redirect('/ytdown')

        try:

            s1 = round((yt.streams.get_by_resolution('360p').filesize)/1000000)

            size_list.append(s1)
            quality_list.append('360p')
        except:
            pass
        try:
            s2 = round((yt.streams.get_by_resolution('720p').filesize)/1000000)
            size_list.append(s2)
            quality_list.append('720p')
        except:
            pass

        my_dict = {
            'qlist': quality_list,
            'llist': link,
            'color': 'ytdown',
            'title': title,
            'length': length,
            'thumb': thumb,
            'size': size_list,
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

        thumb = request.POST.get('thumb')
        try:
            yt = YouTube(link)
            link = yt.streams.filter(res=reg, progressive=True).first()
            rand = randint(1, 8909)
            filename = f'video{rand}.mp4'
            dc = link.download(SAVE_PATH, filename=filename)
        except:
            return redirect('/ytdown')

        url = os.path.basename(dc)
        request.session['url'] = url
        mydict = {

            'color': 'ytdowns',
            'title': title,
            'url': url,
            'thumb': thumb,
            'reg': reg,
        }
        return render(request, 'ytdownpage.html', context=mydict)
    return redirect('/')


def ytmusic(request):
    my_dict = {
        'color': 'yt_body',
    }
    return render(request, 'ytmusic.html', context=my_dict)


def ytmsearch(request):
    if request.method == 'POST':
        SAVE_PATH = "./media"
        dc = None
        link = request.POST.get('link')
        if 'youtu' not in link:
            return redirect('/ytdown')
        try:
            yt = YouTube(link)
            title = yt.title
            length = yt.length
            thumb = yt.thumbnail_url
            music_list = yt.streams.filter(
                only_audio=True, abr='128kbps').first()
            music_size = round((yt.streams.filter(
                only_audio=True, abr='128kbps').first().filesize)/1000000)
            rand = randint(1, 8909)
            filename = f'audio{rand}.mp3'
            dc = music_list.download(SAVE_PATH, filename=filename)
            url = os.path.basename(dc)
            request.session['url'] = url

            mydict = {
                'color': 'ytmdowns',
                'title': title,
                'url': url,
                'thumb': thumb,
            }
        except:
            return redirect('/ytmusic')

        return render(request, 'ytmdownload.html', context=mydict)
    return redirect('/ytmusic')
