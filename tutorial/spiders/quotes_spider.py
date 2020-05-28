'''

ref link:
    https://docs.scrapy.org/en/latest/intro/tutorial.html

cmd list:
    scrapy crawl quotes
    scrapy shell 'https://www.esl-lab.com/easy/homestay/'
    response.css('source')[0].attrib['src']
    response.css('h2.sub-head::text')[0].get()
    tar -zcvf mp3.tar.gz mp3

In easy part, below two not having valid mp3 files:
- Phone_Message
- Physical_Therapy

'''

import scrapy
import urllib

ERROR_URLS = "error_urls.txt"
MP3_URLS = "mp3_urls.txt"
FAIL_MP3_URLS = "fail_mp3_urls.txt"

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        for fname in [ERROR_URLS, MP3_URLS, FAIL_MP3_URLS]:
            with open(fname, 'w') as f:
                f.write("")
        urls = [
            # 'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
            # 'https://www.esl-lab.com//intermediate/weekly-activities/',
            'https://www.esl-lab.com/intermediate/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        sel_li = response.css('div.el-content.uk-panel.uk-margin-top a')
        for sel in sel_li:
            url = sel.attrib['href']
            self.log("%s" % url)
            yield scrapy.Request(url=url, callback=self.parse_mp3)

    def parse_mp3(self, response):
        sels = response.css('source')
        title = response.css('h2.sub-head::text')[0].get().replace(' ', '_').replace("\"", "")
        if (len(sels) == 0):
            with open(ERROR_URLS, 'a+') as f:
                f.write(title + ":" + response.url + "\n")
            self.log("%s doesn't have valid mp3!" % response.url)
            return
        mp3_url = sels[0].attrib['src']
        self.log("%s : %s" %(title, mp3_url))
        with open(MP3_URLS, 'a+') as f:
            f.write(mp3_url + "\n")

        req = urllib.request.Request(mp3_url)
        try:
            # urllib.request.urlopen(req)
            urllib.request.urlretrieve(mp3_url, 'mp3/%s.mp3' % title)
        except urllib.error.URLError as e:
            with open(FAIL_MP3_URLS, 'a+') as f:
                f.write(title + ":" + mp3_url + "\n")
            self.log("%s doesn't have valid mp3!" % mp3_url)