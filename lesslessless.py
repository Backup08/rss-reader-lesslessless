import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from newspaper import Article
import sys
import os
import feedparser

class web_browser(QWidget):

    def __init__(self, parent = None):
        super(web_browser, self).__init__(parent)
        self.createLayout()
        self.createConnection()

        self.lastUrl = ""

    def loadUrl(self,url):
        self.url = url
        self.getRss(self.url)

    def getRss(self, url):       
        d = feedparser.parse(url) 

        os.system("rm -r /tmp/rss.html")
        with open('/tmp/rss.html', 'a') as the_file:
            the_file.write('<!DOCTYPE html><html><head><meta')
            the_file.write('charset="utf-8"><meta')
            the_file.write('name="viewport" content="width=device-width, initial-scale=1"><title>' +  d['feed']['title'] + '</')
            the_file.write('title><style type="text/css">body{margin:40px auto;')
            the_file.write('max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0')
            the_file.write('10px}h1,h2,h3{line-height:1.2}a{text-decoration: none; color:black;};</style></head><body><!-- RSS Feed --><header><h1>') 
            the_file.write( d['feed']['title'] + '</h1>')
            #the_file.write('<aside>' + '-' + '</aside>')
            the_file.write('</header><hr noshade>')
            the_file.write('<p>')
            
            for post in d.entries:
                the_file.write('<a href="' + post.link.encode('ascii', 'ignore') + '">' + post.title.encode('ascii', 'ignore') + "</a><br><br>")


            the_file.write('</p>')
            the_file.write('</body>')

            url = QUrl( 'file:///' + 'tmp' + '/rss.html' )
            self.webView.load(url)      


    def loadPage(self, url):
        
        article = Article(url)
        article.download()
        article.parse()

        article.text = article.text.replace("\n","<br>")
        
        authors = ""
        for author in article.authors:
            authors = authors + author + ' ' 
            
        os.system("rm -r /tmp/somefile.html")
        with open('/tmp/somefile.html', 'a') as the_file:
            the_file.write('<!DOCTYPE html><html><head><meta')
            the_file.write('charset="utf-8"><meta')
            the_file.write('name="viewport" content="width=device-width, initial-scale=1"><title>' + article.title.encode('ascii', 'ignore') + '</')
            the_file.write('title><style type="text/css">body{margin:40px auto;')
            the_file.write('max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0')
            the_file.write('10px}h1,h2,h3{line-height:1.2}</style></head><body><header><h1>') 
            the_file.write( article.title.encode('ascii', 'ignore')  + '</h1>')
            the_file.write('<aside>' + str(authors) + '</aside>')
            the_file.write('</header><br />')
            the_file.write('<img src="'+ article.top_image + '" width="100%">')
            the_file.write('<p>' + article.text.encode('ascii', 'ignore') + '</p>')
            the_file.write('</body>')
        
            url = QUrl( 'file:///' + 'tmp' + '/somefile.html' )
            self.webView.load(url)     

    def loadSummaryPage(self, url):
        
        article = Article(url)
        article.download()
        article.parse()

        article.nlp()
        article.text = article.summary
        
        article.text = article.text.replace("\n","<br>")
        
        authors = ""
        for author in article.authors:
            authors = authors + author + ' ' 
            
        os.system("rm -r /tmp/somefile.html")
        with open('/tmp/somefile.html', 'a') as the_file:
            the_file.write('<!DOCTYPE html><html><head><meta')
            the_file.write('charset="utf-8"><meta')
            the_file.write('name="viewport" content="width=device-width, initial-scale=1"><title>' + article.title.encode('ascii', 'ignore') + '</')
            the_file.write('title><style type="text/css">body{margin:40px auto;')
            the_file.write('max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0')
            the_file.write('10px}h1,h2,h3{line-height:1.2}</style></head><body><header><h1>') 
            the_file.write( article.title.encode('ascii', 'ignore')  + '</h1>')
            the_file.write('<aside>' + str(authors) + '</aside>')
            the_file.write('</header><br />')
            the_file.write('<img src="'+ article.top_image + '" width="100%">')


            the_file.write('<p><strong>Keywords: </strong><i>')
            for i in range(0,5):
				the_file.write( str(article.keywords[i]) + ', ')
            the_file.write( str(article.keywords[6]) )
            the_file.write('</i></p>')
            the_file.write('<p>' + article.text.encode('ascii', 'ignore') + '</p>')
            the_file.write('</body>')
        
            url = QUrl( 'file:///' + '/tmp/' + '/somefile.html' )
            self.webView.load(url)     


    def search(self):
        address = str(self.addressBar.text())        
        url = address

        if "feedburner.com" in url or "rss" in url:
            self.getRss(url)
        else:
            self.loadPage(url)

            
    def back(self):
        url = QUrl( 'file:///' + 'tmp' + '/rss.html' )
        self.webView.load(url)      

    def summary(self):
        self.loadSummaryPage(self.lastUrl)
        url = QUrl( 'file:///' + '/tmp' + '/somefile.html' )
        self.webView.load(url)      

    def next(self):
        page = self.webView.page()
        history = page.history()
        history.forward()

    def createLayout(self):
        self.setWindowTitle('News Reader')
        self.addressBar = QLineEdit()

        self.backButton = QPushButton('')
        self.summaryButton = QPushButton('')

        self.summaryButton.setIcon(QtGui.QIcon('/usr/share/icons/mate/scalable/actions/edit-cut-symbolic.svg'))
        self.backButton.setIcon(QtGui.QIcon('/usr/share/icons/mate/scalable/actions/go-previous-symbolic.svg'))

        bl = QHBoxLayout()
        bl.addWidget(self.backButton)
        bl.addWidget(self.summaryButton)

        self.webView = QWebView()
        self.webView.titleChanged.connect(self.adjustTitle)
        
        layout = QVBoxLayout()
        layout.addLayout(bl)
        layout.addWidget(self.webView)
        layout.setContentsMargins(1,5,1,1)
        self.setLayout(layout)
        self.showMaximized()

    def createConnection(self):
        self.addressBar.returnPressed.connect(self.search)
        self.addressBar.returnPressed.connect(self.addressBar.selectAll)

        self.backButton.clicked.connect(self.back)
        self.summaryButton.clicked.connect(self.summary)

    def adjustTitle(self):
        url = str(self.webView.url().toString())
        
        if "rss.html" in url:
            doNothing = True
            self.summaryButton.setDisabled(True)
        else:    
            if "http" in url:
                self.summaryButton.setDisabled(False)
                self.loadPage(url)
                self.lastUrl = url
            
app = QApplication(sys.argv)
browser = web_browser()
browser.loadUrl(sys.argv[1])
browser.show()
sys.exit(app.exec_())
