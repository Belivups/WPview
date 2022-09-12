import requests
import csv
from requests_html import HTMLSession
from datetime import date
s = HTMLSession()
from login import cookies, headers, data, HTMLSession

s.post('https://plugintheme.net/wp-login.php', cookies=cookies, headers=headers, data=data)


# ----------------------------------- Functions -------------------------------------------


def get_products_links(page):
    url = f'https://plugintheme.net/product-category/wordpress-themes/page/{page}/'
    links = []
    r = s.get(url)
    products = r.html.find('.product-title')
    for item in products:
        links.append(item.find('a', first=True).attrs['href'])
    return links


def parse_products(url):
    r = s.get(url)
    title = r.html.find('h1.product-title.entry-title', first=True) .text.strip()
    price = int(2)
    try:
        demo_link = r.html.find('a.grey-link', first=True).attrs['href']
    except AttributeError as err:
        demo_link = "Products Unavailable"

    try:
        download_link = r.html.find('a.red-link', first=True).attrs['href']
    except AttributeError as err:
        download_link = "Download Link Unavailable"

    image = r.html.find('.woocommerce-product-gallery__image a', first=True).attrs['href']

    category = "WordPress Theme"

    sdes = "Very cheap price & Original product !, We Purchase And Download From Original Authors, You’ll Receive Untouched And Unmodified Files, 100% Clean Files & Free From Virus, Unlimited Domain Usage, Free New Version"

    try:
        full_des = r.html.find('#tab-description', first=True)
        ff_des = full_des.text.splitlines()
        f_des = ''.join(ff_des)

    except AttributeError as err:
        f_des = "No Description Given"

    try:
        versions = r.html.find('.product-short-description ul li:nth-child(7) ', first=True)
        version = versions.text
    except AttributeError as err:
        version = "Update Version"

    today = date.today()
    update = today.strftime("%d/%m/%Y")

    product_details = {
        'image': image,
        'title': title,
        'price': price,
        'version': version,
        'demo_link': demo_link,
        'download_link': download_link,
        'update': update,
        'category': category,
        'sdes': sdes,
        'f_des': f_des,
    }
    return product_details


def save_csv(results):
    keys = results[0].keys()

    with open('Products.csv', 'w') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)


def main():
    results = []

    for x in range(1, 2):
        urls = get_products_links(x)
        for url in urls:
            results.append(parse_products(url))
        save_csv(results)


main()