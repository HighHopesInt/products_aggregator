import re

import requests
from bs4 import BeautifulSoup

from .meta_data_for_scraping import headers, inter_dict
from .valutate import get_current_usd


def get_product_url(link):
    request_link = requests.get(link, headers=headers, timeout=20)
    html = BeautifulSoup(request_link.text, 'html.parser')
    return html


def scraper_saks(url):
    # Get url and him html-code
    base_url = url
    request_to_base_url = requests.get(base_url, headers=headers,
                                       timeout=20)
    bsobj_base_site = BeautifulSoup(request_to_base_url.text,
                                    'html.parser')

    # Get links of products and it index
    for index, item in enumerate(
            bsobj_base_site.findAll(
                'div', {'id': re.compile('^product-([0-9])*$')}
            )):
        # Set default values
        inter_dict['Free Shipping'].append('FALSE')
        inter_dict['Available'].append('TRUE')

        inter_dict['Retailer Name'].append(list(
            bsobj_base_site.find('a',
                                 {'class': 'hbc-header__logo'}).children
        )[0].get_text())
        inter_dict['Main Category'].append(list(
            bsobj_base_site.find('a', {'id': 'bc-306418052'}).children
        )[0].get_text() + ' Shoes')

        # Try get subcategory
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

        # Get link of product
        link = item['data-url']
        print(link)

        # Get image of product
        inter_dict['Image URL'].append(item['data-image'])

        # Get html code of product
        bsobj_product = get_product_url(link)

        inter_dict['URL'].append(link)

        # Get price of products
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

        # Get color
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

        # Try get list of available sizes
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

        # Site don't specifed material
        inter_dict['Material'].append('-')

        # Get title of product
        title = (bsobj_product.find(
                'h1', {'class': 'product-overview__short-description'}
                 ).get_text())
        title = re.sub('[^a-zA-Z0-9-_*.]', '', title)
        inter_dict['Title'].append(title)

        # Get descipritons of product
        if isinstance(bsobj_product.find('div', {'itemprop':
                                                 'description'}
                                         ).contents[0], str):
            descr = (bsobj_product.find(
                     'div', {'itemprop': 'description'})
                     .contents[0])
            descr = re.sub('[^a-zA-Z0-9-_*.]', '', descr)
            inter_dict['Description'].append(descr)
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

        inter_dict['Meta Title'] = inter_dict['Title']
    return inter_dict
