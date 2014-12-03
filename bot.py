import twitter
import os
import random
import redis

# Load environment variables
consumer_key = os.environ.get('ROSENBOT_CONSUMER_KEY')
consumer_secret = os.environ.get('ROSENBOT_CONSUMER_SECRET')
access_token = os.environ.get('ROSENBOT_ACCESS_TOKEN')
access_token_secret = os.environ.get('ROSENBOT_ACCESS_TOKEN_SECRET')

# Init
redis_url = os.getenv('ROSENBOT_REDISTOGO_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret)

# Take in given text
with open('text-file.txt', 'r') as f:
    text = f.read()

# Separate text by sentence
cleaned_text = text.replace("\n", "")
sentences = cleaned_text.split(".")

# Get sentences under 140 characters
tweetable_sentences = []

for sentence in sentences:
    if len(sentence) < 140 and len(sentence) > 1:
        formatted_sentence = "{0}.".format(sentence)
        tweetable_sentences.append(formatted_sentence)

while True:
    # Pick random tweet, see if it has been tweeted before
    # If so, try again. If not, tweet away
    tweet_sentence = random.choice(tweetable_sentences)

    if r.sismember('past_tweets', tweet_sentence) is False:

        # Post tweet and save it to DB
        status = api.PostUpdate(tweet_sentence)
        r.sadd('past_tweets', tweet_sentence)
        r.save()

        break
