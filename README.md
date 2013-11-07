coursescrape
==============
A scraper to download course resources from course websites, originally made specifically for UC Berkeley's CS course websites.

Configure the values in ```start_urls``` and then run ```python2 fscrapy.py``` to download files into the save/ directory. Files will be downloaded preserving relative paths (i.e. ```http://url.edu/path/to/file.pdf``` will go to ```coursename/path/to/file.pdf```).

Made using mechanize.