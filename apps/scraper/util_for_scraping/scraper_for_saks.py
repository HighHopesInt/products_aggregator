import re

import requests
from bs4 import BeautifulSoup
from django.contrib import messages

from .meta_data_for_scraping import headers, intermediate_dictionary
from .valutate import get_current_usd


def scraper_saks(request):
    try:
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
            intermediate_dictionary['Free Shipping'].append('False')
            intermediate_dictionary['Available'].append('True')
            intermediate_dictionary['Retailer Name'].append(list(
                bsobj_base_site.find('a',
                                     {'class': 'hbc-header__logo'}).children
            )[0].get_text())
            intermediate_dictionary['Main Category'].append(list(
                bsobj_base_site.find('a', {'id': 'bc-306418052'}).children
            )[0].get_text())
            intermediate_dictionary['Subcategory'].append(
                bsobj_base_site.find(
                    'a', {'id': 'category-306418205'}
                ).get_text().strip())
            intermediate_dictionary['SubSubcategory'].append(
                bsobj_base_site.find(
                    'a', {'id': 'refinement-306420996'}
                ).get_text().strip())
            intermediate_dictionary['Gender'] = \
                [i + ' Gender' for i in intermediate_dictionary
                 ['Main Category']]
            link = item['data-url']
            intermediate_dictionary['Image URL'].append(item['data-image'])
            bsobj_product = get_product_url(link)
            intermediate_dictionary['URL'].append(link)
            price = bsobj_product.find('span', {'itemprop':
                                                re.compile('rice$')}).attrs[
                'content'
            ]
            intermediate_dictionary['Price'].append(price)
            intermediate_dictionary['Price'][index] = int(float(
                intermediate_dictionary['Price'][index])) // int(
                get_current_usd())
            intermediate_dictionary['Color'].append(
                bsobj_product.find('dd', {'class': re.compile('^product-var')}
                                   ).get_text()
            )
            intermediate_dictionary['Sale Price'] = \
                intermediate_dictionary['Price']
            intermediate_dictionary['Brand'].append(bsobj_product.find('a', {
                'class': 'product-overview__brand-link'
            }).get_text())
            size = bsobj_product.find('div', {'product-size-options'}). \
                find('ul', {'class': 'product-variant-attribute-values'})
            size_product = []
            if size:
                for si in size.children:
                    if 'product-variant-attribute-value--unavailable' \
                            not in si.attrs['class']:
                        size_product.append(si.get_text().replace(' M', ''))
            else:
                size_product.append('')
            intermediate_dictionary['Size'].append(size_product)
            intermediate_dictionary['Material'].append(bsobj_product.find(
                'div', {'itemprop': 'description'}
            ).find('ul').find('li').get_text().replace(' upper', ''))
            if isinstance(bsobj_product.find('div', {'itemprop':
                                                     'description'}
                                             ).contents[0], str):
                intermediate_dictionary['Description'].append(
                    bsobj_product.find(
                        'div', {'itemprop': 'description'}
                    ).contents[0])
            else:
                intermediate_dictionary['Description'].append(
                    ' Product ' + str(index) + ' ')
            intermediate_dictionary['Short Description'] = \
                intermediate_dictionary['Description']
            intermediate_dictionary['Meta Description'].append(
                'Buy' + str(intermediate_dictionary['Description'][index]) +
                'on ' + str(intermediate_dictionary['Material'][index]))
            intermediate_dictionary['Title'].append(bsobj_product.find(
                'h1', {'class': 'product-overview__short-description'}
            ).get_text())
            intermediate_dictionary['Meta Title'] = \
                intermediate_dictionary['Title']
            if index == 2:
                break
        return intermediate_dictionary
    except requests.exceptions.Timeout:
        messages.error(request, 'Timeout')
    except AttributeError:
        messages.error(request, ('Scraper was fall. Site can edit structure.'
                                 'Tell that to us'))


def get_product_url(link):
    request_link = requests.get(link, headers=headers, timeout=20)
    html = BeautifulSoup(request_link.text, 'html.parser')
    return html
