import aiohttp
import asyncio
import requests
import pandas as pd
import json
import time
import csv
import random

# THIS WORKS
'''
async def main2(i):

    async with aiohttp.ClientSession() as session:
        print(f'Starting main %d',i)
        async with session.get('http://python.org', ssl=False) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")
            print('Finishing main %d',i)





async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()

async def main(url):
    print(f'Fetching %d',url)
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        #print(html)

    print('Finished fetching %d',url)

async def doit():
    df = pd.read_csv('Shopify Database - Shopify Data.csv', delimiter=',')
    yo = list(df['Web Site'])
    tasks2 = [main(site) for site in yo[1:10]]
    print(tasks2)

    return await asyncio.gather(*tasks2)

if __name__ == '__main__':


    #any = asyncio.gather(*tasks)
    many = doit()
    asyncio.run(many)
    #asyncio.run(main())

'''

import aiohttp
import asyncio
import requests
import pandas as pd

# TODO: Figure out what to do when client resets connection, I think its shopify saying chill the fuck out,
# so i need to figure out how to open a new connection if that happens...
# TODO: Figure out why fashionnova is raising some issue with the json after a while... What exception even is it??
# Its a content type exception, I can turn of this shit by passing in params (https://github.com/aio-libs/aiohttp/issues/1766)
# The issue becomes, what if I truly just need to skip a site?

# 1. I could just remove the sites as I catch them: inspireuplift.com
# 2. I could do so & make it so each site is scraped synchronously, but each page asynchronously..
# This will prevent me from having to restart everything all the time smdh
# Speaking of which, I think its the opposite rn... Each page is being scrapped syncronously

# OR i can say fuck all of this and aggregate the stats i want


'''
once, we know the number of product pages, we can queue them up in a list
potential algorithm to find number of product pages:
Start at 10, keep doubling, until we get to a page with no product
Once we reach this page, we go to the half way point between the last two indexes (i/2 * 1.5, or i*0.75 = j)
If this page has products, go up to the half point between j and i

If it have no products, Go down to the half point between j and i/2

Keep doing this until you've reached the last page essentially

'''
def get_product_page(url, page):

    url_with_page = url + '/products.json' + '?page={}'.format(page)



    response = requests.get(url_with_page)

    products = response.json()['products']


    return products

def find_last_page(url):
    i = 1
    max = 1
    min = 1

    products = get_product_page(url,i)
    # find last page = i

    while products:
        print(url + '/products.json' + '?page={}'.format(i))
        i *= 2
        products = get_product_page(url,i)

    max = i
    min = i/2
    i = int((max+min) // 2)

    while True:
        #print("MAX: ", max)
        #print(url + '/products.json' + '?page={}'.format(i))
        #print("Min: ", min)
        products = get_product_page(url,i)


        if products:
            print("Products found here updating Min to :", i)
            min = i

        else:
            print("No products found here updating Min to :", i)
            max = i

        if max- min <=1 :
            break

        i = int((max+min) // 2)



    return (i)




headers = [{
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            },
    {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            },
    {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            },
    {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            },
    {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
            }
]

async def get_proxy():
    resp = requests.get("https://api.proxyorbit.com/v1/?token=hHnbWA7WQi4OmSPRl90NTvJuHEnacVmOYL9a5eU77ek&ssl=true&shopify=true&protocols=http")
    js = resp.json()
    random_ip = js['ip']
    random_port = js['port']
    # Zip together


    # This will Fetch Random IP Address and corresponding PORT Number

    random_protocol = js['protocol']

    # convert Tuple into String and formart IP and PORT Address
    proxy = "http://{}:{}".format(random_ip,random_port)

    # Create a Proxy
    #proxy = random_protocol + ip_random_string

    print(proxy)

    # return Proxy
    return proxy


didnt_work = []

'''
async def fetch_product_page(session, url, page, prox):
    url_with_page = url + '/products.json' + '?page={}'.format(page)
    print("Grabbing %s using IP: %s" % (url_with_page, prox))
    sem = asyncio.Semaphore(30)
    async with sem:
        async with session.get(url_with_page, ssl=False, proxy=prox) as response:
            try:
                prod = await response.json()
                prod = prod['products']
            except Exception as inst:
                print(inst)
                print("couldn't grab products from: ", url_with_page)
                didnt_work.append(url_with_page)
                prod = False
        return prod
'''

async def fetch_product_page(session, url, page, prox):
    url_with_page = url + '/products.json' + '?page={}'.format(page)
    print("Grabbing %s using IP: %s" % (url_with_page, prox))
    sem = asyncio.Semaphore(30)
    async with sem:
        async with session.get(url_with_page, ssl=False, proxy=prox) as response:
            prod = await response.json()
            prod = prod['products']
        return prod


async def read_write_products(url):
    t1 = time.perf_counter()
    print(f'Fetching: ',url)
    file_directory = 'products_db/' + url.split('//')[1].split('.')[0] + "_products.csv"
    prox = await get_proxy()
    print("Grabbed %s" % (url ))
    header = random.choice(headers)

    with open(file_directory, 'w') as f:
        f.truncate(0)
        writer = csv.writer(f)
        writer.writerow(['Category', 'Name', 'Variant Name', 'Price', 'URL', 'SKU'])
        page = 1

        async with aiohttp.ClientSession(headers=header) as session:


            #If the proxy is bad try one more time, it shouldn't be bad more than once in a row
            try:
                products = await fetch_product_page(session, url, page, prox)
            except aiohttp.client_exceptions.ClientProxyConnectionError:
                for i in range(10):
                    prox = await get_proxy()
                    products = await fetch_product_page(session, url, page, prox)
                    if products:
                        break

            while products:
                print("Grabbed %f" % (page))
                for product in products:
                    name = product['title']
                    product_url = url + '/products/' + product['handle']
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
                page += 1

                if page > 10:
                    break

                products = await fetch_product_page(session, url, page, prox)

    t2 = time.perf_counter() - t1
    print('Finished fetching %d in %f seconds',url, t2)

async def doit():
    df = pd.read_csv('Shopify Database - Shopify Data.csv', delimiter=',')
    yo = list(df['Web Site'])
    #tasks2 = [read_write_products(('https://' + site)) for site in yo[1:20]]
    tasks2 = [read_write_products(('https://fashionnova.com'))]
    print(tasks2)

    return await asyncio.gather(*tasks2)

if __name__ == '__main__':
    '''
    t1 = time.perf_counter()
    #any = asyncio.gather(*tasks)
    many = doit()
    for i in range(3):
        asyncio.run(many)
    t2 = time.perf_counter() - t1
    print(t2)
    print(didnt_work)
    #asyncio.run(main())
    '''
    find_last_page('https://fashionnova.com')


