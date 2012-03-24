import time
import datetime
import logging
from threading import Thread
from TweetStorage import Tweet
from TweetStorage import TweetStorage
import urllib
from xml.etree import ElementTree

__author__="Jiri Chadima"
__date__ = "$Mar 7, 2011 10:45:46 AM$"

BASE_URL = "http://api.twitter.com/1/statuses/user_timeline.rss"
PARAM = "?screen_name="
RSS_BASE_LINK = BASE_URL + PARAM
REFRESH_TIME = 60


class TwitterClient(Thread):
    """Main communication class that takes care of checking and updating twitter
    status feed."""
    def __init__(self, uname):
        """Inits thread, storage and basic data structures."""
        Thread.__init__(self)
        self.halt = False
        self.username = uname
        self.rssLink = RSS_BASE_LINK + self.username
        self.storage = TweetStorage()
        self.daemon = True

    def run(self):
        """Pseudo-infinite loop checking RSS each REFRESH_TIME"""
        while not self.halt:
            self.refresh_rss()
            time.sleep(REFRESH_TIME)

    def stop(self):
        """Stops refreshing loop"""
        self.halt = True
        logging.info("Stopping twitter client...")

    def refresh_rss(self):
        """Refreshes feed from twitter and tries to enrich storage. In the end
        invokes inform_listeners from storage."""
        logging.info("Refreshing feed on %s..." % self.rssLink)

        try:
            feed = urllib.urlopen(self.rssLink)
            tree = ElementTree.XML(feed.read())
            feed.close()
            items = tree.find('channel').findall('item')

            for item in items:
                self.storage.add_tweet(
                    Tweet(
                        datetime.datetime(* time.strptime(' '.join(item.find('pubDate').text.split(' ')[:-1]), "%a, %d %b %Y %H:%M:%S")[:6]),
                        ': '.join(item.find('description').text.split(': ')[1:]).encode("utf-8"),
                        item.find('guid').text
                    )
                )

            self.storage.inform_listeners()
        except Exception, e:
            logging.error("Feed error: %s", e)


if __name__ == "__main__":
    """Simple testing script"""
    import sys
    if len(sys.argv) < 2:
        logging.fatal("No username given! Stopping...")
        print "Usage: %s [username]" % sys.argv[0]
        sys.exit(1)

    cl = TwitterClient(sys.argv[1])
    cl.start()

    shown = []

    while True :
        try:
            time.sleep(3)
            c =  cl.storage.get_all_sorted()
            for t in c:
                if t.guid not in shown:
                    print t
                    shown.append(t.guid)

        except KeyboardInterrupt, e:
            cl.stop()
            sys.exit(0)
    
