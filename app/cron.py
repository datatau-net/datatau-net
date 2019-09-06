import tweepy
from django.conf import settings

from .views import get_hottest

auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

api = tweepy.API(auth)


def tweet_post():
    hottest_posts = get_hottest(page=1)[0:settings.TWITTER_HOTTEST]

    target_post = None
    for post in hottest_posts:
        if not post.tweeted:
            target_post = post
            break

    if target_post:
        tweet_text = f'{target_post.title}: https://datatau.net/post/{target_post.id}'
        api.update_status(tweet_text)
        
        target_post.tweeted = True
        target_post.save()

