

# sample url
# http://s3.amazonaws.com/stanford_videos/cs229/subtitles/09.1-NeuralNetworksLearning-CostFunction-subtitles.xml



def readdata(filename="data.txt"):
    f = open(filename)
    files = []
    try:
        for line in f:
            files.append(line)
    finally:
        f.close
    return files

def getsubtitlename(mp4_name):
    return mp4_name.rsplit(".", 1)[0] + "-subtitles.xml"

urlbase_subtitles = 'http://s3.amazonaws.com/stanford_videos/cs229/subtitles/'

def getsubtitleurl(subtitle_name):
    return urlbase_subtitles + subtitle_name

def writesubtitlefile(name, contents):
    f = open(name, 'w')
    f.write(contents)
    f.close()

import urllib2, os

def wget():

    path="output/"
    mp4s = readdata("data.txt")
    
    for mp4 in mp4s:
        
        name = getsubtitlename(mp4)
        url = getsubtitleurl(name)
        filename = path + name

        if os.path.exists(filename):
            continue

        try:
            c = urllib2.urlopen(url)
            contents = c.read()

            writesubtitlefile(filename, contents)

        except:
            print "ERROR: " + url
        







