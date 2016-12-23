# -*- coding: utf-8 -*-
import scrapy
import urllib.request
import ssl
import os


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["douban.com"]

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"}

    def start_requests(self):
        # 首先爬一次登录页，然后进入回调函数parse
        return [scrapy.Request("https://accounts.douban.com/login", meta={"cookiejar": 1}, callback=self.parse)]

    def parse(self, response):
        # 获取验证码图片所在地址
        captcha=response.xpath('//img[@id="captcha_image"]/@src').extract()

        # 所以需要判断此时是否需要输入验证码，若captcha列表中有元素，说明有验证码信息
        if len(captcha)>0:
            print("此时有验证码")
            localpath = "captcha.png"
            urllib.request.urlretrieve(captcha[0], filename=localpath)
            print("请查看本地图片captcha.png并输入对应验证码：")
            # 通过input()等待我们输入对应的验证码并赋给captcha_value变量
            captcha_value = input()

            '''使用云打码
            cmd = "D:/python27/python D:/python27/yzm/YDMPythonDemo.py"
            r = os.popen(cmd)
            captcha_value = r.read()
            r.close()
            '''
            print("输入的验证码为："+str(captcha_value))
            # 设置要传递的post信息
            data = {
                "form_email": "1260164843@qq.com",
                "form_password": "**",
                "captcha-solution": captcha_value,
                "redir": "https://www.douban.com/people/66430852/",  # 设置登录后需要转向的网址
                # "login":"登录",
            }
        else:
            print("此时没有验证码")
            data={
                "form_email": "1260164843@qq.com",
                "form_password": "**",
                "redir": "https://www.douban.com/people/66430852/",
            }
        print("登录中…")

        # 通过FormRequest.from_response()进行登陆
        return [scrapy.FormRequest.from_response(
            response,
            meta={"cookiejar": response.meta["cookiejar"]},
            headers=self.header,
            formdata=data,
            callback=self.next
        )]


    def next(self, response):
        # 分别提取网页标题、日记标题、日记发表时间、日记内容、日记链接
        title = response.xpath("/html/head/title/text()").extract_first()
        notetitle = response.xpath("//div[@class='note-header pl2']/a/@title").extract()
        notetime = response.xpath("//*[@class='note-header pl2']/div/span/text()").extract()
        notecontent = response.xpath("//div[@class='note']/text()").extract()
        noteurl = response.xpath("//div[@class='note-header pl2']/a/@href").extract()
        print("网页标题是："+title)

        # 可能有多篇日记，通过for循环依次遍历
        for i in range(0,len(notetitle)):
            print("第"+str(i+1)+"篇文章的信息如下:")
            print("文章标题为："+notetitle[i])
            print("文章发表时间为：" + notetime[i])
            print("文章内容为：" + notecontent[i])
            print("文章链接为：" + noteurl[i])
            print("------------")

