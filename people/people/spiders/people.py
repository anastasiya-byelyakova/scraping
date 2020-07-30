from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import re
from datetime import datetime
from selenium.webdriver.chrome.options import Options
import pandas as pd

from people.settings import CSV_FILE

class SpiderSpider(CrawlSpider):
    name = 'people'
    allowed_domains = ['morganlewis.com']
    start_urls = ['http://www.morganlewis.com/our-people']

    def start_requests(self):

        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        parsed = pd.read_csv(CSV_FILE)

        if not parsed.empty:
            parsed_links = set(parsed['Url to the employe profile'])
        else:
            parsed_links = []


        with webdriver.Chrome(
                executable_path=ChromeDriverManager().install(),
                chrome_options=options
        ) as driver:
            driver.get(self.start_urls[0])
            time.sleep(1)
            i = 1
            while True:
                i += 1
                try:
                    time.sleep(1)
                    links = (k.get_attribute('href') for k in driver.find_elements_by_xpath(
                        '//div[@class="c-content_team__card-info"]/a'))

                    for link in links:
                        if link not in parsed_links:
                            yield Request(link,
                                          callback=self.parse_person)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    ActionChains(driver).move_to_element(
                        driver.find_element_by_xpath(f'//*[@data-pagenum="{i}"]')).click().perform()
                except:
                    break

    def parse_person(self, response):

        profile_url = response.url
        photo_url = response.xpath(
            '//div[@class="thumbnail"]/img/@src').extract_first()
        name = response.xpath('//h1/span/text()').extract_first()
        email = response.xpath('//p[@class="bio-mail-id"]/a/@href').extract_first()
        position = response.xpath(
            '//*[@id="contentWrapper"]/div[2]/div[2]/div/div[1]/section[1]/h2/text()').extract_first()
        sectors = response.xpath(
            '//*[@id="contentWrapper"]/div[2]/div[2]/div/div[1]/aside/div/div[2]/ul/li/a/text()').extract()
        serivices = response.xpath(
            '//*[@id="contentWrapper"]/div[2]/div[2]/div/div[1]/aside/div/section[1]/ul/li/a/text()').extract()
        phones = re.findall('(\+[0-9\.]*)', response.body.decode('utf-8'))
        publications = response.xpath(
            '//*[@id="pubexpandlist"]//text()').extract()  # //div[@class="ml-publication-media"]/@data-tooltip-text
        brief = response.xpath(
            '//*[@id="contentWrapper"]/div[2]/div[2]/div/div[1]/section[2]/div/div[1]/div/p/text()').extract_first()
        date = datetime.now().strftime("%d/%B/%Y %H:%M:%S")

        yield {
            'Url to the employe profile': profile_url,
            'Photo url': photo_url,
            'Full name': name,
            'Position': position,
            'Phone numbers': phones,
            'Email': email,
            'Services': serivices,
            'Sectors': sectors,
            "Publications": publications,
            "Person brief": brief,
            "DateTime of scraping the profile": date

        }
