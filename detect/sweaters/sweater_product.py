# -*- coding: utf-8 -*-

import requests
from lxml import html, etree
import pysnooper
import random
from fake_useragent import UserAgent
import sys
sys.path.append("../..")
import bearychat_send as bs

"""get the information from sweater websites"""

@pysnooper.snoop()
def __product(url_product, product_title_xpath, product_price_xpath, product_size_xpath, current_price):
    #user agent
    url_detail = url_product
    count = 0
    #Because of anti-scrapy, running until get the information or up to 50x
    while True:
        count += 1
        # get the result of price and title
        html_etree = html_request(url_detail)
        product_title = html_etree.xpath(product_title_xpath) 
        product_price = html_etree.xpath(product_price_xpath) 
        product_size = html_etree.xpath(product_size_xpath) 
        # break when get info or fails
        if product_price or count > 30:
            break
    #store data to dictionary and then return
    news_dictionary = {"product": "Failed to get infomation",
                        "price":"$$$"}
    #title
    try:
        __product_title = product_title[0].strip()
        if __product_title:
            d_product = {"product": __product_title}
        news_dictionary.update(d_product)
    except:
        pass
    #size
    try:               
        print(product_size)
        __product_size = product_size[0].strip()
    except:
        __product_size = " "
    #price
    try:                  
        __product_price = product_price[0].strip()  
        d_price = "$$$"              
        if product_price[0].strip() == current_price: # if price changed
            d_price = {"price": "Price: " + __product_price}
        else:
            d_price = {"price": "Original price: " + \
                        current_price + "\n" + \
                        "Sale: " + __product_price + "\n" + \
                        __product_size}
        news_dictionary.update(d_price)
    except:
        pass



    return news_dictionary

def html_request(url_detail):
    #return html request with cookie, header
    cookies = 'v=3; \
                iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; \
                webp=true; \
                ci=1%2C%E5%8C%97%E4%BA%AC; \
                __guid=26581345.3954606544145667000.1530879049181.8303; \
                _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; \
                _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; \
                monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; \
                __mta=189118996.1530879050545.1530936763555.1530937843742.18'
    cookie = {}
    for line in cookies.split(';'):
        name, value = cookies.strip().split('=', 1)
        cookie[name] = value
    user_agent = UserAgent().random
    HEADERS = {'User-Agent':user_agent,
                'Referer': "www.google.com"}
    response = requests.get(url_detail, cookies=cookie, headers=HEADERS)
    html_etree = etree.HTML(response.content.decode('utf-8'))
    return html_etree

def detect(data):
    # return product price and name from amazon    
    url_product = data.get("url_product") 
    url_img = data.get("url_img") 
    message_title = data.get("message_title")
    product_title_xpath = data.get("product_title_xpath")
    product_price_xpath = data.get("product_price_xpath")
    product_size_xpath = data.get("product_size_xpath")
    current_price = data.get("current_price")
    #detect price and title of product
    product_inform = __product(url_product, product_title_xpath, product_price_xpath, product_size_xpath, current_price)
    #send to beary chat
    bs.send(True, 
            message_title, 
            message_title, 
            "shop-list", #channel
            [{
                "title": product_inform.get("product"),
                "url": url_product,
                "text": product_inform.get("price"),
                "images": [
                    {"url": url_img}
                ]
            }]
    )
    
def main():
    pass
    #detect()

if __name__ == "__main__":
    main()

