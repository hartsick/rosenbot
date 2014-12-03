import twitter
import os
import random
import redis
import nltk

# Load environment variables
consumer_key = os.environ.get('ROSENBOT_CONSUMER_KEY')
consumer_secret = os.environ.get('ROSENBOT_CONSUMER_SECRET')
access_token = os.environ.get('ROSENBOT_ACCESS_TOKEN')
access_token_secret = os.environ.get('ROSENBOT_ACCESS_TOKEN_SECRET')

# NLTK Init
if os.path.exists('nltk_data/tokenizers/punkt/english.pickle') is not True:
    nltk.download('punkt', './nltk_data')
sent_detector = nltk.data.load('nltk_data/tokenizers/punkt/english.pickle')

# Redis Init
redis_url = os.getenv('ROSENBOT_REDISTOGO_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

# Twitter Init
api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

# Read given text & split into sentences
with open('text-file.txt', 'r') as f:
    read_data = f.read().decode('utf8').replace("\n", " ")
sentences = sent_detector.tokenize(read_data)

# Get sentences under 140 characters
tweetable_sentences = [sentence for sentence in sentences if len(sentence) < 140]

while True:
    # Pick random tweet, see if it has been tweeted before
    # If so, try again. If not, tweet away
    tweet = random.choice(tweetable_sentences)

    if r.sismember('past_tweets', tweet) is False:

        # Post tweet and save it to DB
        api.PostUpdate(tweet)
        r.sadd('past_tweets', tweet)

        break
