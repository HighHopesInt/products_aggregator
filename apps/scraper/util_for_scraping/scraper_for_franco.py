import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from selenium import webdriver

from .meta_data_for_scraping import intermediate_dictionary


path_to_driver = str(Path.home()) + '/driver/chromedriver'


def open_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options,
                               executable_path=path_to_driver)
    return browser


def get_product(link):
    browser = open_browser()
    browser.get(link)
    html = browser.page_source
    time.sleep(3)
    browser.close()
    return BeautifulSoup(html, 'html.parser')


def scraper_franco(request):
    try:
        browser = open_browser()
        browser.get('https://www.francosarto.com/en-US/_/_/_/'
                    'Wedges/_/Products.aspx?icid=TopNav_Wedges')
        time.sleep(3)
        bs_base = BeautifulSoup(browser.page_source, 'html.parser')
        browser.close()
        for index, prod in enumerate(bs_base.findAll('div', {
            'id': re.compile('^p-([0-9])*$')
        })):
            intermediate_dictionary['Retailer Name'].append('FrancoSarto')
            intermediate_dictionary['Free Shipping'].append('True')
            intermediate_dictionary['Available'].append('True')
            intermediate_dictionary['Gender'].append('women')
            intermediate_dictionary['Main Category'].append(
                intermediate_dictionary['Gender'][index].title() + '\'s' +
                ' Shoes')
            link = 'https://www.francosarto.com' + \
                   prod.find('div', {
                       'class': 'productBrandTitleColor'}).a['href']
            print(link)
            intermediate_dictionary['URL'].append(link)
            intermediate_dictionary['Subcategory'].append(
                bs_base.find('a', {'href': re.compile('Products.aspx$'),
                                   'class': 'active'}).get_text())
            bs_product = get_product(link)
            categories = bs_product.find('span', {'class': 'runa_command'}) \
                .attrs['categories']
            categories = categories.split(',')
            index_cate = categories.index('Wedges')
            if index_cate == len(categories) - 1:
                intermediate_dictionary['SubSubcategory'].append(
                    categories[index_cate - 1])
            else:
                intermediate_dictionary['SubSubcategory'].append(
                    categories[index_cate + 1])
            intermediate_dictionary['Brand'].append(
                bs_product.find('meta', {'property': 'og:brand'
                                         }).attrs['content'])
            intermediate_dictionary['Color'].append(
                bs_product.find('meta', {'property': 'product:color'
                                         }).attrs['content'])
            sizes = []
            for size in bs_product.find('div', {'id': 'details-sizes'}
                                        ).children:
                if 'class' in size.attrs:
                    sizes.append(size.get_text())
            del sizes[-1]
            intermediate_dictionary['Size'].append(sizes)
            material = bs_product.find('span', {'itemprop': 'description'})
            if material:
                if material.find('ul'):
                    material = material.find('li')
                    material = material.get_text().split()
                    intermediate_dictionary['Material'].append(
                        str(material[0]))
                else:
                    intermediate_dictionary['Material'].append(
                        'Not specified')
            else:
                intermediate_dictionary['Material'].append(
                    'Not specified')
            intermediate_dictionary['Description'].append(
                bs_product.find('span', {'itemprop': 'description'}
                                ).find('p').get_text())
            intermediate_dictionary['Meta Description'].append(
                'Buy ' + intermediate_dictionary['Description'][index] +
                'on ' + intermediate_dictionary['Material'][index])
            intermediate_dictionary['Short Description'] = \
                intermediate_dictionary['Description']
            intermediate_dictionary['Title'].append(
                bs_product.find('span', {'itemprop': 'name'}).get_text()
                                                             .strip())
            intermediate_dictionary['Meta Title'] = \
                intermediate_dictionary['Title']
            intermediate_dictionary['Image URL'].append(
                'https://www.francosarto.com' +
                bs_product.find('img', {'itemprop': 'image'}).attrs['src'])
            intermediate_dictionary['Price'].append(
                bs_product.find('span', {'class': 'price'})
                .get_text().strip().replace('$', ''))
            sale_price = bs_product.find('span', {'class': 'red price'})
            if sale_price:
                intermediate_dictionary['Sale Price'].append(
                    sale_price.get_text().strip().replace('$', ''))
            else:
                intermediate_dictionary['Sale Price'] = \
                    intermediate_dictionary['Price']
        return intermediate_dictionary
    except requests.exceptions.Timeout:
        messages.error(request, 'Timeout. Try again')
    except IndexError:
        print(intermediate_dictionary['Description'])
        print(intermediate_dictionary['Material'])
        print(len(intermediate_dictionary['Description']))
        print(len(intermediate_dictionary['Material']))
