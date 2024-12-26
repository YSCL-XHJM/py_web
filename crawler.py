import requests
from bs4 import BeautifulSoup
import time
from urllib.robotparser import RobotFileParser

def can_fetch(url):
    rp = RobotFileParser()
    rp.set_url(url + "/robots.txt")#设置目标网站的 robots.txt 文件的完整 URL
    try:
        rp.read()#从网络上读取并解析由 set_url 方法指定的 robots.txt 文件
        return rp.can_fetch("*", url)#是否允许抓取
    except Exception as e:
        print(f"无法读取 robots.txt for {url}: {e}")
        # 如果无法读取robots.txt，默认允许抓取
        return True

def scrape_and_save(url, filename):
    try:
        if not can_fetch(url):
            print(f"不允许访问该网址 {url} ")
            return

        response = requests.get(url)#发送 GET 请求到指定的 URL
        response.raise_for_status()#检查 Response 对象中的 HTTP 状态码

        # 使用response.apparent_encoding匹配网页编码
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')#标准内置解析器

        # 提取更多信息，如标题、段落等
        title = soup.title.string if soup.title else "No Title"
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        #调用 .get_text() 方法来提取p标签内的所有文本内容,strip=True去除空白字符
        content = f"Title: {title}\n\n{'\n'.join(paragraphs)}"#将所有段落用换行符连接起来，形成一个多行字符串

        with open(filename, 'w', encoding='utf-8') as file:#以写的形式打开文件
            file.write(content)

        print(f"Content saved to {filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")


urls = [
    "https://www.yjwujian.cn/"
]

for i, url in enumerate(urls, start=1):
    scrape_and_save(url, f"{i}.txt")
    time.sleep(1)