import re
import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver

from .meta_data_for_scraping import inter_dict

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


def scraper_franco(url):
    browser = open_browser()
    browser.get(url=url)
    time.sleep(3)

    bs_base = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()

    for index, prod in enumerate(bs_base.findAll('div', {
        'id': re.compile('^p-([0-9])*$')
    })):
        # Get basic data
        inter_dict['Retailer Name'].append('FrancoSarto')
        inter_dict['Free Shipping'].append('TRUE')
        inter_dict['Available'].append('TRUE')
        inter_dict['Gender'].append('women')
        inter_dict['Main Category'].append(
            inter_dict['Gender'][index].title() + '\'s' + ' Shoes')

        # Get link of product
        link = 'https://www.francosarto.com' + (
               prod.find('div', {
                   'class': 'productBrandTitleColor'}).a['href'])
        print(link)

        inter_dict['URL'].append(link)
        inter_dict['Subcategory'].append(
            bs_base.find('a',
                         {'href': re.compile('Products.aspx$'),
                          'class': 'active'})
            .get_text())

        # Parse product page
        bs_product = get_product(link)

        # Get category of product
        categories = (bs_product.find('span', {'class': 'runa_command'})
                      .attrs['categories'])
        categories = categories.split(',')
        index_cate = categories.index('Wedges')
        if index_cate == len(categories) - 1:
            inter_dict['SubSubcategory'].append(
                categories[index_cate - 1])
        else:
            inter_dict['SubSubcategory'].append(
                categories[index_cate + 1])

        inter_dict['Brand'].append(
            bs_product.find('meta', {'property': 'og:brand'})
            .attrs['content'])

        inter_dict['Color'].append(
            bs_product.find('meta', {'property': 'product:color'})
            .attrs['content'])

        # Here we get sizes of producs
        sizes = []
        for size in (bs_product.find('div', {'id': 'details-sizes'})
                     .children):
            if 'class' in size.attrs:
                sizes.append(size.get_text())
        del sizes[-1]
        inter_dict['Size'].append(sizes)

        # Here we get material of products or
        material = bs_product.find('span', {'itemprop': 'description'})
        if material:
            if material.find('ul'):
                material = material.find('li')
                material = material.get_text().split()
                inter_dict['Material'].append(
                    str(material[0]))
            else:
                inter_dict['Material'].append(
                    'Not specified')
        else:
            inter_dict['Material'].append(
                'Not specified')

        # Get descriptions of product
        inter_dict['Description'].append(
            bs_product.find('span', {'itemprop': 'description'}
                            ).find('p').get_text())
        inter_dict['Meta Description'].append(
            'Buy ' + inter_dict['Description'][index] +
            'on ' + inter_dict['Material'][index])
        inter_dict['Short Description'].append(
            'Product ' + inter_dict['Title'][index] + ' by ' +
            inter_dict['Brand'][index] + ' on ' +
            inter_dict['Color'][index])

        inter_dict['Title'].append(
            bs_product.find('span', {'itemprop': 'name'}).get_text()
            .strip())

        # Meta title equal main title
        inter_dict['Meta Title'] = (
            inter_dict['Title'])
        inter_dict['Image URL'].append(
            'https://www.francosarto.com' +
            bs_product.find('img', {'itemprop': 'image'}).attrs[
                'src'].replace('?preset=details', ''))
        inter_dict['Price'].append(int(float(
            bs_product.find('span', {'class': 'price'})
            .get_text().strip().replace('$', ''))))

        # Try get price on the sale
        sale_price = bs_product.find('span', {'class': 'red price'})
        if sale_price:
            inter_dict['Sale Price'].append(int(float(
                sale_price.get_text().strip().replace('$', ''))))
        else:
            # If sale price does not exist
            inter_dict['Sale Price'] = (
                inter_dict['Price'])
    return inter_dict
