#%%
import scrapy

class SongSpider(scrapy.Spider):
    name = "Kankra2"

    start_urls = [
        'https://www.allthelyrics.com/lyrics/doors/a_feast_of_friends-lyrics-827905.html'
    ]

    def parse(self, response):
        yield {
                'lyrics': response.xpath('//*[@id="node-1522751"]/div/div[2]/div[1]/div[2]/*').getall()
                }
        next_page = response.xpath('//*[@id="lyricslist-left"]/ul[1]/li[1]/a/@href').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

 #response.css('h1.page-title ::text').get()

 #scrapy crawl Kankra2 -o KanKra2.json