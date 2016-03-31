#!/usr/bin/env python

import getopt
import sys
import urllib2
import m3u8
from BeautifulSoup import BeautifulSoup
import wget

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hFf:")
	except Exception, e:
		usage
		sys.exit()

	url = args[0]
	fmt = 360

	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt == '-F':
			list_formats(url)
			sys.exit()
		elif opt == '-f':
			fmt = arg

	html = open_url(url)
	parsed_html = BeautifulSoup(html)

	playlist_url = get_playlist_url(parsed_html)
	playlist = get_playlist(playlist_url, fmt)

	m3u8_obj = open_playlist(playlist)
	download_videos(m3u8_obj)

	print "Download finished. You can now manually merge all the downloaded files."

def usage():
	print 'Usage: vidio.py [VIDIO URL]'

def open_url(url):
	print '[log] downloading webpage'
	opener = urllib2.build_opener(urllib2.HTTPHandler())
	opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)')]
	request = urllib2.Request(url)
	page = opener.open(request)
	html = page.read()
	return html

def get_playlist_url(parsed_html):
	playlists = parsed_html.findAll("div", {"data-clip-hls-url": True})

	for playlist in playlists:
		return playlist['data-clip-hls-url']

def get_playlist(playlist_url, fmt):
	m3u8_obj = m3u8.load(playlist_url)

	for playlist in m3u8_obj.playlists:
		if str(playlist.stream_info.resolution).find(fmt) > 0:
			return playlist.uri

	return None

def open_playlist(playlist):
	m3u8_obj = m3u8.load(playlist)
	return m3u8_obj

def download_videos(m3u8_obj):
	print '[log] downloading videos'
	base_uri = m3u8_obj._base_uri

	for file in m3u8_obj.files:
		video_url = base_uri + "/" + file
		wget.download(video_url)

def list_formats(url):
	html = open_url(url)
	parsed_html = BeautifulSoup(html)

	playlist_url = get_playlist_url(parsed_html)
	m3u8_obj = m3u8.load(playlist_url)

	for playlist in m3u8_obj.playlists:
		print playlist.stream_info.resolution

if __name__ == "__main__":
	try:
		main(sys.argv[1:])
	except Exception, e:
		print e
		sys.exit()
