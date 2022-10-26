import tweepy
import time
import pandas as pd
import os

bearer = '<YOUR BEARER CODE>'
client = tweepy.Client(bearer, wait_on_rate_limit=False)

countries = {'IN': 'India', 'IR': 'Iran', 'NG': 'Nigeria', 'UG': 'Uganda',
             'GM': 'Gambia', 'LY': 'Libya', 'PK': 'Pakistan', 'ZW': 'Zimbabwe',
             'CA': 'Canada', 'GB': 'United Kingdom', 'FI': 'Finland', 'NO': 'Norway',
             'IE': 'Ireland', 'FR': 'France', 'AU': 'Australia', 'SG': 'Singapore'}

for c in countries:
    print(c)
    tweets = []
    for response in tweepy.Paginator(client.search_all_tweets,
                                     query='-is:retweet -is:reply -is:quote -is:nullcast lang:en place_country:SG',
                                     user_fields=['username', 'public_metrics', 'description', 'location'],
                                     tweet_fields=['created_at', 'geo', 'public_metrics', 'text'],
                                     expansions='author_id',
                                     start_time='2017-01-01T00:00:00Z',
                                     max_results=500,
                                     limit=200):
        time.sleep(1)
        tweets.append(response)

    result = []
    user_dict = {}
    # Loop through each response object
    for response in tweets:
        # Take all of the users, and put them into a dictionary of dictionaries with the info we want to keep
        for user in response.includes['users']:
            user_dict[user.id] = {'username': user.username,
                                  'followers': user.public_metrics['followers_count'],
                                  'tweets': user.public_metrics['tweet_count'],
                                  'description': user.description,
                                  'location': user.location
                                  }
        for tweet in response.data:
            # For each tweet, find the author's information
            author_info = user_dict[tweet.author_id]
            # Put all of the information we want to keep in a single dictionary for each tweet
            result.append({'author_id': tweet.author_id,
                           'username': author_info['username'],
                           'author_followers': author_info['followers'],
                           'author_tweets': author_info['tweets'],
                           'author_description': author_info['description'],
                           'author_location': author_info['location'],
                           'text': tweet.text,
                           'created_at': tweet.created_at,
                           'retweets': tweet.public_metrics['retweet_count'],
                           'replies': tweet.public_metrics['reply_count'],
                           'likes': tweet.public_metrics['like_count'],
                           'quote_count': tweet.public_metrics['quote_count']
                           })

    # Change this list of dictionaries into a dataframe
    df = pd.DataFrame(result)
    df.to_csv(c+'.csv', index=False)

# Aggregate all data and sample data
df_all = pd.DataFrame([], columns=df.columns)

directory = '<YOUR DIRECTORY HERE>'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if filename[:2] in countries:
        df = pd.read_csv(f, lineterminator='\n')
        df['country_code'] = filename[:2]
        df_all = pd.concat([df_all, df], axis=0).reset_index(drop=True)

df_all.to_csv('Tweets.csv', index=0)

df_all = pd.read_csv('Tweets.csv')
sample = df_all.groupby('country_code').apply(lambda x: x.sample(10000)).reset_index(drop=True)
sample.to_csv('sample.csv', index=0)


