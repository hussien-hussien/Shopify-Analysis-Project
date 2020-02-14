
import scrapy

# -----
'''
class QuotesSpider(scrapy.Spider):
    name = "stores"

    start_urls = ['https://myip.ms/browse/sites/1/hostID/376095/hostID_A/1/sort/6/asc/1#sites_tbl_top']

    def parse(self, response):

        self.logger.info('hello this is my first spider')

        yield {
            'sites': response.xpath("//td[@class='row_name']/a/text()").getall()
        }

        #next_page = response.css('li.next a::attr(href)').get()

        #if next_page is not None:
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse)



# https://myip.ms/browse/sites/1/hostID/376095/hostID_A/1

# //input[@id='captcha_submit']

'''

# ---

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#import chromeDriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import json
from tkinter import messagebox




def get_shops():
    url = "https://myip.ms/browse/sites/1/hostID/376095/hostID_A/1/sort/6/asc/1#a"
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
    browser = webdriver.Chrome(chrome_options=opts)

    #browser = webdriver.Firefox(executable_path=r'/Users/hussienhussien/Desktop/DSU/shop-scrape/geckodriver')


    browser.get(url)


    #options.set_preference('dom.webnotifications.enabled', False)
    links_list = []

    for i in range(2,5):



        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('td', class_='row_name')
        #print(rows)



        for j in rows:
            print("Page #", str(i), " ", j.get_text().strip('\n'))
            links_list.append(j.get_text().strip('\n'))

        next_page = '//a[@href="#'+ str(i) +'"]'


        browser.find_element_by_xpath(next_page).click()
        time.sleep(2)
        time.sleep(2)
        try:
            while (True):
                print("trying to click captcha")
                print('BEFORE CLICK')
                #print(browser.page_source)
                #print(browser.find_element_by_xpath("//input[@id='captcha_submit']"))
                browser.find_element_by_xpath("//input[@id='captcha_submit']").click()
                print("Captcha Clicked")
                time.sleep(2)

            print("After")
        except:
            #print(browser.page_source)
            browser.find_element_by_xpath(next_page).click()
            print('whoops')


    with open('scraped.json', 'w') as file:
            json.dump(links_list, file,indent=2)

#get_shops()


def get_shops_test():


    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_experimental_option("user-agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
    #browser = webdriver.Chrome(options=options, executable_path=r'/Users/hussienhussien/Desktop/DSU/shop-scrape/chromedriver')
    browser = webdriver.Chrome(options=options)

    url = "https://myip.ms/browse/sites/1/hostID/376095/hostID_A/1/sort/6/asc/1#a"
    #browser = webdriver.Chrome()

    browser.get(url)


    #options.set_preference('dom.webnotifications.enabled', False)
    links_list = []

    for i in range(2,5):



        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('td', class_='row_name')
        #print(rows)



        for j in rows:
            print("Page #", str(i), " ", j.get_text().strip('\n'))
            links_list.append(j.get_text().strip('\n'))

        next_page = '//a[@href="#'+ str(i) +'"]'


        browser.find_element_by_xpath(next_page).click()
        time.sleep(2)
        time.sleep(2)
        try:
            count = 0
            while (True):
                print("trying to click captcha")
                print('BEFORE CLICK')
                #print(browser.page_source)
                #print(browser.find_element_by_xpath("//input[@id='captcha_submit']"))
                browser.find_element_by_xpath("//input[@id='captcha_submit']").click()
                print("Captcha Clicked")
                time.sleep(2)
                count+=1
                print(count)
                if count == 3:
                    time.sleep(30)
                    print("WAITING FOR YOU HUSSIEN")

            print("After")
        except:
            #print(browser.page_source)
            browser.find_element_by_xpath(next_page).click()
            print('whoops')


    with open('scraped.json', 'w') as file:
            json.dump(links_list, file,indent=2)

#get_shops_test()

def get_shops_test2():


    url = "https://myip.ms/browse/sites/1/hostID/376095/hostID_A/1/sort/6/asc/1#a"
    PROXY="184.149.34.86:8080"
    opts = Options()
    opts.add_argument('--proxy-server=%s' % PROXY)
    opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
    opts.add_argument("start-maximized")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(chrome_options=opts)

    #browser = webdriver.Firefox(executable_path=r'/Users/hussienhussien/Desktop/DSU/shop-scrape/geckodriver')


    browser.get(url)



    links_list = []

    for i in range(2,5):



        time.sleep(10)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('td', class_='row_name')
        #print(rows)



        for j in rows:
            print("Page #", str(i), " ", j.get_text().strip('\n'))
            links_list.append(j.get_text().strip('\n'))

        next_page = '//a[@href="#'+ str(i) +'"]'


        browser.find_element_by_xpath(next_page).click()
        time.sleep(3)

        try:
            while (True):
                print("trying to click captcha")
                print('BEFORE CLICK')
                #print(browser.page_source)
                #print(browser.find_element_by_xpath("//input[@id='captcha_submit']"))
                browser.find_element_by_xpath("//input[@id='captcha_submit']")
                messagebox.showinfo(title='2-step verification', message='Finish on screen 2-step verification, and then click OK.')
                print("Captcha Clicked")
                time.sleep(2)

            print("After")
        except:
            #print(browser.page_source)
            browser.find_element_by_xpath(next_page).click()


    links_list = list(set(links_list))
    with open('scraped.json', 'w') as file:
            json.dump(links_list, file,indent=2)

#get_shops_test2()

#import phantomjs as pj
def proxied(self, proxy):
    capabilities = pj.Phantom.DesiredCapabilities.PHANTOMJS.copy()
    capabilities['phantomjs.cli.args'] = [
        '--proxy=' + proxy,
        '--proxy-type=http',
        '--proxy-auth=' + evar.get('PROXY_USER') + ':' + evar.get('PROXY_PASS')
    ]

    return webdriver.Remote(
        command_executor=self.selenium,
        desired_capabilities=capabilities
    )

def testUserLocationAlbuquerque(self):
    self.driver = self.proxied('albuquerque.wonderproxy.com:11000')
    self.driver.get(self.url)
    search = self.driver.find_element_by_id('user-city')
    self.assertIn('Albuquerque', search.text)

print("Woah Virtual Enviroment is neccesary bub")
