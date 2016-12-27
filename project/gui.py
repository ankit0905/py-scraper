# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView
from scriptGenerator import ScriptGenerator
import scraper, syntax

class MainWindow(QMainWindow):
    """ The class that defines the structure of the application's GUI.

        The main GUI contains URL Input box, Selector Input box and following 3 tabs:
        1.) Script Tab : Python Script is generated here for required scraping
        2.) Webpage Tab : Displays the website of input URL
        3.) Data Tab : Displays the Scraped Data using Input URL & Selector
    """
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)

        self.menubar = self.menuBar()
        help_ = self.menubar.addMenu("Help")
        aboutAction = QAction("About",self)
        aboutAction.setShortcut("Ctrl+A")
        aboutAction.setToolTip("About Py-Scrapper")
        aboutAction.triggered.connect(self.about)

        contributeAction = QAction("Contribute Or Report Issues",self)
        contributeAction.setShortcut("Ctrl+Shift+C")
        contributeAction.setToolTip("Opens Repository")
        contributeAction.triggered.connect(self.contribute)

        usageAction = QAction("Usage",self)
        usageAction.setShortcut("Ctrl+U")
        usageAction.setToolTip("Instructions for Using the tool")
        usageAction.triggered.connect(self.usage)

        help_.addAction(aboutAction)
        help_.addAction(contributeAction)
        help_.addAction(usageAction)

        self.dialog = QDialog()

        self.statusbar = self.statusBar()

        mainlayout = QVBoxLayout()
        grid = QGridLayout()

        font = QFont("Times",13)
        self.urlLabel = QLabel("Url:")
        self.urlLabel.setFont(font)
        self.urlInput = QLineEdit()
        self.urlInput.setFont(font)
        self.selectorLabel = QLabel("Selector:")
        self.selectorLabel.setFont(font)
        self.selectorInput = QLineEdit()
        self.selectorInput.setFont(font)
        self.button = QPushButton()
        self.button.setFont(font)
        self.button.setText("Scrape It")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.modifyUI)

        grid.addWidget(self.urlLabel,0,0)
        grid.addWidget(self.urlInput,0,1)
        grid.addWidget(self.selectorLabel,1,0)
        grid.addWidget(self.selectorInput,1,1)
        grid.addWidget(self.button,2,1)

        mainlayout.addLayout(grid)

        self.tab = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab.addTab(self.tab1, "1")
        self.tab.addTab(self.tab2,"2")
        self.tab.addTab(self.tab3,"3")

        tab1layout = QVBoxLayout()
        self.scriptBrowser = QTextBrowser()
        self.scriptBrowser.append("")
        self.scriptBrowser.setFont(QFont("Courier",13))
        self.scriptBrowser.setTextColor(QColor("#C5C8C6"))
        self.scriptBrowser.setStyleSheet("background-color: #1d1f21")
        self.scriptBrowser.setText("Python Script will be generated here")
        tab1layout.addWidget(self.scriptBrowser)
        self.tab.setTabText(0,"Python Script")
        self.tab.setFont(font)
        self.tab1.setLayout(tab1layout)

        tab2layout = QVBoxLayout()
        self.web = QWebView()
        tab2layout.addWidget(self.web)
        self.tab.setTabText(1,"Webpage")
        self.tab2.setLayout(tab2layout)

        tab3layout = QVBoxLayout()
        self.dataBrowser = QTextBrowser()
        self.dataBrowser.setFont(QFont("Courier",13))
        self.dataBrowser.setTextColor(QColor("#C5C8C6"))
        self.dataBrowser.append("Scraped Data: \n\n")
        self.dataBrowser.setStyleSheet("background-color: #1d1f21")
        tab3layout.addWidget(self.dataBrowser)
        self.tab.setTabText(2,"Scraping Results")
        self.tab3.setLayout(tab3layout)

        mainlayout.addWidget(self.tab)
        self.dialog.setLayout(mainlayout)
        self.setCentralWidget(self.dialog)
        self.setWindowTitle("Py-Scrapper")

    def about(self):
        """ Defines the action when the about item under help menu is clicked.

            Displays the basic description of Py-Scrapper.
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Py-Scrapper is a GUI tool for scraping data off webpages"+"\nDeveloped Using Python 2.7 and PyQt4.\n")
        info = "Visit the <a href=\"https://github.com/ankit0905/py-scraper\">Source code</a>"
        msg.setInformativeText(info)
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def contribute(self):
        """ Defines the action when Contribute option under help menu is clicked.

            Opens the source code repository.
        """
        link = "https://github.com/ankit0905/py-scraper"
        QDesktopServices.openUrl(QUrl(link))

    def usage(self):
        """ Defines the action when the Usage menu item is clicked.

            Displays a message box showing the instrucions of Usage.
        """
        text = """
        <p>In the URL input box, copy the web address of the webpage you want to scrape.</p>
        <p>Then, type the appropriate selector depending upon the data to be scraped in the selector input box. <i>(See below on how the selector should look like)</i></p>
        <h4>How to Use Selectors</h4>
        <p>The Selector should be a valid CSSSelector. For recursive scraping, follow a hierarchical way.
        <ul><li>&nbsp;&nbsp;Use the '->' symbol to separate different elements.<li>
        <li>&nbsp;&nbsp;Wheneven you want some to scrape sibling elements - write them in '()' separating by comma.</li></ul></p>
        <br/></br>
        <p><b><u>EXAMPLE:</u></b></p>
        <p><i>a.category -> a.subcategory -> div.item -> (p.title, p.description)</i></p>
        <p>This will scrape the text of the paragraphs will class 'title' and 'description' for all the items of each subcategory and category classed links starting with the url given as input.</p>
        """
        details = QMessageBox()
        details.setText(text)
        details.setIcon(QMessageBox.Information)
        details.setWindowTitle("Usage")
        details.exec_()


    def modifyUI(self):
        """ Method to modify UIs for the tabs after scraping.

            First, the required web page is loaded on the webpage tab.
            Second, the python script is generated and stored in script member variable
            Third, scraper instance is created and scraping starts on a separate thread.
            As soon as scraping finishes, the method addScriptAndData() is called.
        """
        url = self.urlInput.text()
        selectors = self.selectorInput.text()
        self.web.load(QUrl(url))
        print "Webpage Loaded \n"

        self.script = ScriptGenerator(url,selectors).generate()

        self.scraper_ = scraper.Scraper(str(url),str(selectors))
        self.connect(self.scraper_,SIGNAL('threadChange'),self.addScriptAndData)
        self.scraper_.start()

    def addScriptAndData(self):
        """ Method which adds the script and scraped data to respective tabs.

            Syntax highlighter instance is created and functionality added to script Tab.
        """
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.dataBrowser.setText(self.scraper_.data.encode('utf-8').decode('utf-8'))
        self.highlight = syntax.PythonHighlighter(self.scriptBrowser.document())
        self.scriptBrowser.setText(self.script)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

# Minor Issue
# display of warning - QFont::setPixelSize: Pixel size <= 0 (0) while application is working
