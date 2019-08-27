import re

import requests
from bs4 import BeautifulSoup

from .meta_data_for_scraping import headers, intermediate_dictionary
from .valutate import get_current_usd


def scraper_saks():
    base_url = ('https://www.saksfifthavenue.com'
                '/Men/Shoes/Boots/shop/_/N-52fnyc/Ne-6lvnb5')
    request_to_base_url = requests.get(base_url, headers=headers,
                                       timeout=20)
    bsobj_base_site = BeautifulSoup(request_to_base_url.text,
                                    'html.parser')
    for index, item in enumerate(
            bsobj_base_site.findAll(
                'div', {'id': re.compile('^product-([0-9])*$')}
            )):
        intermediate_dictionary['Free Shipping'].append('FALSE')
        intermediate_dictionary['Available'].append('TRUE')
        intermediate_dictionary['Retailer Name'].append(list(
            bsobj_base_site.find('a',
                                 {'class': 'hbc-header__logo'}).children
        )[0].get_text())
        intermediate_dictionary['Main Category'].append(list(
            bsobj_base_site.find('a', {'id': 'bc-306418052'}).children
        )[0].get_text() + ' Shoes')
        intermediate_dictionary['Subcategory'].append(
            bsobj_base_site.find(
                'a', {'id': 'category-306418205'}
            ).get_text().strip())
        intermediate_dictionary['SubSubcategory'].append(
            bsobj_base_site.find(
                'a', {'id': 'refinement-306420996'}
            ).get_text().strip())
        intermediate_dictionary['Gender'].append(list(
            bsobj_base_site.find('a', {'id': 'bc-306418052'}).children
        )[0].get_text())
        link = item['data-url']
        print(link)
        intermediate_dictionary['Image URL'].append(item['data-image'])
        bsobj_product = get_product_url(link)
        intermediate_dictionary['URL'].append(link)
        price = bsobj_product.find('span', {'itemprop':
                                            re.compile('[P|p]rice$')})
        if price:
            price = price.attrs['content']

            intermediate_dictionary['Price'].append(price)
            intermediate_dictionary['Price'][index] = int(float(
                intermediate_dictionary['Price'][index])) // int(
                get_current_usd())
        else:
            intermediate_dictionary['Price'].append('')
        color = bsobj_product.find('dd', {'class': re.compile('^product-var')})
        if color:
            intermediate_dictionary['Color'].append(color.get_text())
        else:
            intermediate_dictionary['Color'].append('')
        intermediate_dictionary['Sale Price'] = \
            intermediate_dictionary['Price']
        intermediate_dictionary['Brand'].append(bsobj_product.find('a', {
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
        intermediate_dictionary['Size'].append(size_product)
        intermediate_dictionary['Material'].append(bsobj_product.find(
            'div', {'itemprop': 'description'}
        ).find('ul').find('li').get_text().replace(' upper', ''))
        intermediate_dictionary['Title'].append(bsobj_product.find(
            'h1', {'class': 'product-overview__short-description'}
        ).get_text())
        if isinstance(bsobj_product.find('div', {'itemprop':
                                                 'description'}
                                         ).contents[0], str):
            intermediate_dictionary['Description'].append(
                bsobj_product.find(
                    'div', {'itemprop': 'description'}
                ).contents[0])
        else:
            intermediate_dictionary['Description'].append(
             'Product ' + intermediate_dictionary['Title'][index] + ' by ' +
             intermediate_dictionary['Brand'][index]
            )
        intermediate_dictionary['Short Description'].append(
            'Product ' + intermediate_dictionary['Title'][index] + ' by ' +
            intermediate_dictionary['Brand'][index] + ' in ' +
            intermediate_dictionary['Color'][index]
        )
        intermediate_dictionary['Meta Description'].append(
            'Buy' + str(intermediate_dictionary['Description'][index]) +
            'on ' + str(intermediate_dictionary['Material'][index]))
        intermediate_dictionary['Meta Title'] = \
            intermediate_dictionary['Title']
    return intermediate_dictionary


def get_product_url(link):
    request_link = requests.get(link, headers=headers, timeout=20)
    html = BeautifulSoup(request_link.text, 'html.parser')
    return html
