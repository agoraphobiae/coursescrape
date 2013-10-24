# Scrapy settings for insteecsscrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'insteecsscrape'

SPIDER_MODULES = ['insteecsscrape.spiders']
NEWSPIDER_MODULE = 'insteecsscrape.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'insteecsscrape (+http://www.yourdomain.com)'


ITEM_PIPELINES = {'insteecsscrape.pipelines.Scrape70Pipeline': 1}