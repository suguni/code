# -*- coding: utf-8 -*-

import xml.dom.minidom
import os, os.path

def gethead(title, source):
    head = """<HEAD>
    <TITLE>%s</TITLE>
    <SAMIParam>
      Media {%s}
      Metrics {time:ms;}
      Spec {MSFT:1.0;}
    </SAMIParam>
    <STYLE TYPE="text/css">
    <!--
      P { font-family: Arial; font-weight: normal; color: white; background-color: black; text-align: center; }
      #Source {color: red; background-color: blue; font-family: Courier; font-size: 12pt; font-weight: normal; text-align: left; }
      .ENUSCC { name: English; lang: en-US ; SAMIType: CC ; }
    -->
    </STYLE>
  </HEAD>"""

    return head % (title, source)

def gettitle(filename):
    n = os.path.basename(filename)
    if n == '': return ''

    sn = os.path.splitext(n)
    if sn[1] == '': return ''

    i = sn[0].rfind('-subtitles')
    return sn[0][0:i]

def getbody(syncs):
    body = '<BODY>\n'
    body += '\n'.join(syncs)
    body += '\n</BODY>'
    return body
    
def hms2ms(hhmmss):
    ps = hhmmss.split(":")
    if len(ps) != 3: return None
    
    try:
        h = int(ps[0])
        m = int(ps[1])
        ms = int(float(ps[2]) * 1000)
        return h * 60 * 60 * 1000 + m * 60 * 1000 + ms
    except ValueError:
        return None

def gettext(elm):

    text = ''
    t = elm.firstChild

    while t:
        if t.nodeType == t.TEXT_NODE:
            text += t.data
        t = t.nextSibling

    return text.strip()

    
# input sample p
# <p begin="00:00:17.39" dur="00:00:0.95">
# Every time you use a web</p>
#
# output sample sync
# <SYNC Start=1000>
#  <P Class=ENUSCC>SAMI 1000 text</P>
# </SYNC>
# if need blank
# <SYNC Start=500>
#  <P>&nbsp;</P>
# <SYNC>
# <SYNC Start=1000>
#  <P Class=ENUSCC>SAMI 1000 text</P>
# </SYNC>

# 닫는 태그 넣으면 안됨.
def get_blank_sync(start):
    return '<SYNC Start=%d><P>\n&nbsp;' % start # </P><SYNC>

def get_sync(start, content):
    return '<SYNC Start=%d><P Class=ENUSCC>\n%s' % (start, content) # </P></SYNC>

def is_my_p(p):
    return p.nodeType == p.ELEMENT_NODE and p.tagName == 'p' and p.hasAttribute('begin') and p.hasAttribute('dur')

def get_syncs(div):
    
    p = div.firstChild
    if p == None: return None

    # search first p node
    while not is_my_p(p):
        p = p.nextSibling
        if p == None: return None

    count = 0
    prevp = None
    prev_end = -1

    syncs = []

    while p != None:
        
        if not is_my_p(p):
            p = p.nextSibling
            continue

        begin = hms2ms(p.getAttribute('begin'))
        dur = hms2ms(p.getAttribute('dur'))
        text = gettext(p)

        if begin == None or dur == None or text == None:
            print "Error %dth p element" % count
            p = p.nextSibling
            continue

        if prev_end != -1 and (prev_end + 100) < begin:
            syncs.append(get_blank_sync(prev_end))

        o = get_sync(begin, text)
        syncs.append(o) #get_sync(begin, text))

        prevp = p
        prev_end = begin + dur
        p = p.nextSibling

    return syncs

def writefile(name, contents):
    f = open(name, 'w')
    f.write(contents)
    f.close()


def main(filename):
    dom = xml.dom.minidom.parse(filename)
    syncs = get_syncs(dom.getElementsByTagName('div')[0])

    title = gettitle(filename)

    head = gethead(title, title+'.mp4')
    body = getbody(syncs)

    sami = '<SAMI>\n' + head + '\n' + body + '\n</SAMI>'

    output = os.path.dirname(filename) + '/' + title + '.smi'
    writefile(output, sami)

def test():
    filenames = os.listdir('output')
    for f in filenames:
        if f.find('.xml') != -1:
            main('output/' + f)

