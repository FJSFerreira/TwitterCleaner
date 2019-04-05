# Based on: https://pushpullfork.com/i-deleted-tweets/

import config

import tweepy
import csv
import sys

def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)

def read_csv(file):
    with open(file, encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        rows = []
        for line in reader:
            row_data = []
            for element in line:
                row_data.append(element)
            if row_data != []:
                rows.append(row_data)
    return(rows)

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth)

tweets = read_csv(sys.argv[1])

for tweet in tweets:
    print('A eliminar tweet com o ID {}...'.format(tweet[0]))
    try:
        api.destroy_status(tweet[0])
    except:
        print('Tweet com o ID {} nao encontrado.'.format(tweet[0]))