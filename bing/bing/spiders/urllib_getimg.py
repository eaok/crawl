import urllib.request
import re

def get_file(url):
    try:
        data=urllib.request.urlopen(url).read()
        return data
    except BaseException as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        return None

def getcontent(url):
    #模拟成浏览器
    headers = ("User-Agent","Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36")
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    #将opener安装为全局
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(url).read().decode("utf-8")
    #构建段子内容提取的正则表达式
    contentpat='g_img={url: "(.*?)"'
    #寻找出所有的内容
    content=re.compile(contentpat,re.S).findall(data)
    img_url = 'https://cn.bing.com' + content[0]
    print(img_url)
    f = open(img_url.split('/')[-1], "wb")
    f.write(get_file(img_url))
    f.flush()
    f.close()
    print("Successfully generated " + img_url.split('/')[-1] + "!")

if __name__ == "__main__":
    url="https://cn.bing.com"
    getcontent(url)
