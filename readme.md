#New MODX Revo Extras Python Tweeter
A simple Python script which, in combination with a scheduler like cron, will tweet about new PHP CMS/CMF MODX extras when they are released.

##Instructions
You may need to install the feedparser and tweepy modules.

```
pip install feedparser
```

```
pip install tweepy
```

Set up your [Twitter application and obtain your consumer key, consumer secret, token key and secret](https://dev.twitter.com).

Make a copy of modx_latest_extras_tweets.py.cfg.sample and save as modx_latest_extras_tweets.py.cfg

Add your keys and secrets as obtained above where indicated in the modx_latest_extras_tweets.py.cfg file you just created

Finally run 

```
python modx_latest_extras_tweets.py
```
