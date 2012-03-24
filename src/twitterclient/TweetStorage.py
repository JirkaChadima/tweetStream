
__author__="Jiri Chadima"
__date__ ="$Mar 7, 2011 10:42:07 AM$"

MAX_SIZE = 50

class Tweet :
    """Simple data container"""
    def __init__(self, pubDate, text, link):
        """Guid is extracted from link"""
        self.pubDate = pubDate
        self.text = text
        self.link = link
        self.guid = link.split('/')[-1:][0]

    def __str__(self):
        return self.pubDate.strftime("%d. %m. %Y %H:%M") + ': ' + self.text



class TweetStorage :
    """Container for lots of tweets"""
    def __init__(self):
        """Data fields initialization"""
        self.data = []
        self.guids = []
        self.listeners = []

    def get_last(self, limit = 1):
        """Returns 'limit' of recently added tweets. Tweets are sorted before."""
        if len(self.data) == 0:
            return None
        self.sort_and_reduce()
        if len(self.data) < limit:
            limit = len(self.data)

        return self.data[-limit:][0]

    def get_all_sorted(self):
        """Sorts all tweets and returns them"""
        self.sort_and_reduce()
        return self.data

    def sort_and_reduce(self):
        """Sorts tweets by pubDate, oldest first. If there's more tweets than MAX_SIZE,
        they are deleted."""
        self.data = sorted(self.data, key=lambda item: item.pubDate)
        if len(self.data) > MAX_SIZE:
            self.data = self.data[-MAX_SIZE:]


    def add_tweet(self, tweet):
        """Tries to add tweet. If tweet with such guid exists, it is not added."""
        if tweet.guid not in self.guids:
            self.guids.append(tweet.guid)
            self.data.append(tweet)


    def add_listener(self, listener):
        """Registers listener. See observer design pattern."""
        self.listeners.append(listener)

    def inform_listeners(self):
        """Invokes stream_updated method on all registered listeners"""
        d = self.get_all_sorted()
        for listener in self.listeners:
            listener.stream_updated(d)
            

