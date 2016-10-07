from functools import partial
import scrapy


class BiteBt(scrapy.Spider):
    name = "bitebt"

    start_urls = [
        #"http://www.bitebt.com/forum.php",
        "http://www.bitebt.com/forum-43-1.html",
    ]

    def parse(self, response):
        """
        只要第一页，后面的页不要了
        """
        for href in set(response.css('a::attr(href)').re(r'thread-\d+-1-1\.html')):
            url = response.urljoin(href)
            yield {
                'type': 'thread',
                'url': url,
            }
            yield scrapy.Request(url, callback=partial(self.parse_thread, url))

    def parse_thread(self, thread_url, response):
        yield {
            'type': 'movie',
            'thread_url': thread_url,
            'subject': response.css('#thread_subject::text').extract_first().strip(),
            'bt': response.urljoin(response.css('a[href*="mod=attachment"]::attr(href)').extract_first()),
            'imgs': response.css('#postlist div:first-of-type img[lazyloadthumb]::attr(file)').extract(),
            'douban': response.css('a[href*="movie.douban.com"]::attr(href)').extract_first(),
        }
        # TODO: item pipeline & media pipeline
        # https://doc.scrapy.org/en/1.2/topics/item-pipeline.html
        # https://doc.scrapy.org/en/1.2/topics/media-pipeline.html
