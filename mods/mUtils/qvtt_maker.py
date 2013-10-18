from optparse import OptionParser
import urllib2
import json


SEG_STEP = 10


def optParser():
    optp = OptionParser()
    #settings
    optp.add_option('-u', '--url', help='url of the media file on Qiniu',
                    dest='url', default=None)
    optp.add_option('-o', '--output', help='output file name',
                    dest='output', default='sample.vtt')

    opts, args = optp.parse_args()
    return opts.url, opts.output


def getVideoInfo(url):
    req = urllib2.Request('%s?avinfo' % (url,))
    try:
        conn = urllib2.urlopen(req, timeout=15)
        data = conn.read()
        return json.loads(data)
    except Exception as e:
        print 'Error: %s' % (e,)
    return


def makeTrace(start, seg):
    return '%s --> %s' % (sec2str(start), sec2str(start + seg))


def makeThumbUrl(url, offset, width=120, height=90, imgFormat='jpg'):
    return '%s?vframe/%s/offset/%d/w/%d/h/%d' % (url, imgFormat, offset, width, height)


def sec2str(sec):
    minNum = int(sec) / 60
    secNum = int(sec) % 60
    return '%02d:%02d.000' % (minNum, secNum)


def makeSegmentation(start, duration, step=10):
    return range(start, start+duration, step)


def makeContent(url):
    videoInfo = getVideoInfo(url)
    if not videoInfo:
        print 'can not get video info'
        return

    start = int(float(videoInfo['format']['start_time']))
    duration = int(float(videoInfo['format']['duration']))

    seg = makeSegmentation(start, duration, SEG_STEP)

    contentList = []
    for offset in seg:
        line = '%s\n%s\n' % (makeTrace(offset, SEG_STEP), makeThumbUrl(url, offset))
        contentList.append(line)

    content = '\n'.join(contentList)
    return content


def makeFile(output, content):
    with open(output, 'w') as f:
        f.write(content)
    return


def main():
    url, output = optParser()
    if not url:
        print 'need an available url on Qiniu Cloud Storage'
        return

    content = makeContent(url)
    if output:
        makeFile(output, content)
    return


if __name__ == '__main__':
    main()