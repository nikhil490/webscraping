import scrapy
from scrapy.loader import ItemLoader
from flaskr.scrapyspider.items import Article, ConferencePaper
from scrapy.loader.processors import Join


class WileyDoi(scrapy.Spider):
    name = 'wiley'

    def __init__(self, category='', **kwargs):
        self.start_urls = [category]
        super().__init__(**kwargs)

    def parse(self, response):
        type_of_article = response.xpath("//meta[@property='og:type']/@content").extract()[0]
        if type_of_article == 'Article':
            details = response
            loader = ItemLoader(item=Article(), selector=details)
            loader.default_output_processor = Join()
            loader.add_xpath('title', "//meta[@name='citation_title']/@content")
            loader.add_xpath('author', "//meta[@name='citation_author']/@content")
            loader.add_xpath('author', "//*[@id='a1_Ctrl']/span/text()")
            loader.add_xpath('journal', "//meta[@name='citation_journal_title']/@content")
            loader.add_xpath('publisher', "//meta[@name='citation_publisher']/@content")
            loader.add_xpath('year', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('abstract', "normalize-space(//meta[@property='og:description']/@content)")
            loader.add_xpath('doi', "//meta[@name='citation_doi']/@content")
            loader.add_xpath('timestamp', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('url', "//meta[@property='og:url']/@content")
            loader.add_xpath('ENTRYTYPE', "//meta[@property='og:type']/@content")
            loader.add_value('ID', load_id(loader))
        else:
            details = response
            loader = ItemLoader(item=ConferencePaper(), selector=details)
            loader.default_output_processor = Join()
            loader.add_xpath('title', "//meta[@name='citation_title']/@content")
            loader.add_xpath('booktitle', "//meta[@name='citation_book_title']/@content")
            loader.add_xpath('author', "//meta[@name='citation_author']/@content")
            loader.add_xpath('author', "//*[@id='a1_Ctrl']/span/text()")
            loader.add_xpath('publisher', "//meta[@name='citation_publisher']/@content")
            loader.add_xpath('year', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('abstract', "normalize-space(//meta[@property='og:description']/@content)")
            loader.add_xpath('doi', "//meta[@name='citation_doi']/@content")
            loader.add_xpath('timestamp', "//meta[@name='citation_online_date']/@content")
            loader.add_xpath('url', "//meta[@property='og:url']/@content")
            loader.add_xpath('ENTRYTYPE', "//meta[@property='og:type']/@content")
            loader.add_value('ID', load_id(loader))
            print(loader.load_item())
        yield loader.load_item()


def load_id(loader):
    author = loader.get_output_value('author').split(' ')[0]
    year = loader.get_output_value('year')
    return author + str(year)
