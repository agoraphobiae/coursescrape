# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import log

from urlparse import urlparse
import os

SAVELOC = "save/"

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

class Scrape70Pipeline(object):
    def process_item(self, item, spider):
        path = item['url']
        path = urlparse(path)
        path = os.path.basename(path.path)
        path = SAVELOC + path

        ensure_dir(path)

        with open(path, "wb") as f:
            f.write(item['doc'])

        # release file from mem
        del item['doc']
        item['path'] = path

        return item
