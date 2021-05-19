import os

import pandas as pd
import pickle

from scraping import SephoraScraper

# System path to chrome webdriver and urls to scrape
PATH = 'C:/WebDrivers/chromedriver.exe'

TO_SCRAPE = ['https://www.sephora.com/shop/moisturizer-skincare', 
            'https://www.sephora.com/shop/facial-toner-skin-toner',
            'https://www.sephora.com/shop/facial-treatment-masks',
            'https://www.sephora.com/shop/exfoliating-scrub-exfoliator']

LINKS_PATH = '../data/product_links.csv'

def download_data(checkpoint=''):
    if checkpoint:
        with open(checkpoint, 'rb') as pickle_file:
            scraper = pickle.load(pickle_file)
    else:
        scraper = SephoraScraper(driver_path=PATH)
        if os.path.isfile(LINKS_PATH):
            links = pd.read_csv(LINKS_PATH, sep='\t')['links'].to_list()
        else:
            links = scraper.scrape_links(TO_SCRAPE)

    scraper.scrape_products_and_reviews(num_pages_reviews=2, product_links=links, checkpoint_after=2)
    scraper.save_products_as_csv('../data/products.csv')
    scraper.save_ratings_as_csv('..data/ratings.csv')

def remove_nicknames(ratings):
    ratings['buyer_id'] = pd.factorize(ratings['buyer_nickname'])[0]
    ratings = ratings.drop(['buyer_nickname'], axis=1)
    return ratings


download_data()