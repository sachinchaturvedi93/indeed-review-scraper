# Citation
This is based on [MatthewChatham's Glassdoor Review Scraper](https://github.com/MatthewChatham/glassdoor-review-scraper)

# Installation
First, make sure that you're using Python 3.

1. Clone or download this repository.
2. Run `pip install -r requirements.txt` inside this repo. Consider doing this inside of a Python virtual environment.
3. Install [Chromedriver](http://chromedriver.chromium.org/) in the working directory.

# Usage
```
usage: main.py [-h] [-u URL] [-f FILE] [--headless] [--username USERNAME]
               [-p PASSWORD] [-c CREDENTIALS] [-l LIMIT] [--start_from_url] 
               [--max_date MAX_DATE] [--min_date MIN_DATE]

optional arguments:
  -h, --help                                  show this help message and exit
  -u URL, --url URL                           URL of the company's Indeed landing page.
  -f FILE, --file FILE                        Output file.
  --headless                                  Run Chrome in headless mode.
  --username USERNAME                         Email address used to sign in to GD.
  -p PASSWORD, --password PASSWORD            Password to sign in to GD.
  -c CREDENTIALS, --credentials CREDENTIALS   Credentials file
  -l LIMIT, --limit LIMIT                     Max reviews to scrape
  --start_from_url                            Start scraping from the passed URL.
  
  --max_date MAX_DATE                         Latest review date to scrape. Only use this option
                                              with --start_from_url. You also must have sorted
                                              Indeed reviews ASCENDING by date.
                                              
  --min_date MIN_DATE                         Earliest review date to scrape. Only use this option
                                              with --start_from_url. You also must have sorted
                                              Indeed reviews DESCENDING by date.
```

Run the script as follows, taking Commonwealth-Bank as an example. You can pass `--headless` to prevent the Chrome window from being visible, and the `--limit` option will limit how many reviews get scraped. The`-f` option specifies the output file, which defaults to `indeed_reviews.csv`.  

### Example 1
Suppose you want to get the top 1,000 most popular reviews for Commonwealth-Bank. Run the command as follows:

`python main.py --headless --url "python main.py --headless --url "https://au.indeed.com/cmp/Commonwealth-Bank/" --limit 1000 -f commonwealthbank_reviews.csv" --limit 1000 -f wells_fargo_reviews.csv`

**Note**: To be safe, always surround the URL with quotes. This only matters in the presence of a query string.

