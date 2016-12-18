# coding=utf-8
import scrapy


class ZhhilianSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        "http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&jl=%E7%83%9F%E5%8F%B0&sm=0&p=1",
        #"http://sou.zhaopin.com/jobs/searchresult.ashx?bj=160000&jl=%E5%8C%97%E4%BA%AC&p=1&isadv=0"
    ]

    def parse(self, response):
        """
        charset = response.xpath(
            "//meta[contains(@content,'charset')]/@content").extract_first()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print(charset)
        """

        for t in response.css('table.newlist'):
            zwmc_res = t.css("td.zwmc").xpath(".//a/text()").extract_first()
            zwurl = t.css("td.zwmc a::attr(href)").extract_first()
            gsmc_res = t.css("td.gsmc").xpath(".//a/text()").extract_first()
            zwyx_res = t.css("td.zwyx::text").extract_first()
            gzdd_res = t.css("td.gzdd::text").extract_first()
            gxsj_res = t.css("td.gxsj span::text").extract_first()
            detail1 = " ".join(
                t.css("li.newlist_deatil_two span::text").extract())
            detail2 = t.css("li.newlist_deatil_last::text").extract_first()
            if zwmc_res and gsmc_res:
                # print(zwyx_res)
                #print(u"{}->{}->{}".format(gsmc_res.encode("utf-8", 'ignore'), zwmc_res.encode("utf-8", "ignore"), zwyx_res))
                yield {
                    "职位名称（zwmc）": zwmc_res,
                    "公司名称（gsmc）": gsmc_res,
                    "职位月薪（zwyx）": zwyx_res,
                    "工作地点（gzdd）": gzdd_res,
                    "更新时间（gxsj）": gxsj_res,
                    "概要信息（detail1）": detail1,
                    "职位要求（detail2）": detail2,
                    'url': zwurl
                }
        next_page_url = response.css(
            "li.pagesDown-pos a.next-page::attr(href)").extract_first()
        if next_page_url is not None:
            next_page = response.urljoin(next_page_url)
            yield scrapy.Request(next_page, callback=self.parse)
