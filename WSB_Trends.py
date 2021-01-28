import requests
import praw
import os
import secrets as s
import logging


# Set up logging for debugging HTTP requests to the Reddit API
if s.IS_DEBUG:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
                logger = logging.getLogger(logger_name)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(handler)



BASE_URL = 'https://www.reddit.com'
SUBREDDIT = "wallstreetbets"

reddit = praw.Reddit(
    client_id='DfqePo7ZMhlddA',
    client_secret='mXKFSAo-SgdAPj7mg2QsPl1SeDRQiA',
    user_agent='WSB Sentiment Analysis'
)

subreddit = reddit.subreddit(SUBREDDIT).hot(limit=10)

for submission in subreddit:
    print(submission.title)

