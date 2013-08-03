import webapp2
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os
import urllib2
import re
import logging

jinja_environment = Environment(
                 loader=FileSystemLoader('templates'))


class MainHandler(webapp2.RequestHandler):
    def get(self):

        logging.debug("helloooo")
        request = urllib2.Request("http://www.mygretutor.com/vocabularyGREDifficult.aspx")
        request.add_header('User-Agent', 'Mozilla/5.0')
        req = urllib2.urlopen(request)
        wiki = req.read()
        data = re.findall('<span.*</span>',wiki)
        words = re.findall(r'<b>.*?</b>&nb', data[0])
        meanings = re.findall(r'100%>.*?<', data[0])
        '''
        self.response.out.write(data[0])
        self.response.out.write(words)
        '''

        htmlString = '''
        <!doctype html>
<html lang="en">
  <head>
    <title>JQueries</title>
    <meta charset="utf-8" />

<link rel="stylesheet" type="text/css" href="static/index.css" />
  </head>
  <body>

<div id="wrapper">
<table id="tab">
        <tr>
        <td class="tabdata"><input type="text" class="text" maxlength="1" tabindex="1" /></td>
        <td class="tabdata"><input type="text" class="text" maxlength="1" tabindex="2"/></td>
        </tr>
        <tr>
        <td class="tabdata"></td>
        <td class="tabdata"></td>
        </tr>
        '''


        htmlString = htmlString + '''</table><script type="text/javascript" src="static/index.js"></script></body></html>'''

        '''
        http://wordsmith.org/words/random.cgi
        http://en.wikipedia.org/wiki/Special:Random
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())
        '''
        self.response.out.write(htmlString)

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True
)
