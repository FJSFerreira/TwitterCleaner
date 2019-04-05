import config

import tweepy
import datetime

threshold_date = datetime.datetime.now()-datetime.timedelta(days=config.days_to_keep)

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

timeline = tweepy.Cursor(api.user_timeline).items()
since_id = 1

to_delete = []

for tweet in timeline:
    if tweet.created_at < threshold_date:
        print('ID {} adicionado a lista de tweets a eliminar'.format(tweet.id))
        to_delete.append(tweet.id)
        since_id = tweet.id

print('Serao apagados {} tweets (antes de filtragem)'.format(len(to_delete)))

retweets = tweepy.Cursor(api.retweets_of_me).items()

for tweet in retweets:
    for retweet in tweet.retweets():
        if tweet.id in to_delete and retweet.created_at > threshold_date:
            print('ID {} removido da lista de tweets a eliminar'.format(tweet.id))
            to_delete.remove(tweet.id)

print('Serao apagados {} tweets (apos filtrar retweets)'.format(len(to_delete)))

mentions = tweepy.Cursor(api.mentions_timeline, since_id=since_id).items()

for tweet in mentions:
    if tweet.id in to_delete and retweet.created_at > threshold_date:
            print('ID {} removido da lista de tweets a eliminar'.format(tweet.id))
            to_delete.remove(tweet.id)

print('Serao apagados {} tweets (apos filtrar conversas)'.format(len(to_delete)))


for tweet in to_delete:
	print('A eliminar tweet com o ID {}...'.format(tweet))
	api.destroy_status(tweet)     