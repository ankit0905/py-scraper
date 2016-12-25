class ScriptGenerator():
    """ Generate python script to scrape given selector.

        url      : link of the webpage to be scraped
        selector : must follow proper format of a CSS Selector
    """
    def __init__(self, url, selector):
        self.CSSSelector = selector
        self.url = url

    def generate(self):
        """ Returns the python script as string.
        """
        script = r"""
from bs4 import BeautifulSoup
import requests
from urlparse import urljoin

def modify(selector):
    selector = selector.split('->')
    for i in range(len(selector)):
        selector[i] = selector[i].lstrip().rstrip()
    return selector

def parse(url, selectors):
    try:
        r = requests.get(url)
    except:
        print "Connection failed"
        return
    page = BeautifulSoup(r.content,"html.parser")
    scrape(url,page,0,len(selectors)-1,selectors)

def scrape(url, soup, index, hi, selectors):
    if index > hi:
        text = soup.get_text()
        text = str(text.encode("utf-8"))
        print text.lstrip().rstrip()
        return
    elif index != hi and selectors[index].startswith("a."):
        elements = soup.select(selectors[index])
        for ele in elements:
            href = ele.get("href")
            new_url = urljoin(url,href)
            try:
                req = requests.get(new_url)
            except:
                print "Connection failed"
                return
            new_soup = BeautifulSoup(req.content,"html.parser")
            scrape(new_url,new_soup,index+1,hi,selectors)
    else:
        if selectors[index].startswith("("):
            lis = selectors[index]
            lis = lis[1:len(lis)-1]
            lis = lis.split(",")
            for it in range(0,len(lis)):
                lis[it] = lis[it].lstrip().rstrip()
            for selector in lis:
                new_soup = soup.select(selector)
                for it in range(len(new_soup)):
                    scrape(url,new_soup[it],index+1,hi,selectors)
            print "\n"
        else:
            new_soup = soup.select(selectors[index])
            for it in range(len(new_soup)):
                scrape(url,new_soup[it],index+1,hi,selectors)

def main():
    inputUrl = "{0}"
    inputSelector = "{1}"
    modifiedSelector = modify(inputSelector)
    parse(inputUrl, modifiedSelector)


if __name__=='__main__':
    main()
                 """.format(self.url,self.CSSSelector)
        return script.lstrip().rstrip()
