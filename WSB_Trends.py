import requests
import praw

reddit = praw.Reddit(
    client_id='DfqePo7ZMhlddA',
    client_secret='mXKFSAo-SgdAPj7mg2QsPl1SeDRQiA',
    user_agent='WSB Sentiment Analysis'
)

for submission in reddit.subreddit("wallstreetbets").hot(limit=10):
    print(submission.title)

