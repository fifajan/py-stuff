#! /usr/bin/python

'''
This script should parse mp3 links from 'url'
(worked on xmusic.me on Jan 11 2015) and write them to 'text_file'.

Then you can download those mp3 files using:
$ wget -i <text_file>

(c) 2015 Alexey Ivchenko aka fifajan (fifajan@ukr.net)
'''

from BeautifulSoup import BeautifulSoup
import urllib2
import re

url = 'http://xmusic.me/search/q/LBgWCg/page/'
text_file = open("mp3_links.list", "w")

if __name__ == '__main__':
    urls = [url + str(i) for i in range(1, 6)]

    for u in urls:
        html_page = urllib2.urlopen(u)
        soup = BeautifulSoup(html_page)
        mp3 = [str(l).split('"')[1] for l in (
        	soup.findAll('a', attrs={'href': re.compile("^http://")}))]

        mp3 = [l for l in mp3 if l.endswith('.mp3')]
        text_file.write('\n'.join(mp3))

    text_file.close()
