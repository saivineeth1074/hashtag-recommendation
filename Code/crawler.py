"""
    Program: crawler to scrape data from given domain (politics in this case)
"""


from scrapy.crawler import CrawlerProcess
import os, json, shutil, scrapy, urlparse, logging

start_url = "http://www.moneycontrol.com/news/politics"

# the subclass of the Spider class of scrapy
class IRSpider(scrapy.Spider) :
    # initialize docID to be 0
    docID = 0
    # name of the crawler
    name = "IRCrawler"

    # allowed domains in order to not deviate from the start site
    allowed_domains = ["moneycontrol.com"]

    # start URL being in the sports section of the news domain
    start_urls = [start_url]

    # control what repr() returns for this class
    def __repr__(self) :
        return ""

    def extract_and_write(self, response, raw_content, tags) :

        # get the URL from the response
        url = response.url

        # get the title of the webpage
        title = response.css('title::text').extract()[0].encode('utf-8')

        # get the meta_keywords from the page
        #meta_keywords = response.xpath("//meta[@name='keywords']/@content")[0].extract().encode('utf-8')
        #date = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()[0].encode('utf-8')

        # get the content, that is, the ARTICLE text from the HTML file
        
        content = u''.join(raw_content).encode('utf-8').strip()
        if(content.startswith("[")):
            content = content[1:-1].replace("\r\n", " ")
            js = json.loads(content)
        
            if(len(content.split()) > 100):
                self.docID += 1
                f = open("./crawled-data/%d.txt" % self.docID, "w")
                f.write("URL: %s\nDATE: %s\nSECTION: %s\nTITLE: %s\nDESC: %s\nCONTENT: %s\n" 
                    % (url, js["datePublished"], js["articleSection"], js["headline"], js["description"], js["articleBody"]))
                f.write("TAGS:")
                for i in range(len((tags))):
                    if(not(i == (len(tags) - 1))):
                        tag = " ".join([word[:1].upper() + word[1:] for word in tags[i].split(" ")])
                        f.write(" " + tag + ",")
                    else:
                        tag = " ".join([word[:1].upper() + word[1:] for word in tags[i].split(" ")])
                        f.write(" " + tag + "\n")
                f.close()

    def parse(self, response) :
        # get the text of the main ARTICLE from the HTML page

        if (response.url.endswith('.html') or response.url.endswith('.htm')):
            content = response.xpath('//script[@type="application/ld+json"]/text()')[-1].extract()
            #contentTemp = response.xpath('//div[@id="article-main"]//p/text()').extract()

            tags = response.xpath('//div[@class="clearfix"]//h3[@class="tag_txt"]//a/text()').extract()
            self.extract_and_write(response, content, tags)

        # extract all links from page
        link_selector = scrapy.Selector(response)
        all_links = link_selector.xpath('*//a/@href').extract()

        # iterate over links
        for link in all_links :
            url = urlparse.urljoin(response.url, link)
            if(start_url in str(url)):
                yield scrapy.http.Request(url = url, callback = self.parse)

# create the crawler process to create a twisted reactor for scrapy
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

# create a new directory to store the *.txt files for the pages
if not os.path.exists("./crawled-data") :
    os.makedirs("./crawled-data")
else :
    shutil.rmtree("./crawled-data/")
    os.makedirs("./crawled-data")

process.crawl(IRSpider)

# the script blocks here until the crawling process is finished
process.start()