import re

import requests
from bs4 import BeautifulSoup

from .meta_data_for_scraping import headers, inter_dict
from .valutate import get_current_usd


def scraper_saks(url):
    base_url = url
    request_to_base_url = requests.get(base_url, headers=headers,
                                       timeout=20)
    bsobj_base_site = BeautifulSoup(request_to_base_url.text,
                                    'html.parser')
    for index, item in enumerate(
            bsobj_base_site.findAll(
                'div', {'id': re.compile('^product-([0-9])*$')}
            )):
        inter_dict['Free Shipping'].append('FALSE')
        inter_dict['Available'].append('TRUE')
        inter_dict['Retailer Name'].append(list(
            bsobj_base_site.find('a',
                                 {'class': 'hbc-header__logo'}).children
        )[0].get_text())
        inter_dict['Main Category'].append(list(
            bsobj_base_site.find('a', {'id': 'bc-306418052'}).children
        )[0].get_text() + ' Shoes')
        inter_dict['Subcategory'].append(
            bsobj_base_site.find(
                'a', {'id': 'category-306418205'}
            ).get_text().strip())
        inter_dict['SubSubcategory'].append(
            bsobj_base_site.find(
                'a', {'id': 'refinement-306420996'}
            ).get_text().strip())
        inter_dict['Gender'].append(list(
            bsobj_base_site.find('a', {'id': 'bc-306418052'}).children
        )[0].get_text())
        link = item['data-url']
        print(link)
        inter_dict['Image URL'].append(item['data-image'])
        bsobj_product = get_product_url(link)
        inter_dict['URL'].append(link)
        price = bsobj_product.find('span', {'itemprop':
                                            re.compile('[P|p]rice$')})
        if price:
            price = price.attrs['content']

            inter_dict['Price'].append(price)
            inter_dict['Price'][index] = int(float(
                inter_dict['Price'][index])) // int(
                get_current_usd())
        else:
            inter_dict['Price'].append('')
        color = bsobj_product.find('dd', {'class': re.compile('^product-var')})
        if color:
            inter_dict['Color'].append(color.get_text())
        else:
            inter_dict['Color'].append('')
        inter_dict['Sale Price'] = (
            inter_dict['Price'])
        inter_dict['Brand'].append(bsobj_product.find('a', {
            'class': 'product-overview__brand-link'
        }).get_text())
        size = bsobj_product.find('div', {'class': 'product-size-options'})
        size_product = []
        if size:
            size = size.find('ul', {'class':
                                    'product-variant-attribute-values'})
            if size:
                for si in size.children:
                    if 'product-variant-attribute-value--unavailable' \
                            not in si.attrs['class']:
                        size_product.append(si.span.get_text().replace(' M',
                                                                       ''))
        else:
            size_product.append('')
        inter_dict['Size'].append(size_product)
        inter_dict['Material'].append(bsobj_product.find(
            'div', {'itemprop': 'description'}
            ).find('ul').find('li').get_text().replace(' upper', ''))
        inter_dict['Title'].append(bsobj_product.find(
            'h1', {'class': 'product-overview__short-description'}
            ).get_text())
        if isinstance(bsobj_product.find('div', {'itemprop':
                                                 'description'}
                                         ).contents[0], str):
            inter_dict['Description'].append(
                bsobj_product.find(
                    'div', {'itemprop': 'description'}).contents[0])
        else:
            inter_dict['Description'].append(
             'Product ' + inter_dict['Title'][index] + ' by ' +
             inter_dict['Brand'][index])
        inter_dict['Short Description'].append(
            'Product ' + inter_dict['Title'][index] + ' by ' +
            inter_dict['Brand'][index] + ' in ' +
            inter_dict['Color'][index])
        inter_dict['Meta Description'].append(
            'Buy' + str(inter_dict['Description'][index]) +
            'on ' + str(inter_dict['Material'][index]))
        inter_dict['Meta Title'] = \
            inter_dict['Title']
    return inter_dict


def get_product_url(link):
    request_link = requests.get(link, headers=headers, timeout=20)
    html = BeautifulSoup(request_link.text, 'html.parser')
    return html
