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

        table = []        # contains 2D array of the puzzle
        word_counter = 1  # current word being searched/appended
        hints = []        # contains list of (word's index in words[], x, y, across/down). Used to remember where a word starts

        # Adding the first word
        hints.append([1,0,0,0])        #  [word count, x, y, across/down]


        table = insertLetter(table, 0, 0, 0, words[1])

        self.response.out.write(words[word_counter])
        self.response.out.write('|')
        self.response.out.write(words[i])
        self.response.out.write('|')
        self.response.out.write(table)
        self.response.out.write(createHtmlTable(table))

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


#
#  Adds a word to the crossword assuming that letter
#  overlaps have already been checked
#

def insertLetter(table, x, y, vert, word):

    # Adding horizontal word
    if vert == 0:

        #column not created
        if len(table) < x+len(word):

            # creating empty coulmns
            reqd = len(word)
            for i in range(0,len(word)):
                table.append([])


        # appending letters to the table
        for i in range(0,len(word)):
            table[x+i].append([y, word[i]])

    # Adding vertical word
    else:
        # appending letters to the table
        for i in range(0,len(word)):
            table[x].append([y-1, word[i]])

    return table


def createHtmlTable(table):

    # finding number of rows
    max = 0
    for i in range(0, len(table)-1):
        for j in range(0,len(table[i])-1):
            if table[i][j][0] > max:
                max = table[i][j][0]


    # Adding black blocks
    html_table = []
    for x in range(0, len(table)-1):
        html_table.append([])
        for y in range(0,max):
            html_table[x].append('<td class="tabdata" style="background:black;"></td>')

    # Adding white blocks
    for x in range(0, len(table)-1):
        temp_len = len(table[x])-1
        for y in range(0,temp_len):
            html_table[x][max - table[x][y][0]] = '<td class="tabdata"><input type="text" class="text" maxlength="1" tabindex="1" /></td>'

    # creating html string
    html_string = '<table id="tab">'

    for x in range(0, len(table)-1):
        html_string = html_string + '<tr>'
        for y in range(0,max):
            html_string = html_string + html_table[x][y]
        html_string = html_string + '</tr>'
    html_string = html_string + '</table>'

    return html_string
