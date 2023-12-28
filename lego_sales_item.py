import yaml
import requests
import csv
import bs4
import time
import random
import math
from urllib.parse import urljoin

def load_config():
    """load yaml config, about host and collect_product
    
    """    
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_html_data(url):
    """ To get html data from target host

    Args:
        url (str): target host url

    Returns:
        txt: html data
    """    
    header = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    res = requests.get(url, headers= header) 
    res.encoding = 'utf-8'
    return res.text

def count_page(html_data):
    """Calculate the total page according to the total products
    
    """    
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    total_products = int(soup.find('span', {'data-test': 'result-count'})['data-value'])
    total_page = math.ceil(total_products/18)
    return total_page, total_products

def extract_product_info(product):
    """Get product details

    Args:
        product (_type_): html中的产品页面

    Returns:
        dict: 返回单个产品的信息的字典
    """    
    product_info = {}
    # product number
    product_info['key'] = product['data-test-key']
    
    # product picture
    picture_target = product.find("picture", {"fit": "bounds"})
    product_info['picture'] = picture_target.img['src']

    # product name and url
    title_target = product.find("h3", {'data-test': 'product-leaf-title-row'})
    product_info['title'] = title_target.text
    product_info['url'] = urljoin('https://www.lego.com', title_target.a['href'])

    # original price
    product_info['price'] = product.find("span", {"data-test": "product-leaf-price"}).text

    # discounted price
    product_info['dis_price'] = product.find("span", {"data-test": "product-leaf-discounted-price"}).text

    # discount percentage
    product_info['dis_badge'] = product.find("span", {"data-test": "product-leaf-discount-badge"}).text

    return product_info

def main():
    config = load_config()
    hosts = config.get('hosts', [])
    
    if not hosts:
        raise ValueError('No hosts found in the configuration file.')

    # Get the product number in YAML configuration
    target_keys = config.get('collect', [])
    # print(type(target_keys))
    if not target_keys:
        raise ValueError('No target keys found in the configuration file.')
    
    matched_products = []
    # get products from each host
    for host_config in hosts:
        host_name = host_config.get('name')
        host_url = host_config.get('url')
        
        if not host_name or not host_url:
            raise ValueError('Invalid host configuration in the configuration file.')
        
        print(f'The current page: {host_name}')
        
        with open(f'{host_name}.csv', 'w', encoding='utf-8', newline='') as f:
            csvwriter = csv.DictWriter(f, fieldnames=['key','picture','title','url','price','dis_price','dis_badge'])
            csvwriter.writeheader()

            res = get_html_data(host_url)
            total_page, total_products = count_page(res)
            
            print(f'There are {total_page} pages and {total_products} products in total.')
            
            for i in range(total_page):
                print(f'==========Extracting page {i+1} products==========')
                
                url = f'{host_url}?page={i+1}'
            #  print(url)
                res = get_html_data(url)
                soup = bs4.BeautifulSoup(res, "html.parser") #用bs4模块的beautifulsoup功能将相应的结果解析出来

                products = soup.find_all('article', {'data-test' : 'product-leaf'}) #找到所需产品信息页面

                for product in products:
                    product_info = extract_product_info(product)
                    # print(type(product_info['key']))
                    # product information is written into CSV file
                    csvwriter.writerow(product_info)
                    
                    # Compare each product information with the collection list
                    if int(product_info['key']) in target_keys:
                        matched_products.append(product_info)
                    
                time.sleep(random.randint(1,4))

    # write matched products into csv file
    if matched_products:
        print(f'Found {len(matched_products)} matching products')
        with open('collect_buy.csv', 'w', encoding = 'utf-8', newline='') as collect_file:
            collect_csvwriter = csv.DictWriter(collect_file, fieldnames=['key','picture','title','url','price','dis_price','dis_badge'])
            collect_csvwriter.writeheader()
            collect_csvwriter.writerows(matched_products)
    else:
        print('No matching products')
    
    print('Code end')

if __name__ == '__main__':
    main()