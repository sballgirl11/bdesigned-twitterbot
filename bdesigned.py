import tweepy
import time
from config import create_api


class Stream_Listener(tweepy.StreamListener):
    """Defines the tweet status and error state

    """

    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        """Checks the status of the tweet. Mark it as favourite if not already done it and retweet if not already
        retweeted.

        :param tweet: tweet from listening to the stream
        """
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                print('Stream favorited tweet:', tweet.text)
            except tweepy.TweepError as error:
                print(error)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                print('Stream retweeted tweet:', tweet.text)
            except tweepy.TweepError as error:
                print(error)

    def on_error(self, status_code):
        """When encountering an error while listening to the stream, return False if `status_code` is 420 and print
        the error.

        :param status_code:
        :return: False when `status_code` is 420 to disconnect the stream.
        """
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
        elif status_code == 429:
            time.sleep(900)
        else:
            print(tweepy.TweepError, status_code)


def main(follow, keyword):
    """Main method to initialize the api, create a Stream_Listener object to track tweets based on certain keywords and
    follow tweet owners and the mentors.
    """
    api = create_api()
    my_stream_listener = Stream_Listener(api)
    my_stream = tweepy.Stream(auth=api.auth, listener=my_stream_listener)
    my_stream.filter(track=keyword, follow=follow)
# is_async=True, languages=["en"]


if __name__ == "___main__":
    track_list = ['Python', 'JavaScript', 'WebDev', 'WomenWhoCode', 'MomsCanCode', 'zerotomastery', 'ztm', 'Zero To Mastery', 'programmer', 'svelte', 'sveltejs', 'sapper', 'BrittneyPostma', 'b.Designed',
                  'bDesigned', 'BrittneyPostma', 'bDesigned', 'syntax', 'syntaxfm', '@syntaxFM', '@stolinski', '@wesbos', '@bDesignedWebDev', '@PostmaBrittney', '#zerotomastery', '#ztm', 'bDesignedWebDev', '@BrittneyPostma']
    follow_list = '733722018596687872'
    # ['224115510', '815246', '18727585', '733722018596687872', '801833412487184384', '459275531']
    main(track_list, follow_list)
    print('Streaming...')
