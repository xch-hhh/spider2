
import re
from core.exception import ParseException, ListException
from core.items import BiddingItem
from core.utils.pdf import downloadAndParsePdf
from core.utils.time import get_formatting_date
from core.BaseSpider import BaseSpider


#http://www.myjfjt.com/
#绵阳交通发展集团有限责任公司

class _7514Spider(BaseSpider):
    name = "7514"
    params_list = [
        {"url": "http://www.myjfjt.com/channels/37_{}.html", "section": "招标公告"},

        {"url": "http://www.myjfjt.com/channels/38_{}.html", "section": "中标公示"},
    ]
    params_list2 = [
    {"url": "http://www.myjfjt.com/channels/37.html", "section": "招租公告"},
    {"url": "http://www.myjfjt.com/channels/38.html", "section": "中标公示"},
    ]
    maxRange = 2
    def start_requests(self, page=2):
        for params in self.params_list2:
            params['page'] = 1
            yield self.get(url=params['url'], callback=self.query_list, meta={"params": params})
        for params in self.params_list:
            params['page'] = page
            # print(1)
            yield from self.getListData(params)
    # def start_requests2(self,page=1):
    # def start_requests2(self,page = 1):
    #     for params in self.sigle_list:
    #        for i in self.sigle_list:
    #            params['page'] = page
    #            yield  self.get(url=params['url'], callback=self.query_list, meta={"params": params})

    def getListData(self, params):

        new_url = params['url'].format(params['page'])
        # print(444444,new_url)

        yield self.get(url=new_url, callback=self.query_list, meta={"params": params})

    def query_list(self, response):
        params = response.meta.get('params')
        page = params['page']
        self.debug(f"spider crawl {response.url} section {params['section']} page {page} total {self.maxRange}")
        item_list = response.xpath("//ul[@class= 'newsList']/li") or ListException()
        # // ul[ @class ="list"]
        # item_list = response.xpath('//div[@class="rg_li"]/li')
        # print(111111111111, item_list)
        for item in item_list:
            bidding = BiddingItem()
            bidding['source_id'] = self.name
            bidding['section'] = params['section']
            bidding['province_name'] = '浙江省'
            bidding['title'] = item.xpath('.//div/h2/a/text()').extract_first().strip()
            bidding['source_url'] = "http://www.myjfjt.com/"+item.xpath('.//div/h2/a/@href').extract_first()
            bidding['public_time'] = item.xpath('.//div[@class = "newsInner"]/h3/text()').extract_first()
            # print(bidding)
            # print(1111,bidding['source_url'])
            yield self.get(url=bidding['source_url'], callback=self.parseDtail, meta={'item': bidding}, priority=10)
        if page < self.maxRange:
            params['page'] = page + 1
            yield from self.getListData(params)

    def parseDtail(self, response):
        # print(14444)
        bidding = response.meta['item']
        if response.xpath("//div[@class = 'newsDetailCont']").extract_first():
            bidding['snapshot'] = response.xpath("//div[@class = 'newsDetailCont']").extract_first()
            print(bidding['snapshot'])
            yield bidding
        else:
            raise ParseException(bidding)