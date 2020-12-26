import scrapy
from ..items import HandreqproItem


class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    # allowed_domains = ['xxx.com']
    # 自定义方法用来生成urls没用，框架调不到自定义的方法，就需要自己手动发请求
    start_urls = ['https://duanziwang.com/category/经典段子/1/']

    # 通用的url模板
    url = 'https://duanziwang.com/category/经典段子/%d/'
    page_num = 2

    # 父类方法：这个是该方法的原始实现
    def start_requests(self):
        for u in self.start_urls:
            # 手动对第一页发送请求
            yield scrapy.Request(url=u, callback=self.parse)

    # 将段子网中所有页码对应的数据进行爬取
    def parse(self, response):
        # 数据解析名称和内容
        article_list = response.xpath('/html/body/section/div/div/main/article')
        for article in article_list:
            title = article.xpath('./div[1]/h1/a/text()').extract_first()
            content = article.xpath('./div[2]/p/text()').extract_first()

            item = HandreqproItem()
            item['title'] = title
            item['content'] = content

            yield item

        if self.page_num < 10:  # 结束递归的条件
            new_url = format(self.url % self.page_num)
            self.page_num += 1

            # 对第一页以后的 新的页码对应的url再次进行请求发送（手动请求GET发送）
            yield scrapy.Request(url=new_url,callback=self.parse)
