berkeleyscrape
==============
A scraper to download course resources from UC Berkeley's course websites. Currently it downloads files from specified ```inst.eecs.berkeley.edu/~course/``` pages, which default to the CS70 and CS61C Fa13 pages. When finished it will recursively download all important course documents linked from a course page.

Run ```scrapy crawl insteecs``` to download files into the ```save/``` directory.

Made using Scrapy.