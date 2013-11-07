"""
coursescrape.py

Because scrapy globally disallows scraping of .pdf files.
And because mechanize imo is more pythonic, requiring less
scaffolding etc.

TODO:
multithread/queue downloads instead of inline
dont go to files not matching fileregex
"""

from __future__ import print_function

import mechanize
import re
import os
from urlparse import urlparse

DEBUG = True
# needs __future__ print
def debug(*args):
    if DEBUG:
        print(*args)
RECURSE = False

start_urls = {
    "CS70fa13":"http://inst.eecs.berkeley.edu/~cs70/fa13/",
    "CS61Cfa13":"http://inst.eecs.berkeley.edu/~cs61c/",
    "CS61Afa13":"http://inst.eecs.berkeley.edu/~cs61a/fa13/"
    #"webdesignworkshop":"http://www.thewebdesignworkshop.co/"
}

fileext = ["pptx", "PPTX", "tex", "TEX", "pdf", "PDF", 'zip', "ZIP"]
fileexts = "|".join(str(s) for s in fileext)
fileregex = "^.*\.(%s)$"%fileexts
fileregex = re.compile(fileregex)

urlregex = "^http://inst\\.eecs\\.berkeley\\.edu.*$"
#urlregex = "^http://www\\.thewebdesignworkshop\\.co.*$"
urlregex = re.compile(urlregex)

SAVEFOLDER = "save"

def checkCourseSite(name, url):
    br = mechanize.Browser()
    br.addheaders = [('User-Agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36')]

    checkedUrls = []

    def recurseGoTo(url):
        checkedUrls.append(url)
        debug('checking', url)

        r = br.open(url)
        url = r.geturl() #~cs61c to ~cs61c/fa13 
        html = r.read()

        for link in br.links():
            #debug('link:', link.url)
            dest = validateURL(url, link.url)
            if dest and dest not in checkedUrls:
                if fileregex.match(dest):
                    checkedUrls.append(dest)
                    download(br, name, url, link.url)
                elif urlregex.match(dest):
                    if RECURSE:
                        debug('recursing to', link.url)
                        recurseGoTo(dest)

    return recurseGoTo(url)

def validateURL(baseurl, linkurl):
    """Figures out where to go based on the link url and the current url

    normal relative link
    >>> validateURL('http://inst.eecs.berkeley.edu/~cs61c/fa13/', 'disc/10/Disc10.pdf')
    'http://inst.eecs.berkeley.edu/~cs61c/fa13/disc/10/Disc10.pdf'
    >>> validateURL('http://www.thewebdesignworkshop.co/index.html', 'lectures.html')
    'http://www.thewebdesignworkshop.co/lectures.html'

    links that link to themselves
    >>> validateURL('http://www.thewebdesignworkshop.co/index.html', 'index.html')
    'http://www.thewebdesignworkshop.co/index.html'

    links with ../ and ./
    >>> validateURL('http://inst.eecs.berkeley.edu/~cs61c/fa13/', '../resources/gdb5-refcard.pdf')
    'http://inst.eecs.berkeley.edu/~cs61c/resources/gdb5-refcard.pdf'
    >>> validateURL('http://inst.eecs.berkeley.edu/~cs61c/fa13/', './lec/01LecF13Intro.pptx')
    'http://inst.eecs.berkeley.edu/~cs61c/fa13/lec/01LecF13Intro.pptx'

    ignore mailto
    >>> validateURL('https://site.com/path/to/someplace.php', 'mailto:webmaster@deadbeef.org')
    None
    """
    #debug('ORIGINAL URL:', baseurl+linkurl)
    # out links will not be relative, check
    if urlparse(linkurl).scheme in ['http','https']:
        return linkurl
    elif urlparse(linkurl).scheme == 'mailto':
        return None
    # handle relative linking
    baseurl = baseurl[:baseurl.rfind('/')+1]
    url = urlparse(baseurl+linkurl)
    # realpath fixes those pesky ../, ./ things
    url = url.scheme + '://' + url.netloc + os.path.realpath(url.path)

    return url

def localPath(name, url):
    url = urlparse(url)
    url = SAVEFOLDER + '/' + name + os.path.realpath(url.path)
    return url

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        debug(d, 'did not exist, creating directory...')
        os.makedirs(d)

def download(br, name, baseurl, linkurl):
    url = validateURL(baseurl, linkurl)
    debug('downloading', url)

    try:
        r = br.open(url)
    except mechanize.HTTPError as e:
        if e.code == 403:
            print("Encountered 403 attempting to access", url)
        elif e.code == 404:
            print("Encountered 404 attempting to access", url)
        else:
            raise e
    else:
        localpath = localPath(name, url)
        ensure_dir(os.path.realpath(localpath))
        with open(localpath, 'w') as f:
            f.write(r.read())



def main():
    # lol global vars and python internals instead of OOP lol
    for name, url in start_urls.iteritems():
        checkCourseSite(name, url)

if __name__ == "__main__":
    main()