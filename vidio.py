#!/usr/bin/env python
import sys
import urllib2
import m3u8
from BeautifulSoup import BeautifulSoup
import wget

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

def get_playlist_url(parsed_html):
	try:
		playlists = parsed_html.findAll("div", {"data-clip-hls-url": True})

		for playlist in playlists:
			return playlist['data-clip-hls-url']
	except Exception, e:
		print e
		sys.exit(1)

def get_playlist(playlist_url, resolution):
	m3u8_obj = m3u8.load(playlist_url)

	for playlist in m3u8_obj.playlists:
		if str(playlist.stream_info).find(resolution) > 0:
			return playlist.uri

def open_playlist(playlist):
	m3u8_obj = m3u8.load(playlist)
	return m3u8_obj

def download_videos(m3u8_obj):
	base_uri = m3u8_obj._base_uri

	for file in m3u8_obj.files:
		video_url = base_uri + "/" + file
		wget.download(video_url)

if __name__ == "__main__":
	url = sys.argv[1]

	html = open_url(url)
	parsed_html = BeautifulSoup(html)

	playlist_url = get_playlist_url(parsed_html)
	playlist = get_playlist(playlist_url, "360")

	m3u8_obj = open_playlist(playlist)
	download_videos(m3u8_obj)

	print "Download finished. You can now manually merge all the downloaded files."
	