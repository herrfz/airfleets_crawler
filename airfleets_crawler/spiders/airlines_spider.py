import string
import scrapy

class AirlinesSpider(scrapy.Spider):
    name = 'airlines'
    start_urls = ['http://www.airfleets.net/recherche/list-airline-{}_0.htm'.format(x) for x in string.ascii_lowercase]

    def parse(self, response):
        names = response.selector.xpath('/html/body/table[4]//table[1]//tr[@class="trtab"]//td[1]/a[@class="lien"]/text()').extract()
        countries = response.selector.xpath('/html/body/table[4]//table[1]//tr[@class="trtab"]//td[2]/text()').extract()
        status = response.selector.xpath('/html/body/table[4]//table[1]//tr[@class="trtab"]//td[3]/a[@class="lien"]/text()').extract()

        countries = [x.strip() for x in countries]
        airlines = [{'name':x, 'country':y} for x, y in zip(names, countries)]

        idx = -1
        for s in status:
            if s in [' ', ' inactive']:
                idx += 1
                airlines[idx]['active'] = True if s == ' ' else False
                curstatus = None
            elif s == 'supported aircraft':
                curstatus = s
            else:
                if curstatus == 'supported aircraft':
                    airlines[idx]['merged into'] = s
                else:
                    airlines[idx]['fleet'] = s.strip().split()[0]

        for airline in airlines:
            yield airline

        next_page = response.selector.xpath("/html/body//a[@class='page' and text() = 'Next page ']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
