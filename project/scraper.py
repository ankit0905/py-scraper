import requests
from bs4 import BeautifulSoup
import urlparse

class Scraper:
    """ Class for scraping webpages

        url       : starting link for scraping
        selectors : user input of selectors
        data      : string that stores the scraped data
    """
    def __init__(self,link,selectors):
        self.url = link
        self.CSSSelectors = selectors
        self.data = ""

    def parse(self):
        """ Parses the Website url.

            Website content is requested, BeautifulSoup object is created and then
            scrape() function is called for required scraping.
        """
        try:
            r = requests.get(self.url,timeout=5)
        except:
            self.data = "Connection Refused - Could not Scrape"
            print "Connection Refused"
            return
        page = BeautifulSoup(r.content, "html.parser")
        self.modify()
        self.scrape(self.url,page,0,len(self.CSSSelectors)-1,self.CSSSelectors)

    def modify(self):
        """ Modifies the string selector and converts it into list of selectors
        """
        selectors = self.CSSSelectors.split('->')
        for it in range(len(selectors)):
            selectors[it] = selectors[it].lstrip().rstrip()
        self.CSSSelectors = selectors

    def scrape(self,url,soup,index,hi,selectors):
        """ Recursively scrapes the webpage as per the given input.

            url       : current url being scraped
            soup      : current BeautifulSoup object being operated on
            index     : current index of the list of selectors
            hi        : highest index of the list of selectors
            selectors : the actual list of selectors (created from user input)
        """
        if index > hi:
            text = soup.get_text()
            text = str(text.encode('utf-8'))
            self.data += text.lstrip().rstrip()+'\n'
            return
        elif index != hi and selectors[index].startswith('a.'):
            elements = soup.select(selectors[index])
            for ele in elements:
                href = ele.get('href')
                print href
                new_url = urlparse.urljoin(url,href)
                try:
                    req = requests.get(new_url,timeout=5)
                except:
                    self.data = "Connection Refused - Could not Scrape"
                    print "Connection Refused"
                    return
                new_soup = BeautifulSoup(req.content,"html.parser")
                self.scrape(new_url,new_soup,index+1,hi,selectors)
        else:
            if selectors[index].startswith('('):
                lis = selectors[index]
                lis = lis[1:len(lis)-1]
                lis = lis.split(',')
                for it in range(0,len(lis)):
                    lis[it] = lis[it].lstrip().rstrip()
                for selector in lis:
                    new_soup = soup.select(selector)
                    for it in range(len(new_soup)):
                        self.scrape(url,new_soup[it],index+1,hi,selectors)
                self.data += '\n\n'
            else:
                new_soup = soup.select(selectors[index])
                for it in range(len(new_soup)):
                    self.scrape(url,new_soup[it],index+1,hi,selectors)

#TEST CASE (success)
#inp = "a.organization-card__link -> (h3.banner__title,li.organization__tag--technology)"
#link = "https://summerofcode.withgoogle.com/archive/2016/organizations/"
#scraper = Scraper(link,inp)
#scraper.parse()
#print scraper.data

#ISSUES
#Gui sometimes goes to non-responding mode while scraping is done
#Can be solved by introducing threads
