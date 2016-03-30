#!/usr/bin/env python
import sys
import urllib2
from BeautifulSoup import BeautifulSoup

def open_url(url):
	try:
		opener = urllib2.build_opener(urllib2.HTTPHandler())
		opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)')]
		request = urllib2.Request(url)
		page = opener.open(request)
		html = page.read()
		return html
	except Exception, e:
		print e
		sys.exit(1)

def get_playlist(parsed_html):
	try:
		playlists = parsed_html.findAll("div", {"data-clip-hls-url": True})

		for playlist in playlists:
			return playlist['data-clip-hls-url']
	except Exception, e:
		print e
		sys.exit(1)

if __name__ == "__main__":
	print "Vidio.com Downloader"

	url = sys.argv[1]

	html = open_url(url)
	parsed_html = BeautifulSoup(html)

	playlist = get_playlist(parsed_html)
	playlist = open_url(playlist)

	print playlist