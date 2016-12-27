# py-scraper

A GUI tool for web-scraping which scrapes the required webpage recursively using CSS Selectors.

## Installation Instructions For Linux

Firstly, python (mostly pre-installed) and pip must be installed.  
To install pip, type the following on terminal.

```
   $ sudo apt-get update  
   $ sudo apt-get install python-pip
```  
Then, install PyQt4 using the following:

```
   $ sudo apt-get update  
   $ sudo apt-get install python-qt4
```  
Finally, install the other dependencies from requirements.txt:

```
   $ sudo pip install -r requirements.txt
```

## Usage
Firstly to launch the application, do the following 
```
   $ cd /path to folder py-scrapper/project
   $ python gui.py
```
[![app-sample.png](https://s24.postimg.org/5y0psfv11/app_sample.png)](https://postimg.org/image/byyepihn5/)   

In the Url and Selector Input Boxes, copy the web address of the webpage and the appropriate Selector
depending on your scraping requirements. *(Check out the preview shown above)*

#### Using Selectors
The selector must be a valid CSS Selector. For recursive scraping, use the hierarchical way:  

* Use the '->' symbol to separate different elements.
* Wheneven you want some to scrape sibling elements - write them in '()' separating by comma.

**Example**  

To scrape the text of the paragraphs with class *'title'* and *'description'* for all the items of each 
subcategory and category classed links starting with the url given as input, the selector will look something
like as given below:

       a.category -> a.subcategory -> div.item -> (p.title, p.description)

You can also refer to the screenshot above for another example.  

**NOTE:** Once installed, you can check out the Help menu for any help.

