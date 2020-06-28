import crochet
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapyspider import settings as sets
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
import database


class Scrape:
    crochet.setup()
    crawl_runner = CrawlerRunner()
    item = {}
    dict_of_spiders = {}

    def scrape(self, domain, dict_of_spiders):
        domains = domain
        self.dict_of_spiders = dict_of_spiders

        for domain in domains:
            try:
                self.scrape_with_crochet(domain).wait(timeout=5)
                yield self.item
            except crochet.TimeoutError:
                self.scrape_with_crochet(domain).cancel()
                raise

    @crochet.run_in_reactor
    def scrape_with_crochet(self, domain):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        crawler_settings = Settings()
        crawler_settings.setmodule(sets)
        self.crawl_runner.settings = crawler_settings
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)

        for i in self.dict_of_spiders:
            if i in domain:
                eventual = self.crawl_runner.crawl(self.dict_of_spiders[i], category=domain)
                return eventual

    def _crawler_result(self, item, response, spider):
        database.save(dict(item))
        self.item = dict(item)
