import requests
import praw
import os
import secrets as s
import logging
import pandas as pd
import re
import ystockquote as ysq

# Set up logging for debugging HTTP requests to the Reddit API
if s.IS_DEBUG:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    for logger_name in ("praw", "prawcore"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)


try: 
    BASE_URL = 'https://www.reddit.com'
    SUBREDDIT = "wallstreetbets"

    reddit = praw.Reddit(
            user_agent=s.USER_AGENT,
            client_id=s.CLIENT_ID,
            client_secret=s.CLIENT_SECRET,
            username=s.USERNAME,
            password=s.PASSWORD
    )

    # Potential strategy:
    #
    #     Read the top 50 titles of wallstreetbets, parse those for tickers
    #
    #     Read the 10,000 most recent comments on wallstreetbets, scan for tickers and group them
    #
    #     Either take the top 10,000 comments or the comments from the top 50 posts

    subreddit = reddit.subreddit(SUBREDDIT).hot(limit=10)

    # Getting the top 200 comments
    comments = reddit.subreddit(SUBREDDIT).comments(limit=100000)


except Exception as e:
    print("There was an issue connecting to the Reddit API...")
    raise e

# extract the comments from the array and send to pandas dataframe
comment_arr = [com.body.upper() for com in comments]

# put all the individual words from the comments into an arr
word_arr = []
for com in comment_arr:
    words = com.split(" ")
    word_arr.extend(words)


# only get words where length is 1-5 characters long
pot_tickers = list(filter(lambda word: len(word) < 6, word_arr))

# only get words with actual characters in them
regex_pattern = "[A-Z]"
pattern = re.compile(regex_pattern)
pot_tickers = list(filter(lambda word: pattern.match(word), pot_tickers))

# for each word, strip everything out except for letters
pot_tickers = list(map(lambda word: re.sub(r'[^A-Z]', '', word), pot_tickers))

print(len(pot_tickers))

# for pt in pot_tickers:
    
#     if pt[0] != '$':
#         w = "$" + pt
#     else:
#         w = pt

#     pt_list.append(w)




# create a dataframe with the stickers and count the number of times the word appears
data = {"pot_tickers": pot_tickers}
df = pd.DataFrame(data=data)

# get the csv with the list of stock tickers that currently exist
tickers_file = "ticks.csv"
stock_tickers = pd.read_csv(tickers_file)

# do an inner join on the ticker names so we are only left with legit stock tickers
stock_tickers_wsb = pd.merge(left=df, right=stock_tickers, left_on="pot_tickers", right_on="ACT Symbol")['pot_tickers']

# count up all the times the ticker appears in the dataframe
vc_df = stock_tickers_wsb.value_counts(sort=True)

import pdb
pdb.set_trace()

# ticks = vc_df.index.tolist()
# nums = vc_df.tolist()

# print(set(zip(ticks, nums)))


# data = {'comment': comment_arr}
# df = pd.DataFrame(data=data)

# import pdb
# pdb.set_trace()


# endpoint = "/user/moneymay195/comments"
# url = BASE_URL + endpoint
# submission = reddit.submission(url=url)

print("SUCCESS")

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
# auth = requests.auth.HTTPBasicAuth(s.CLIENT_ID, s.CLIENT_SECRET)

# # here we pass our login method (password), username, and password
# data = {'grant_type': 'password',
#         'user_agent': s.USER_AGENT,
#         'username': s.USERNAME,
#         'password': s.PASSWORD, 
#         'client_id': s.CLIENT_ID,
#         'client_secret': s.CLIENT_SECRET}

# # setup our header info, which gives reddit a brief description of our app
# headers = {'User-Agent': s.USER_AGENT}

# # send our request for an OAuth token
# res = requests.post(base_url + 'api/v1/access_token',
#                     auth=auth, data=data, headers=headers)

# # convert response to JSON and pull access_token value
# TOKEN = res.json()['access_token']

# # add authorization to our headers dictionary
# headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# base_url = 'https://oauth.reddit.com'

# response = requests.get(base_url + '/r/wallstreetbets/about/rules', headers=headers)

#if response.status_code == 200:
    #print(response.json())

