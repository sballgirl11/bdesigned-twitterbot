
from os import environ
import time
import tweepy

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
user = api.me()
print(user.name)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text.encode("utf-8"))


def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except tweeWpy.RateLimitError:
        time.sleep(300)


# api.update_status('b.Designed Bot is now working! #python #tweepy')


# Narcissist bot
search = '#zerotomastery OR #ztm OR #svelte OR @svelte OR #javascript OR #webdev #womenwhocode OR #momscancode OR @WomenWhoCode'
totalItems = 10

for tweet in tweepy.Cursor(api.search, search).items(totalItems):
    try:
        tweet.favorite()  # likes
        tweet.retweet()  # retweets
        print('It worked')
    except tweepy.TweepError as err:
        print(err.reason)
    except StopIteration:
        break

# generous bot
for follower in limit_handler(tweepy.Cursor(api.followers).items()):
    follower.follow()
    break
