import time
import pandas as pd
from argparse import ArgumentParser
import argparse
import logging
import logging.config
from selenium import webdriver as wd
import selenium
import numpy as np
from schema import SCHEMA
import json
import urllib
import datetime as dt

start = time.time()

DEFAULT_URL = ('https://www.indeed.co.in/cmp/Gartner')

parser = ArgumentParser()
parser.add_argument('-u', '--url',
					help='URL of the company\'s Indeed landing page.',
					default=DEFAULT_URL)
parser.add_argument('-f','--file', default='indeed_ratings.csv',
					help='Output file.')
parser.add_argument('--headless', action='store_true',
                    help='Run Chrome in headless mode.')
parser.add_argument('-l','--limit', default=25,
					action='store', type=int, help='Max reviews to scrape')
parser.add_argument('--start_from_url', action='store_true',
                    help='Start scraping from the passed URL.')
parser.add_argument(
    '--max_date', help='Latest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Indeed reviews ASCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
parser.add_argument(
    '--min_date', help='Earliest review date to scrape.\
    Only use this option with --start_from_url.\
    You also must have sorted Indeed reviews DESCENDING by date.',
    type=lambda s: dt.datetime.strptime(s, "%Y-%m-%d"))
args = parser.parse_args()

if not args.start_from_url and (args.max_date or args.min_date):
    raise Exception(
        'Invalid argument combination:\
        No starting url passed, but max/min date specified.'
    )
elif args.max_date and args.min_date:
    raise Exception(
        'Invalid argument combination:\
        Both min_date and max_date specified.'
    )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(lineno)d\
    :%(filename)s(%(process)d) - %(message)s')
ch.setFormatter(formatter)

logging.getLogger('selenium').setLevel(logging.CRITICAL)
logging.getLogger('selenium').setLevel(logging.CRITICAL)

def scrape(field, review, author):

    def scrape_date(review):
        return review.find_element_by_class_name('cmp-review-date-created').text.strip("'")

    def scrape_emp_title(review):
        return review.find_element_by_class_name('cmp-reviewer').text.strip("'")

    def scrape_location(review):
        try:
            res = review.find_element_by_class_name('cmp-reviewer-job-location').text.strip("'")
        except Exception:
            res = np.nan
    
        return res


    def scrape_rev_title(review):
        return review.find_element_by_class_name('cmp-review-title').text.strip('"')

    def scrape_reviews(review):
        try:
            res = review.find_element_by_class_name(
                'cmp-review-text').text.strip("'")
        except Exception:
            res = np.nan
        return res

    def scrape_overall_rating(review):
        try:
            res = review.find_element_by_class_name('cmp-ratingNumber').text
        except Exception:
            res = np.nan
        return res

    def _scrape_subrating(i):
        try:
            ratings = review.find_element_by_class_name(
                'cmp-rating-expandable')
            subratings = ratings.find_element_by_class_name(
                'cmp-ratings-popup').find_element_by_tag_name('tbody')
            this_one = subratings.find_elements_by_tag_name('tr')[i]
            x = this_one.find_element_by_class_name(
                'cmp-Rating-on').get_attribute('style')
            res = (int(x[x.find(":")+1:x.find("%")]))*0.05
        except Exception:
            res = np.nan
        return res
    
    def scrape_work_life_balance(review):
        return _scrape_subrating(0)

    def scrape_comp_and_benefits(review):
        return _scrape_subrating(1)

    def scrape_job_security(review):
        return _scrape_subrating(2)

    def scrape_senior_management(review):
        return _scrape_subrating(3)

    def scrape_culture_and_values(review):
        return _scrape_subrating(4)

    funcs = [
        scrape_date,
        scrape_emp_title,
        scrape_location,
        scrape_rev_title,
        scrape_reviews,
        scrape_overall_rating,
        scrape_work_life_balance,
        scrape_comp_and_benefits,
        scrape_job_security,
        scrape_senior_management,
        scrape_culture_and_values
        ]

    fdict = dict((s, f) for (s, f) in zip(SCHEMA, funcs))

    return fdict[field](review)


def extract_from_page():

    def is_featured(review):
        try:
            review.find_element_by_class_name('cmp-review-featured-container')
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def extract_review(review):
        author = review.find_element_by_class_name('cmp-reviewer-job-title')
        res = {}
        # import pdb;pdb.set_trace()
        for field in SCHEMA:
            res[field] = scrape(field, review, author)

        assert set(res.keys()) == set(SCHEMA)
        return res

    logger.info(f'Extracting reviews from page {page[0]}')

    res = pd.DataFrame([], columns=SCHEMA)

    reviews = browser.find_elements_by_class_name('cmp-review-container')

    if(len(reviews) == 0):
        logger.info('No more Review!')
        date_limit_reached[0] = True

    logger.info(f'Found {len(reviews)} reviews on page {page[0]}')

    for review in reviews:
        if not is_featured(review):
            data = extract_review(review)
            logger.info(f'Scraped data for "{data["review_title"]}"\
({data["date"]})')
            res.loc[idx[0]] = data
        else:
            logger.info('Discarding a featured review')
        idx[0] = idx[0] + 1

    if args.max_date and \
        (pd.to_datetime(res['date']).max() > args.max_date) or \
            args.min_date and \
            (pd.to_datetime(res['date']).min() < args.min_date):
        logger.info('Date limit reached, ending process')
        date_limit_reached[0] = True

    return res

def more_pages():
    try:
        browser.find_element_by_class_name(
            'cmp-Pagination-link.cmp-Pagination-link--nav')
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False

def go_to_next_page():
    logger.info(f'Going to page {page[0] + 1}')
    next_ = browser.find_element_by_class_name(
        'cmp-Pagination-link.cmp-Pagination-link--nav')
    browser.get(next_.get_attribute('href'))
    time.sleep(1)
    page[0] = page[0] + 1


def no_reviews():
    return False

def navigate_to_reviews():
    logger.info('Navigating to company reviews')

    browser.get(args.url)
    time.sleep(1)

    if no_reviews():
        logger.info('No reviews to scrape. Bailing!')
        return False

    reviews_cell = browser.find_element_by_xpath(
        '//*[@id="cmp-skip-header-desktop"]/ul/li[3]/a')
    reviews_path = reviews_cell.get_attribute('href')
    browser.get(reviews_path)
    time.sleep(1)

    return True

def get_browser():
    logger.info('Configuring browser')
    chrome_options = wd.ChromeOptions()
    if args.headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    browser = wd.Chrome(options=chrome_options)
    return browser


def get_current_page():
    logger.info('Getting current page number')
    paging_control = browser.find_element_by_class_name(
        'cmp-Pagination-link cmp-Pagination-link--current')
    current = int(paging_control.text.replace(',', ''))
    return current


def verify_date_sorting():
    logger.info('Date limit specified, verifying date sorting')
    ascending = urllib.parse.parse_qs(
        args.url)['sort.ascending'] == ['true']

    if args.min_date and ascending:
        raise Exception(
            'min_date required reviews to be sorted DESCENDING by date.')
    elif args.max_date and not ascending:
        raise Exception(
            'max_date requires reviews to be sorted ASCENDING by date.')


browser = get_browser()
page = [1]
idx = [0]
date_limit_reached = [False]


def main():

    logger.info(f'Scraping up to {args.limit} reviews.')

    res = pd.DataFrame([], columns=SCHEMA)


    if not args.start_from_url:
        reviews_exist = navigate_to_reviews()
        if not reviews_exist:
            return
    elif args.max_date or args.min_date:
        verify_date_sorting()
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)
    else:
        browser.get(args.url)
        page[0] = get_current_page()
        logger.info(f'Starting from page {page[0]:,}.')
        time.sleep(1)

    reviews_df = extract_from_page()
    res = res.append(reviews_df)

    # import pdb;pdb.set_trace()

    while more_pages() and\
            len(res) < args.limit and\
            not date_limit_reached[0]:
        go_to_next_page()
        reviews_df = extract_from_page()
        res = res.append(reviews_df)

    logger.info(f'Writing {len(res)} reviews to file {args.file}')
    res.to_csv(args.file, index=False, encoding='utf-8')

    end = time.time()
    logger.info(f'Finished in {end - start} seconds')


if __name__ == '__main__':
    main()
