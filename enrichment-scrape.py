import pandas as pd
import csv
import json
import urllib3
from bs4 import BeautifulSoup
import humanfriendly
import aiohttp
import time
import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# todo
# add error handling
# Add try catch to requests
# Use  Rotating User Agents

# ADD asynconous capabilities

# Write script to find social links
# Write script to catch errors

# Add time outs to shopify scraper


def get_proxy():
    resp = requests.get("https://api.proxyorbit.com/v1/?token=hHnbWA7WQi4OmSPRl90NTvJuHEnacVmOYL9a5eU77ek&ssl=true&shopify=true")
    js = resp.json()
    random_ip = js['ip']
    random_port = js['port']
    # Zip together


    # This will Fetch Random IP Address and corresponding PORT Number

    random_protocol = js['protocol']

    # convert Tuple into String and formart IP and PORT Address
    ip_random_string = "{}:{}".format(random_ip,random_port)

    # Create a Proxy
    proxy = {random_protocol:ip_random_string}

    # return Proxy
    return proxy

class ShopScraper():

    def __init__(self, url):
        self.base_url = 'https://' + url

        self.tricks = []
        self.fb_handle = ''
        self.ig_handle = ''
        self.fb_likes = -1
        self.ig_followers = -1
        self.ping_count = 0
        self.proxy = {}
        self._headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            }
        # self.get_social_links()

    def get_product_page(self, page):
        '''
        url_with_page = self.base_url + '/products.json' + '?page={}'.format(page)
        print(f"Fetching: {url_with_page}")
        response = requests.get(url_with_page, timeout=4, proxies=proxy)
        time.sleep(0.5)
        products = json.loads(response.content)['products']
        print(products)
        '''
        '''
        # With proxy rotator
        url_with_page = self.base_url + '/products.json' + '?page={}'.format(page)
        proxy = proxy_rotator.Random_Proxy()
        request_type = "get"
        response = proxy.Proxy_Request(url=url_with_page, request_type=request_type, proxies=proxy)
        products = json.loads(response.content)['products']
        '''
        url_with_page = self.base_url + '/products.json' + '?page={}'.format(page)

        print(f"Fetching: {url_with_page}")
        if (self.ping_count % 10 == 0):
            self.proxy = get_proxy()
            time.sleep(2)

        response = requests.get(url_with_page, timeout=4, proxies=self.proxy, headers=self._headers)

        products = json.loads(response.content)['products']

        self.ping_count += 1


        return products


    def write_products(self):

        file_directory = 'products_db/' + self.base_url.split('//')[1].split('.')[0] + "_products.csv "
        with open(file_directory, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Name', 'Variant Name', 'Price', 'URL', 'SKU'])
            page = 1
            if q % 3 == 0:
                time.sleep(3)
            products = self.get_product_page(page)
            while (products):
                for product in products:
                    name = product['title']
                    product_url = self.base_url + '/products/' + product['handle']
                    category = product['product_type']
                    for variant in product['variants']:
                        variant_names = []
                        for i in range(1, 4):
                            k = 'option{}'.format(i)
                            if variant.get(k) and variant.get(k) != 'Default Title':
                                variant_names.append(variant[k])
                        variant_name = ' '.join(variant_names)

                        # Get Sku
                        sku = variant['sku']

                        # Get price
                        price = variant['price']

                        # Turn into row list and write as link in csv
                        row = [category, name, variant_name, price, product_url, sku]
                        #print(row)

                        writer.writerow(row)
                # REMOVE THIS
                if page > 10:
                 break
                page += 1
                products = self.get_product_page(page)

    def get_social_links(self):
        # return dictionary of social links
        # Facebook, twitter.com, instagram, anythingelse
        pass

    def get_fb_info(self):
        # so far only returns facebook likes
        community_page = requests.get(f"https://facebook.com/pg/{self.fb_handle}/community")
        document = BeautifulSoup(community_page.content, 'html.parser')
        page_likes = humanfriendly.parse_size(
            document.find(text='Total Likes').parent.previous.replace(',', '')
        )
        self.fb_likes = int(page_likes)
        return page_likes

    def get_ig_info(self):
        # This works, I'm not sure if I need selenium or nah

        username = self.ig_handle
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options)
        browser.get('https://www.instagram.com/' + username + '/?hl=en')
        Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        source = browser.page_source
        data = BeautifulSoup(source, 'html.parser')
        scripts = data.select('script[type="application/ld+json"]')
        scripts_content = json.loads(scripts[0].text.strip())
        main_entity_of_page = scripts_content['mainEntityofPage']
        interaction_statistic = main_entity_of_page['interactionStatistic']
        followers = interaction_statistic['userInteractionCount']
        self.ig_followers = int(followers)
        return followers

    def get_ad_info(self):
        pass

    def get_fb_page_id(self, page_name):
        # so far only returns facebook likes
        community_page = requests.get(f"https://facebook.com/pg/{page_name}/about")
        document = BeautifulSoup(community_page.content, 'html.parser')
        first_one = document.find('a', rel='dialog')
        page_id = first_one.__str__().split('page_id=')[1].split(';')[0].strip('&amp')
        return page_id




'''
# Read the CSV into a pandas data frame (df)
df = pd.read_csv('Shopify Database - Shopify Data.csv', delimiter=',')
yo = list(df['Web Site'])
print(yo[1:10])
q = 0
for site in yo[1:10]:
    if q %3 == 0:
        time.sleep(3)
    site = "https://" + site
    get_products(site)
'''



if __name__ == '__main__':
    # Read the CSV into a pandas data frame (df)
    df = pd.read_csv('Shopify Database - Shopify Data.csv', delimiter=',')
    yo = list(df['Web Site'])
    print(yo[1:10])
    q = 0
    t1 = time.perf_counter()
    site = yo[6]
    print(site)
    temp = ShopScraper(site)
    temp.write_products()

    t2 = time.perf_counter() - t1
    print(f'Total Time to Scrape {site}: {t2:0.2f} seconds')

