#%%
import scrapy
class SongSpider(scrapy.Spider):
    name = "Kankra2"
    start_urls = [
        'https://www.allthelyrics.com/lyrics/doors'
    ]
    def parse(self, response):
#        for song in response.css('.content-text-inner'):
#            yield {
#                    'lyrics': song.css('.content-text-inner ::text').getall()
#                }
#            print(song)

        next_page = response.css('li ::attr(href)').getall()
        print(next_page)
        if next_page is not None or next_page.startswith('/lyrics'):
            for links in next_page:
                link_full='https://www.allthelyrics.com'+links
                next_page_response = response.urljoin(link_full)
                yield scrapy.Request(next_page_response, callback=self.parse)
                for song in response.css('.content-text-inner'):
                    yield {
                        'lyrics': song.css('.content-text-inner ::text').getall()
                        }

 #response.css('h1.page-title ::text').get()
 #scrapy crawl KanKra2 -o KanKra2.json