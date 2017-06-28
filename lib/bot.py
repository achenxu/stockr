import random
import requests
import bs4
import time
from stockr.lib import utilities

class Stockr():
    def __init__(self, proxy_file_name):
        self.proxies = utilities.get_proxies_from_file(proxy_file_name)

    def get_random_proxy(self):
        return random.choice(self.proxies)

    def get_products(self, domain):
        endpoint = 'https://{0}/sitemap_products_1.xml'.format(domain)
        response = requests.get(endpoint, proxies=self.get_random_proxy())
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        products = []
        for product in soup.find_all('url')[1:]:
            image_element = product.find('image:loc')
            title_element = product.find('image:title')
            products.append({
                'url': product.find('loc').getText(),
                'image': image_element.getText() if image_element else None,
                'title': title_element.getText() if title_element else None
            })
        return products

    def get_diffs(self, old_products, new_products):
        return [product for product in new_products if product not in old_products]

    def run(self, domain):
        old_products = utilities.run_until_complete(target=self.get_products, args=(domain,))
        while True:
            new_products = utilities.run_until_complete(target=self.get_products, args=(domain,))
            diffs = self.get_diffs(old_products, new_products)
            for diff in diffs:
                utilities.log(diff)
            old_products = new_products
            time.sleep(0.01) # Protect against busy waiting if we get an error loop
