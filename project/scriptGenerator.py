class ScriptGenerator():
    """ Generate python script to scrape given selector.

        Selector : must follow proper format of a CSS Selector
    """
    def __init__(self, url, selector):
        self.CSSSelector = selector
        self.url = url

    def generate(self):
        """ Script Generating function.

            Returns the script as a string.
        """
        script = r'''
from bs4 import BeautifulSoup
import requests

def parse(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    element = soup.select("{0}")

def main():
    parse("{1}")

if __name__=='__main__':
    main()
                 '''.format(self.CSSSelector,self.url)
        return script.lstrip().rstrip()

#scr = ScriptGenerator("https://www.google.com","title")
#scr.generate()
