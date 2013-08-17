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
        for i in range(0,len(words)):
            words[i] = words[i][3:-7]
            meanings[i] = meanings[i][5:-1]

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

        table = []        # contains list of (x, y, letter)
        word_counter = 1  # current word being searched/appended
        hints = []        # contains list of (word's index in words[], x, y, across/down). Used to remember where a word starts

        # Adding the first word
        hints.append([1,0,0,0])        #  [word count, x, y, across/down]

        for i in range(0, len(words[word_counter])):
            table.append([i,0,words[word_counter][i]])

        word_counter+=1
        flag = 0
        for i in range(0,len(words)):
            for j in range(0,len(words[word_counter])):
                if words[i].count(words[word_counter][j])>0:
                    flag = 1
                    break
                    index_of_old_word = words[i].index(words[word_counter][j])
                    index_of_new_word = j
                    matched_word_counter = i
                    # match found. Check for placement of word

        if flag==1:
            self.response.out.write("FOUNDDD")
            self.response.out.write(words[i].index(words[word_counter][j]))

        self.response.out.write(words[word_counter])
        self.response.out.write('|')
        self.response.out.write(words[i])

        htmlString = htmlString + '''</table><script type="text/javascript" src="static/index.js"></script></body></html>'''

        '''
        http://wordsmith.org/words/random.cgi
        http://en.wikipedia.org/wiki/Special:Random
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())
        '''
        #       self.response.out.write(htmlString)

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True
)
