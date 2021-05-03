"""
scrapy runspider -L WARNING song_scrape_Paul.py
"""

#%%
import scrapy
from scrapy.http import Request
import re


class SongSpider(scrapy.Spider):
    name = "Kankra2000"
    allowed_domains = ["www.allthelyrics.com"]
    start_urls = ["https://www.allthelyrics.com/de/lyrics/rolling_stones"]

    def parse(self, response):
 #       artist_links = response.xpath("//div[contains(@class, 'glossary-search-result')]//a/@href").getall()

        # next_page = response.css("li ::attr(href)").getall()
        songlinks = response.xpath(
            "//li[contains(@class, 'lyrics-list-item')]/a/@href"
        ).getall()
        # print(next_page)
        for sl in songlinks:
            print(Request(response.urljoin(sl))) #Is print only for the command?
            yield Request(response.urljoin(sl)) #What is yield doing?

        song_text = response.xpath(
            "//div[contains(@class, 'content-text')]//p//text()"
        ).getall()

        clean_text = "".join(song_text)
        clean_text = re.sub("\n", " ", clean_text)

        item = {"lyrics": clean_text}
        yield item
#        with open('lyrics.csv', 'w') as csv_file:  
#           writer = csv.writer(csv_file)
#           for key, value in item.items():
#         writer.writerow([key, value])

        # if next_page is not None or next_page.startswith('/lyrics'):
        #     for links in next_page:
        #         link_full='https://www.allthelyrics.com'+links
        #         next_page_response = response.urljoin(link_full)
        #         yield scrapy.Request(next_page_response, callback=self.parse)
        #         for song in response.css('.content-text-inner'):
        #             yield {
        #                 'lyrics': song.css('.content-text-inner ::text').getall()
        #                 }


# response.css('h1.page-title ::text').get()
# scrapy crawl Kankra2000 -o beatles.csv
