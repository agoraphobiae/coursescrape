"""
fscrapy.py

Because scrapy globally disallows scraping of .pdf files.
And because mechanize imo is more pythonic, requiring less
scaffolding etc.
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

start_urls = {
    "CS70fa13":"http://inst.eecs.berkeley.edu/~cs70/fa13/",
    "CS61Cfa13":"http://inst.eecs.berkeley.edu/~cs61c/",
    "CS61Afa13":"http://inst.eecs.berkeley.edu/~cs61a/fa13/"
}

fileext = ["pptx", "PPTX", "tex", "TEX", "pdf", "PDF"]
fileexts = "|".join(str(s) for s in fileext)
fileregex = "^.*\.(%s)$"%fileexts
fileregex = re.compile(fileregex)

urlregex = "^http://inst\\.eecs\\.berkeley\\.edu.*$"
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
            if link.url not in checkedUrls:
                if fileregex.match(link.url):
                    checkedUrls.append(link.url)
                    download(br, name, url, link.url)
                elif urlregex.match(link.url):
                    debug('recursing to', link.url)
                    recurseGoTo(validateURL(link.url))

    return recurseGoTo(url)

def validateURL(baseurl, linkurl):
    #debug('ORIGINAL URL:', baseurl+linkurl)
    # fix those pesky ../, ./ things
    url = urlparse(baseurl+linkurl)
    url = url.scheme + '://' + url.netloc + os.path.realpath(url.path)

    return url

def localPath(url):
    url = urlparse(url)
    url = SAVEFOLDER + os.path.realpath(url.path)
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
        localpath = localPath(url)
        ensure_dir(os.path.realpath(localpath))
        with open(localpath, 'w') as f:
            f.write(r.read())



def main():
    # lol global vars and python internals instead of OOP lol
    for name, url in start_urls.iteritems():
        checkCourseSite(name, url)

if __name__ == "__main__":
    main()