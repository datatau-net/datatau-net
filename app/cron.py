import logging

import tweepy
from django.conf import settings

from .views import get_hottest

twitter_keys = settings.TWITTER_KEYS
twitter_retweet_keys = settings.TWITTER_RETWEET_KEYS


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


log = get_logger()


def get_api(keys):
    auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'],
                               keys['CONSUMER_SECRET'])
    auth.set_access_token(keys['ACCESS_TOKEN'],
                          keys['ACCESS_SECRET'])

    return tweepy.API(auth)


api = get_api(twitter_keys)


def retweet_post(status, keys_dict):
    for user in keys_dict:
        log.info(f'user {user} retweeting...')
        user_api = get_api(keys_dict[user])

        user_api.retweet(status.id)
        user_api.create_favorite(status.id)


def tweet_post():
    log.info('getting hottests posts...')
    hottest_posts = get_hottest(page=1)[0:settings.TWITTER_HOTTEST]

    target_post = None
    for post in hottest_posts:
        if not post.tweeted:
            target_post = post
            break

    if target_post:
        tweet_text = f'{target_post.title}: https://datatau.net/post/{target_post.id}'
        log.info(f'tweet to post: {tweet_text}')

        status = api.update_status(tweet_text)

        log.info('tweet posting success')
        target_post.tweeted = True
        target_post.save()

        log.info('retweeting and liking...')
        retweet_post(status, twitter_retweet_keys)

        log.info('tweet retweeting success')
    else:
        log.info('all hot posts already tweeted')
