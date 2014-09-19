import sys
import tweepy
import feedparser
import os
import json
import ConfigParser
from datetime import datetime

cfg = None
localpath = os.path.dirname(os.path.abspath(__file__))
datafile = 'data.dat'
feedurl = 'http://modx.com/feeds/latest.rss'
consumer_key = ''
consumer_secret = ''
token_key = ''
token_secret = ''
configFileName = ''

def doGreeting():
	sys.stderr.write("\x1b[2J\x1b[H")
	greetingStr = ''
	greetingStr += '\nNew MODX Revo Extras Tweeter'
	greetingStr += '\n'
	greetingStr += '\nA simple Python script to tweet when a new MODX Revo extra is released.'
	greetingStr += '\nFor full details see http://freelancewebdev.github.com/New-MODX-Revo-Extra-Py-Tweeter'
	greetingStr += '\n'  
	greetingStr += '\nCopyright (C) ' + str(datetime.now().year) + ' Joe Molloy (info[at]hyper-typer.com)'
	greetingStr += '\nThis script comes with ABSOLUTELY NO WARRANTY.'
	greetingStr += '\nThis is free software, licensed under the GPL V3'
	greetingStr += '\nand you are welcome to redistribute it'
	greetingStr += '\n'
	print greetingStr

def getConfig():
	global configFileName, cfg, consumer_key, consumer_secret, token_key, token_secret
	configFileName = __file__ + '.cfg'
	print '\nChecking configuration data...'
	cfg = ConfigParser.ConfigParser()
	try:
		cfg.read(os.path.join(localpath, configFileName))
	except:
		try:
			os.chmod(os.path.join(localpath,configFileName),0777)
			cfg.read(os.path.join(localpath,configFileName))
		except Exception as e:
			print 'There was a problem reading the config file'
			print 'Please ensure you have renamed'
			print '\'' + configFileName + '_sample\' to \'' + configFileName + '\''
			print 'and added your own values as appropriate'
			sys.exit()
	try:
		consumer_key = cfg.get('twitter','consumer-key')
	except:
		print 'No Twitter consumer key set in config file. Exiting.'
		sys.exit(1)
	try:
		consumer_secret = cfg.get('twitter','consumer-secret')
	except:
		print 'No Twitter consumer secret set in config file. Exiting.'
		sys.exit(1)
	try:
		token_key = cfg.get('twitter','token-key')
	except:
		print 'No Twitter token key set in config file. Exiting.'
		sys.exit(1)
	try:
		token_secret = cfg.get('twitter','token-secret')
	except:
		print 'No Twitter token secret set in config file. Exiting.'
		sys.exit(1)
	print 'Config loaded\n'


def getLatestFeedItem():
	guid = None
	title = None
	try:
		with open(os.path.join(localpath,datafile), 'r') as f:
			try:
				data = json.loads(f.read())
				guid = data['guid']
				title = data['title']
			except:
				pass
	except IOError:

		print 'Data file not created yet'
	feed = feedparser.parse(feedurl)
	item = feed.entries[0]
	if item['guid'] == guid or item['title'] == title:
		print 'No new extras. Quitting.'
		sys.exit(0)
	else:
		message = 'A new #MODX #REVO extra has been published - "'
		message = message + item['title'] +'" by ' + item['author'] + '\n'
		message = message + item['link']
		guid = item['guid']
		title = item['title']
		try:
			with os.fdopen(os.open(os.path.join(localpath,datafile), os.O_WRONLY | os.O_CREAT, 0777), 'w') as f:
				data = {}
				data['title'] = title
				data['guid'] = guid
				dataStr = json.dumps(data)
				f.write(dataStr)
		except IOError:
			print 'Failed to save data'
			sys.exit(0)
		return message

def doTweet(message):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(token_key, token_secret)
	api = tweepy.API(auth)
	try:
		api.update_status(message) 
		print 'Tweet posted'
	except:
		print 'There was a problem'

def main():
	doGreeting()
	getConfig()
	message = getLatestFeedItem()
	doTweet(message)

if __name__ == '__main__':
	main()