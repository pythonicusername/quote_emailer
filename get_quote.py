# get_quote.py - Opens quote website and returns the quote
import requests
import bs4
import configparser
from pathlib import Path


class Application:
    def __init__(self, url, selector):
        self.url = url
        self.selector = selector

    def get_a_quote(self):
        try:
            res = requests.get(self.url)
            try:
                res.raise_for_status()
                try:
                    soup = bs4.BeautifulSoup(res.text, 'html.parser')
                    element = soup.select(self.selector)
                    return element[0].text.strip()
                except Exception as selector_exc:
                    print(f'There was a problem with the CSS Selector: {selector_exc}')
            except Exception as get_exc:
                print(f'There was a problem loading the page: {get_exc}')
        except Exception as url_exc:
            print(f'There was a problem with the URL: {url_exc}')


def start():
    if __name__ == '__main__':
        print(Application.get_a_quote(website))
    else:
        return Application.get_a_quote(website)


config_path = Path(__file__).parent / "../quote_emailer/config.ini"
config = configparser.ConfigParser()
config.read_file(open(config_path))
website = Application(config.get('website', 'url'), config.get('website', 'selector'))
start()
