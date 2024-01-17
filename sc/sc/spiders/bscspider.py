import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime
import re

class BscSpider(scrapy.Spider):
    name = "bsc"
    allowed_domains = ["bscscan.com"]
    start_urls = ["https://bscscan.com/txs?a=0xD43b86CD7ccD89cb127F028E47A1F9d51029Eba8"]
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        for i in range(1, 51):            
            transaction_url_selector = f'#ContentPlaceHolder1_divTransactions > div.table-responsive > table > tbody > tr:nth-child({i}) > td:nth-child(2) > div > span > a::attr(href)'
            transaction_url = response.css(transaction_url_selector).get()
            if transaction_url:
                yield response.follow(transaction_url, self.parse_transaction)
            else:
                self.logger.warning(f"No href attribute in {transaction_url_selector}")

            next_page_selector = '#ContentPlaceHolder1_divBottomPagination > nav > ul > li:nth-child(4) > a::attr(href)'
            next_page_url = response.css(next_page_selector).get()
            if next_page_url:
                yield SplashRequest(response.urljoin(next_page_url), self.parse, args={'wait': 0.5})
            
            
    def parse_transaction(self, response):
        formatted_timestamp = ''
        address = ''
        amount = 0
        formatted_release_timestamp = ''
        timestamp_selector = '#ContentPlaceHolder1_divTimeStamp > div > div.col-md-9'
        timestamp_html = response.css(timestamp_selector).get()
        if timestamp_html is not None:
            timestamp_str = re.search(r'<span id="showUtcLocalDate" data-timestamp="\d+">(.*?)</span>', timestamp_html).group(1)
            timestamp_str = timestamp_str.rsplit(' ', 1)[0]
            timestamp = datetime.strptime(timestamp_str, '%b-%d-%Y %I:%M:%S %p')
            formatted_timestamp = timestamp.strftime('%d.%m.%Y')
        else:
            self.logger.warning(f"No elements match {timestamp_selector}")
            
        input_data = response.css('#inputdata::text').get()
        if input_data is not None:
            address = '0x' + re.search(r'\[0\]:\s+000000000000000000000000(.*?)$', input_data, re.MULTILINE).group(1)
            amount = int(re.search(r'\[1\]:\s+(.*?)$', input_data, re.MULTILINE).group(1), 16) / 10**18
            release_timestamp = datetime.fromtimestamp(int(re.search(r'\[2\]:\s+(.*?)$', input_data, re.MULTILINE).group(1), 16))
            formatted_release_timestamp = release_timestamp.strftime('%d.%m.%Y')
        else:
            self.logger.warning(f"No elements match #inputdata::text")

        yield {
            'timestamp': formatted_timestamp,
            'address': address,
            'amount': amount,
            'release': formatted_release_timestamp,
        }