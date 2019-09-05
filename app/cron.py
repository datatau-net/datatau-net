import tweepy
from django.conf import settings

from .views import get_hottest

auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

api = tweepy.API(auth)


def tweet_post():
    hottest_posts = get_hottest(page=1)[0:settings.TWITTER_HOTTEST]

    tweet_text = ''
    for post in hottest_posts:
        if not post.tweeted:
            tweet_text = f'{post.title}: https://datatau.net/post/{post.id}'
            break

    if tweet_text:
        api.update_status(tweet_text)
