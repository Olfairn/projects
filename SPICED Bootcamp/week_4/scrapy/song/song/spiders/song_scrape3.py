#%%
import scrapy
class SongSpider(scrapy.Spider):
    name = "Kankra3"
    start_urls = [
        'https://www.allthelyrics.com/lyrics/doors'
    ]
    def parse(self, response):
        for song in response.css('.content-text-inner'):
            yield {
                    'lyrics': song.css('.content-text-inner ::text').getall()
                }
            print(song)

        next_page = ['https://www.allthelyrics.com/lyrics/doors/alabama_song_whisky_bar-lyrics-26366.html']
        print(next_page)
        if next_page is not None:
            next_page_response = response.urljoin(next_page)
            yield scrapy.Request(next_page_response, callback=self.parse)
            print(next_page_response)
 #response.css('h1.page-title ::text').get()
 #scrapy crawl KanKra2 -o KanKra2.json