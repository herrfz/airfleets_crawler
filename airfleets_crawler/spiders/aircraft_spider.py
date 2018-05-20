import scrapy
from bs4 import BeautifulSoup

class AircraftSpider(scrapy.Spider):
    name = 'aircraft'
    # scrapy shell http://www.airfleets.net/recherche/supported-plane.htm
    # response.selector.xpath('/html/body/table[4]//table//td[@class = "tdtexten"]//a/@href').extract()
    start_urls = ['http://www.airfleets.net/recherche/' + x for x in
        ['../listing/a300-1.htm',
         '../listing/a310-1.htm',
         '../listing/a318-1.htm',
         '../listing/a319-1.htm',
         '../listing/a320-1.htm',
         '../listing/a321-1.htm',
         '../listing/a330-1.htm',
         '../listing/a340-1.htm',
         '../listing/a350-1.htm',
         '../listing/a380-1.htm',
         '../listing/atr-1.htm',
         '../listing/bae146-1.htm',
         '../listing/beh-1.htm',
         '../listing/b717-1.htm',
         '../listing/b737-1.htm',
         '../listing/b737ng-1.htm',
         '../listing/b747-1.htm',
         '../listing/b757-1.htm',
         '../listing/b767-1.htm',
         '../listing/b777-1.htm',
         '../listing/b787-1.htm',
         '../listing/csr-1.htm',
         '../listing/crj-1.htm',
         '../listing/arj21-1.htm',
         '../listing/c919-1.htm',
         '../listing/ssc-1.htm',
         '../listing/dh8-1.htm',
         '../listing/e120-1.htm',
         '../listing/e145-1.htm',
         '../listing/e170-1.htm',
         '../listing/e190-1.htm',
         '../listing/f50-1.htm',
         '../listing/f100-1.htm',
         '../listing/il96-1.htm',
         '../listing/l10-1.htm',
         '../listing/dc10-1.htm',
         '../listing/md11-1.htm',
         '../listing/md80-1.htm',
         '../listing/s20-1.htm',
         '../listing/sf3-1.htm',
         '../listing/ssj-1.htm']]

    def parse(self, response):
        acline = response.selector.xpath('/html/body/table[4]//h2/text()').extract()[0].split(' : ')[0]
        columns = [x for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "textenu"]//td/text()').extract() if x != '\xa0']

        msn = response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[1]/a/text()').extract()

        # q & d
        if 'LN ' in columns:
            ln = response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[2]/a/text()').extract()
            actype = [x.strip() for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[3]/text()').extract()]
            # more q & d due to empty airline in data
            _temp_airline = response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[4]/a').extract()
            airline = []
            for aa in _temp_airline:
                soup = BeautifulSoup(aa, 'lxml')
                for a in soup.find_all('a'):
                    if a.string is None:
                        airline.append('')
                    else:
                        airline.append(a.string)

            # missing data is OK here because it's not an <a> tag ...
            firstflight = [x.strip() for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[5]/text()').extract()]

            # more q & d due to empty registration in data
            _temp_reg = response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[6]/a').extract()
            registration = []
            for aa in _temp_reg:
                soup = BeautifulSoup(aa, 'lxml')
                for a in soup.find_all('a'):
                    if a.string is None:
                        registration.append('')
                    else:
                        registration.append(a.string)

            status = [x.strip() for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[7]/text()').extract()]

            airplanes = [{'msn':x, 'ln':t, 'actype':y, 'airline':z, 'firstflight':u, 'registration':v, 'status':w}
                            for x, t, y, z, u, v, w in zip(msn, ln, actype, airline, firstflight, registration, status)]
        else:
            actype = [x.strip() for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[2]/text()').extract()]
            # more q & d due to empty airline in data
            _temp_airline = response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[3]/a').extract()
            airline = []
            for aa in _temp_airline:
                soup = BeautifulSoup(aa, 'lxml')
                for a in soup.find_all('a'):
                    if a.string is None:
                        airline.append('')
                    else:
                        airline.append(a.string)

            # missing data is OK here because it's not an <a> tag ...
            firstflight = [x.strip() for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[4]/text()').extract()]

            # more q & d due to empty registration in data
            _temp_reg = response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[5]/a').extract()
            registration = []
            for aa in _temp_reg:
                soup = BeautifulSoup(aa, 'lxml')
                for a in soup.find_all('a'):
                    if a.string is None:
                        registration.append('')
                    else:
                        registration.append(a.string)

            status = [x.strip() for x in response.selector.xpath('/html/body/table[4]//table//tr[@class = "trtab"]//td[6]/text()').extract()]

            airplanes = [{'msn':x, 'actype':y, 'airline':z, 'firstflight':u, 'registration':v, 'status':w}
                            for x, y, z, u, v, w in zip(msn, actype, airline, firstflight, registration, status)]

        for airplane in airplanes:
            airplane['acline'] = acline
            yield airplane

        next_page = response.selector.xpath("/html/body//a[@class='page' and text() = 'Next page ']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
