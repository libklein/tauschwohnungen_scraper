import scrapy
from scrapy.http import Response

def parse_offer(page):
    offer_details = page.xpath("//table[contains(@class, 'table-characteristics')]")[0]
    offer = {
        i.css(".t-title::text").get(): i.css(".t-content::text").get() for i in offer_details.xpath("tbody/tr")
    }

    # Get main offer stats
    offer.update(dict(zip(["kaltmiete", "wohnfläche", "zimmer"], page.xpath("//div[@class='col-12 col-md-6']//div[@class='row mb-3']//strong//text()").getall())))

    return { key.lower().strip(): value.replace("€","").replace("m²", "").lower().strip() for key, value in offer.items() }

def parse_gesuch(page):
    gesuch_details = page.xpath('//div[h4[text()="Gesuch"]]/div[contains(@class,"card")]//strong/text()')
    return {key: value.replace("€", "").strip() for key, value in zip(["stadt", "stadtteile", "kaltmiete", "wohnfläche", "zimmer"], gesuch_details.getall())}

class TauschwohnungSpider(scrapy.Spider):
    name = "Tauschwohnung"
    url = None

    def start_requests(self):
        if self.url is None:
            raise RuntimeError("Please set a search url! (-a url=\"https://tauschwohnung.com/search/result?...\")")
        yield scrapy.Request(self.url, callback=self.parse)

    def parse_offer(self, response: Response):
        offer = parse_offer(response)

        gesuch = parse_gesuch(response)

        # Get Beschreibung
        beschreibung = response.xpath("//div[h4[text()='Beschreibung']]/p//text()").get()

        url = response.url
        offer_id = response.url.rpartition("-")[-1]

        yield {
            'offer': offer,
            'gesuch': gesuch,
            'description': beschreibung,
            'url': url,
            'id': offer_id
        }

    def parse(self, response: Response):
        # Extract offers
        yield from response.follow_all(xpath='//a[@class="stretched-link"]', callback=self.parse_offer)
        # Navigate to other pages
        yield from response.follow_all(xpath='//li[@class="page-item"]/a[not(contains(@class,"page-link-icon"))]')
