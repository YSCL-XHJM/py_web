import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
#logging: 用于记录日志信息。
#selenium: 是一个自动化Web浏览器交互的工具。
#webdriver, EdgeService, EdgeOptions: 用于配置和启动Microsoft Edge浏览器实例。
#By, WebDriverWait, expected_conditions: 用来等待页面元素加载完成，确保与页面的交互是可靠的。
#BeautifulSoup: 用于解析HTML文档，方便提取数据。

# 设置日志级别,设置了日志的基本配置，将日志级别设为INFO，意味着会记录所有INFO级别的消息以及更高级别的警告和错误。
logging.basicConfig(level=logging.INFO)


def setup_driver():
    service = EdgeService(executable_path=r'D:\edge\edgedriver_win64\msedgedriver.exe')
    options = EdgeOptions()#创建一个 EdgeOptions 对象
    options.add_argument('--headless')  #向 EdgeOptions 对象添加一个命令行参数 --headless,即无头模式
    return webdriver.Edge(service=service, options=options)
    #返回一个新的 webdriver.Edge 实例。创建这个实例时，传入之前配置好的 service 和 options 参数。
    # 这意味着该 WebDriver 将使用指定的服务配置和浏览器选项来启动 Edge 浏览器。
#创建并返回一个Edge WebDriver实例，
# 它被配置为在无头模式下运行（即不显示浏览器窗口）。这有助于在服务器环境中或不需要GUI时运行脚本。

def fetch_and_save_content(driver, url):
    try:
        driver.get(url)
        # 等待页面加载，并等待特定元素出现（一个具有'title'属性的'span'）
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[@title]"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 使用更具体的选择器来查找所有具有'title'属性的'span'标签
        title_spans = soup.find_all('span', {'title': True})
        if not title_spans:
            logging.warning("未能找到具有'title'属性的'span'标签")
            return

        # 提取文本内容
        text_contents = [span.get_text(strip=True) for span in title_spans]

        # 写入文件
        with open('out.txt', 'w', encoding='utf-8') as file:
            for text in text_contents:
                file.write(text + '\n\n')
        logging.info("已成功保存到out.txt")
    except Exception as e:
        logging.error(f"发生错误: {e}")
        raise
#fetch_and_save_content函数接收WebDriver实例和目标URL作为参数，尝试访问该URL，
# 并等待页面加载完成直到找到至少一个具有title属性的span元素。
#然后，它使用BeautifulSoup解析页面源代码，并查找所有符合条件的span标签，
# 提取它们的文本内容，并将这些内容写入到out.txt文件中。
def main():
    driver = None
    try:
        driver = setup_driver()
        fetch_and_save_content(driver, 'http://g-ican.com/news/list')
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()